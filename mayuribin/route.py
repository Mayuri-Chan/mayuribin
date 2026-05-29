from fastapi import Request

get_list = []
post_list = []

class Route:
    def get(path, enable_docs=True, **kwargs):
        def decorator(func):
            get_list.append({"path": path, "func_name": func.__name__, "enable_docs": enable_docs, "kwargs": kwargs})
            return func
        return decorator

    def post(path, enable_docs=True, **kwargs):
        def decorator(func):
            post_list.append({"path": path, "func_name": func.__name__, "enable_docs": enable_docs, "kwargs": kwargs})
            return func
        return decorator

    def load_routes(self):
        for route in get_list:
            endpoint = getattr(self, route["func_name"])
            self.add_api_route(route["path"], endpoint, methods=["GET"], include_in_schema=route["enable_docs"], **route["kwargs"])
        for route in post_list:
            endpoint = getattr(self, route["func_name"])
            self.add_api_route(route["path"], endpoint, methods=["POST"], include_in_schema=route["enable_docs"], **route["kwargs"])
