import functools


class PubsubError(Exception):
    def __init__(self, message):
        super().__init__(message)


def exception_mapper(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except PubsubError:
            raise
        # except NotFound:
        #     raise

        except Exception as e:
            raise PubsubError('Pubsub error: ') from e

    return wrapper
