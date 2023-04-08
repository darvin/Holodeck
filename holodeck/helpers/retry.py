
import functools


def retry(max_attempt: int=3):
    """
    Function decorator that retries calling a function with a specified maximum number of attempts,
    logs errors to stdout, and raises an exception if the function fails after reaching the maximum number of attempts.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempt:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    # Log the error to stdout
                    print(f'Error in function {func.__name__}: {e}')
                    attempts += 1
            raise Exception(f'Function {func.__name__} failed after {max_attempt} attempts')
        return wrapper
    return decorator