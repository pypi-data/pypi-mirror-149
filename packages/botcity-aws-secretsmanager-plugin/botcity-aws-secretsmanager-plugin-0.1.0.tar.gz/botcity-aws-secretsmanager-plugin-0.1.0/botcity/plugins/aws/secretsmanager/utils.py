from functools import wraps

from botocore.exceptions import ClientError


def secret_not_found_handler(func):
    """
    Decorator which handle ResourceNotFoundException.
    Args:
        func (callable): The function to be wrapped
    Returns:
        wrapper (callable): The decorated function
    """

    @wraps(func)
    def inner(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except ClientError as err:
            if not self.RAISE_IF_NOT_FOUND and err.response['Error']['Code'] == 'ResourceNotFoundException':
                return None
            else:
                raise err

    return inner
