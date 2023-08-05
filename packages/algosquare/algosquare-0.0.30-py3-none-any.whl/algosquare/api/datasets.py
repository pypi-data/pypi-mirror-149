import io
import time
import numpy as np
import pandas as pd
import requests
import json

from ..base.tabular import is_input_metatype
from ..base.types import is_target_metatype
from ..metrics import get_metric

from .api import ApiObject, api_get, api_post, api_put, throttle
from .tasks import Task


def get_datasets():
    return [Dataset.load(x) for x in api_get('api/datasets')]

class Dataset(ApiObject):
    def __init__(self, entry):
        if type(self) == Dataset:
            raise RuntimeError('base class should not be instantiated')
        super().__init__(entry)

    def __repr__(self):
        return str({f : getattr(self, f, None) for f in ['title', 'data_format', 'status', 'dataset_id']})

    @staticmethod
    def load(entry):
        if entry['data_format'] == 'tabular':
            return TabularData(entry)
        else:
            raise ValueError('unknown data_format')

    @throttle(60)
    def refresh(self):
        self.update(api_get('api/datasets/{}'.format(self.dataset_id)))

    @throttle(10)
    def get_tasks(self):
        return [Task(x) for x in api_get('api/datasets/{}/tasks'.format(self.dataset_id))]

class TabularData(Dataset):
    @classmethod
    def from_csv(cls, title, input_file, target_file, input_metatypes = None, target_metatypes = None):
        input_df = pd.read_csv(input_file, dtype=str)
        target_df = pd.read_csv(target_file, dtype=str)
        return cls.from_df(title, input_df, target_df, input_metatypes, target_metatypes)

    @classmethod
    def from_df(cls, title, input_df, target_df, input_metatypes = None, target_metatypes = None):
        if not isinstance(title, str):
            raise TypeError('title must be a string')
        if len(title) > 1024:
            raise ValueError('title must be maximum 1024 characters')

        if not isinstance(input_df, pd.DataFrame):
            raise TypeError('input_df must be a DataFrame')
        if not isinstance(target_df, pd.DataFrame):
            raise TypeError('target_df must be a DataFrame')

        metatypes = []

        if input_metatypes is not None:
            metatypes = _prepare_metatypes(input_df, input_metatypes)
            for metatype in metatypes.values():
                if not is_input_metatype(metatype):
                    raise ValueError(f'invalid input metatype: {metatype}')
            metatypes.append(dict(namespace = 'inputs', metadata = [dict(name = name, metatype = metatypes.get(name, 'void')) for name in input_df]))

        if target_metatypes is not None:
            metatypes = _prepare_metatypes(input_df, input_metatypes)
            for metatype in metatypes.values():
                if not is_target_metatype(metatype):
                    raise ValueError(f'invalid target metatype: {metatype}')
            metatypes.append(dict(namespace = 'targets', metadata = [dict(name = name, metatype = metatypes.get(name, 'void')) for name in target_df]))

        files = [dict(namespace = namespace, key = _upload_dataframe(namespace, df)) for namespace, df in [('inputs', input_df), ('targets', target_df)]]
        entry = api_post('api/datasets', json=dict(settings = dict(title = title, data_format = 'tabular'), files = files, metatypes = metatypes))
        return cls(entry)

    @throttle(10)
    def create_task(self, title, evaluation_metric, holdout = 25, input_columns = None, target_columns = None):
        holdout = int(holdout)
        if holdout < 5 or holdout > 30:
            raise ValueError('holdout outside of range 5-30')

        if input_columns is None:
            input_columns = [x['name'] for x in self.metadata['inputs']]

        if target_columns is None:
            target_columns = [self.metadata['targets'][0]['name']]

        if len(target_columns) != 1:
            raise ValueError('only one target column is currently allowed')

        columns = dict(inputs = input_columns, targets = target_columns)
        features = {namespace : [x for x in self.metadata[namespace] if x['name'] in columns[namespace]] for namespace in self._namespaces()}

        if len(features['inputs']) == 0:
            raise ValueError('no X features selected')

        if len(features['targets']) != 1:
            raise ValueError('only one y feature must be selected')

        task_type = 'regression' if features['targets'][0]['metatype'] == 'numerical' else 'classification'

        metric = get_metric(evaluation_metric)
        if task_type != metric._task_type:
            raise ValueError(f'{evaluation_metric} is not a {task_type}-metric')

        payload = dict()
        payload['settings'] = dict(title = title, evaluation_metric = evaluation_metric, holdout = holdout, task_type = task_type)
        payload['selections'] = [dict(namespace = namespace, features = [x['feature_id'] for x in v]) for namespace, v in features.items()]

        return Task(api_post(f'api/datasets/{self.dataset_id}/tasks', json=payload))

def _prepare_metatypes(data_df, metatypes):
    if isinstance(metatypes, str):
        mt_df = pd.read_csv(metatypes, dtype = str, index_col = 0)
        if mt_df.shape[1] != 1:
            raise ValueError(f'{metatypes} must have exactly two columns')
        output = mt_df.squeeze().to_dict()
        if set(output.keys()).difference(data_df):
            raise ValueError(f'{metatypes} have invalid names')
        return output
    else:
        return dict(zip(data_df, metatypes))

def _upload_dataframe(namespace, df):
    with io.BytesIO() as f:
        df.to_csv(f, index=False)
        r = api_put('api/scratchpad', json=dict(filename = f'{namespace}.csv'))
        requests.put(r['url'], data=f.getvalue())
        return r['key']

def _sizeof_fmt(num, suffix="B"):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi']:
        if abs(num) < 1024.0 or unit == 'Pi':
            break
        num /= 1024.0
    return f'{num:3.1f} {unit}{suffix}'