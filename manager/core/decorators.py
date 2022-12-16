import timeit


def time_calculator_decorator(func):
    def wrapper(*args, **kwargs):
        start = timeit.default_timer()
        func(*args, **kwargs)
        stop = timeit.default_timer()
        print("Timer", stop-start)
        return func(*args, **kwargs)

    return wrapper
