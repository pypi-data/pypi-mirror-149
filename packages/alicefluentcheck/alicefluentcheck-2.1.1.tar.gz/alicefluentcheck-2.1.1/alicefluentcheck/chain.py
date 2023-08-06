from functools import wraps


def chained(fn):
    @wraps(fn)
    def new(*args, **kwargs):
        fn(*args, **kwargs)
        return args[0]

    return new
