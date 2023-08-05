# Copyright: (c) 2022, Swimlane <info@swimlane.com>
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)

from functools import wraps
from requests.exceptions import (
    HTTPError,
    ConnectionError,
    Timeout,
    RequestException
)
from swimlane.exceptions import SwimlaneHTTP400Error

from .base import Base


def log_exception(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except SwimlaneHTTP400Error as sw:
            Base().log_exception(sw.args)
            if not Base.continue_on_error:
                raise sw
        except HTTPError as he:
            log = f"Unable to process '{func.__name__}' request"
            if kwargs:
                log += f" with the requested parameters '{', '.join([x for x in kwargs.keys()])}' {kwargs}."
            Base().log_exception(log)
            if not Base.continue_on_error:
                raise he
        except ConnectionError as errc:
            Base().log_exception(f"An Error Connecting to the API occurred: {repr(errc)}")
            if not Base.continue_on_error:
                raise errc
        except Timeout as errt:
            Base().log_exception(f"A timeout error occurred: {repr(errc)}")
            if not Base.continue_on_error:
                raise errt
        except RequestException as err:
            Base().log_exception(f"An Unknown Error occurred: {repr(err)}")
            if not Base.continue_on_error:
                raise err
        except Exception as e:
            Base().log_exception(f"There was an unknown exception that occurred in '{func.__name__}': {e}")
            if not Base.continue_on_error:
                raise e
    return wrapper
