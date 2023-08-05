"""Testing of tabular algos."""
import uuid
import time
import pickle
import os
import numpy as np
import pandas as pd
import datetime

from .errors import TestError
from .targets import create_classification_target, create_regression_target
from ..base.tabular import TabularClassifier, TabularRegressor, is_input_metatype
from ..base.types import Metatype, is_classification_metatype, is_delimiter_metatype, get_delimiter
from ..metrics.metrics import get_metric

def create_tabular_inputs(input_metatypes, n_rows = 1000, n_cols = 2, seed = 0):
    X_metatypes = []
    data = []
    index = range(n_rows)

    for metatype in input_metatypes:
        X_metatypes += [metatype for _ in range(n_cols)]

        rng = np.random.default_rng(seed = seed)

        if metatype == Metatype.NUMERICAL:
            x = create_regression_target(index, n_cols, seed = seed)
        elif metatype == Metatype.CATEGORICAL:
            x = create_classification_target(index, n_cols, ['red', 'green', 'blue', 'yellow'], seed = seed)
        elif metatype == Metatype.BINARY:
            x = create_classification_target(index, n_cols, ['bad', 'good'], seed = seed)
        elif metatype == Metatype.DATETIME:
            timestamps = pd.DataFrame(datetime.datetime(2022, 2, 22, 0, 0).timestamp() + rng.normal(0, 1e6, (n_rows, n_cols)))
            x = timestamps.applymap(lambda x: datetime.datetime.fromtimestamp(x).isoformat())
        elif metatype == Metatype.TIMESTAMP:
            x = pd.DataFrame(datetime.datetime(2022, 2, 22, 0, 0).timestamp() + rng.normal(0, 1e6, (n_rows, n_cols)))
        elif is_delimiter_metatype(metatype, strict = True):
            delim = get_delimiter(metatype)
            categories = ['dog','cat','dolphin','lion']
            idx = pd.DataFrame(rng.integers(1,len(categories),size=(1000, n_cols)))
            x = idx.applymap(lambda x: delim.join(categories[:x]))
        else:
            raise TestError('invalid metatype')

        data.append(x)

    X = pd.concat(data, axis = 1)
    X.columns = [f'X{i}' for i in range(X.shape[1])]
    return (X.astype(str), X_metatypes)

def load_tabular_data(algo, nan_fraction = 0.1):
    X, X_metatypes = create_tabular_inputs(algo.input_metatypes())

    rng = np.random.default_rng(seed = 0)
    X.mask(rng.uniform(size = X.shape) < nan_fraction, inplace=True)

    is_multioutput = algo.is_multioutput()
    if not isinstance(is_multioutput, bool):
        raise TestError('is_multioutput should return bool')

    n_cols = 3 if is_multioutput else 1

    if isinstance(algo, TabularClassifier):
        target_metatype = algo.target_metatype()
        categories = ['bad', 'good'] if target_metatype == Metatype.BINARY else ['red', 'green', 'blue', 'yellow']
        y = create_classification_target(X.index, n_cols, categories)
        y_metatypes = [target_metatype for x in range(n_cols)]
    elif isinstance(algo, TabularRegressor):
        y = create_regression_target(X.index, n_cols)
        y_metatypes = [Metatype.NUMERICAL for x in range(n_cols)]
    else:
        raise TypeError('invalid algo class')

    return (X, y, X_metatypes, y_metatypes)

def test_tabular(algo, output_dir, timeout, nan_fraction):
    output = dict()

    input_metatypes = algo.input_metatypes()
    if not isinstance(input_metatypes, set) or not input_metatypes:
        raise TestError('input_metatypes must be a non-empty set')

    for metatype in input_metatypes:
        if not is_input_metatype(metatype):
            raise TestError('invalid input metatype')

    output['input_metatypes'] = sorted(list(input_metatypes), key=lambda x: x.name)

    is_multioutput = algo.is_multioutput()
    if not isinstance(is_multioutput, bool):
        raise TestError('is_multioutput should return bool')

    output['is_multioutput'] = is_multioutput

    if isinstance(algo, TabularClassifier):
        target_metatype = algo.target_metatype()
        if not is_classification_metatype(target_metatype):
            raise TestError('invalid classification metatype')

        output['target_metatype'] = target_metatype

        metric = get_metric('accuracy')
    else:
        metric = get_metric('mean_squared_error')

    X, y, X_metatypes, y_metatypes = load_tabular_data(algo, nan_fraction)

    t_start = time.time()
    algo.fit(timeout, metric, X, y, X_metatypes, y_metatypes, X_unlabelled = X)
    fit_seconds = time.time() - t_start

    if fit_seconds > timeout + 10:
        raise TestError('timeout significantly exceeded')

    pred = algo.predict(X)
    if not isinstance(pred, pd.DataFrame):
        raise TestError('prediction must be DataFrame')

    if list(pred.columns) != list(y.columns):
        raise TestError('prediction columns must equal y columns')

    if list(pred.index) != list(X.index):
        raise TestError('prediction index must equal X index')

    prediction_methods = ['predict']

    if isinstance(algo, TabularClassifier):
        for prediction_method in ('predict_proba', 'decision_function'):
            try:
                pred_prediction_method = getattr(algo, prediction_method)(X)
                if not algo.is_multioutput():
                    pred_prediction_method = [pred_prediction_method]

                for ppm, col in zip(pred_prediction_method, y):
                    _check_prediction(prediction_method, ppm, X, y[col], pred[col])

                prediction_methods.append(prediction_method)
            except NotImplementedError:
                pass

    output['prediction_methods'] = sorted(prediction_methods)

    if output_dir is not None:
        filename = os.path.join(output_dir, str(uuid.uuid4()) + '.mdl')
        algo.save(filename)

        algo_loaded = algo.load(filename)
        pred_loaded = algo_loaded.predict(X)

        if not pred_loaded.equals(pred):
            raise TestError('loaded model predictions are off')

        os.remove(filename)

    print(f'TESTING DONE: {type(algo).__name__}')
    return output

def _check_prediction(prediction_method, ppm, X, y, pred):
    if not isinstance(ppm, pd.DataFrame):
        raise TestError(f'{prediction_method} must return a DataFrame for univariate and list thereof for multivariate problems')

    if list(ppm.index) != list(X.index):
        raise TestError('prediction index must equal X index')

    if prediction_method == 'predict_proba':
        if (ppm < 0).any(axis = None):
            raise TestError(f'{prediction_method} probabilities cannot be negative')

        if (ppm > 1).any(axis = None):
            raise TestError(f'{prediction_method} probabilities cannot be greater than 1')

        if ((ppm.sum(axis=1) - 1).abs() > 1e-6).any():
            raise TestError(f'{prediction_method} probabilities must sum to 1 for each row')

    if prediction_method in ('predict_proba', 'decision_function'):
        idx = ppm.to_numpy().argmax(axis = 1)
        if ppm.columns[idx].tolist() != pred.tolist():
            raise TestError(f'argmax of {prediction_method} output should equal predicted class')

    y_unique = set(y)

    if ppm.shape[1] != len(y_unique) or set(ppm.columns) != y_unique:
        raise TestError(f'{prediction_method} must have a column for each class')
