_callback = None

def init(callback):
    global _callback
    _callback = callback
    return

def query(query: str, context: str = ""):
    def wrapper_func(func):
        def wrapper_decorator(*args, **kwargs):
            return _callback(query, args, context)
        return wrapper_decorator
    return wrapper_func
