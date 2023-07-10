class Demo():
    def __init__(self):

        self.route_handlers = {}

    def route(self, path, methods = ['GET']):
        # Decorator to register a route handler
        def decorator(func):
    #            self.route_handlers['routes'] = {path, func, methods}
            self.route_handlers[path] = {'func': func, 'methods': tuple(methods)}
            return func
        return decorator

app = Demo()

@app.route('/')
def home():
    print('home')

