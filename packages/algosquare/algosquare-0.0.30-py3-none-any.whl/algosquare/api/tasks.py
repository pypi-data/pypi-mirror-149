from .api import ApiObject, api_get, api_post, api_delete, throttle
from .models import Model

class Task(ApiObject):
    @throttle(60)
    def refresh(self):
        self.update(api_get(f'api/tasks/{self.task_id}'))

    def start_automl(self, run_time, max_algos, max_server_cost):
        if self.status != 'inactive':
            raise RuntimeError('status must be inactive')

        self.update(api_post(f'api/tasks/{self.task_id}/automl', dict(run_time = run_time, max_algos = max_algos, max_server_cost = max_server_cost)))

    def stop_automl(self):
        if self.status == 'inactive':
            raise RuntimeError('task is inacative')

        self.update(api_delete(f'api/tasks/{self.task_id}/automl'))

    @throttle(60)
    def get_models(self):
        return [Model(x) for x in api_get(f'api/tasks/{self.task_id}/models')]