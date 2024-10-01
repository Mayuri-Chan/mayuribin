from aiohttp import web

routes_list = []

class Route:
    def get(path):
        def decorator(func):
            def wrapper(request):
                self = request.app
                return func(self, request)
            routes_list.append(web.get(path, wrapper))
            return wrapper
        return decorator

    def post(path):
        def decorator(func):
            def wrapper(request):
                self = request.app
                return func(self, request)
            routes_list.append(web.post(path, wrapper))
            return wrapper
        return decorator
