from .api import ApiObject, api_post, api_get, api_delete

def get_deployed():
    return [Model(x) for x in api_get('api/models/deployments').json()]

class Model(ApiObject):
    def deploy(self):
        self.update(api_post(f'api/models/{self.model_id}/deployment'))

    def discharge(self):
        self.update(api_delete(f'api/models/{self.model_id}/deployment'))

    def predict(self, data):
        return api_post(f'api/models/{self.model_id}/prediction', data = data)

