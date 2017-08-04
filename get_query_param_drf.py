def get_query_params(self, param):
    return {param: self.request.query_params.get(param)} if self.request.query_params.get(param) else {}

def get(self, *args, **kwargs):
    params = {}
    for param in self.available_params:
        params.update(self.get_query_params(param))
