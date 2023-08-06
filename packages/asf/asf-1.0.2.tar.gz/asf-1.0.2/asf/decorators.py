import time
import jsons
import logging
import functools
from typing import List

_logger = logging.getLogger(__name__)
_logger.setLevel(level=logging.INFO)


def serializable(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        return jsons.dump(res, default=lambda o: o.__dict__)

    return wrapper


def autolog(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            _logger.info(f"Starting method from Function: {func.__name__} "
                         f"Parameters: {['{0} '.format(str(arg)) for arg in args]} {['{0}: {1}'.format(key, str(param)) for key, param in kwargs.items()]}".replace("'", ""))
        except Exception:
            pass
        res = func(*args, **kwargs)
        try:
            _logger.info(f"Completed method from Function: {func.__name__}")
        except Exception:
            pass
        return res

    return wrapper


def viewable(func):
    @functools.wraps(func)
    def call(*args, **kwargs):
        return func(*args, **kwargs)

    call.is_viewable = True
    return call


class _preauthorize:
    def __init__(self, func: any = None, has_any_roles: List[str] = [], has_all_roles: List[str] = []):
        self.func = func
        self.has_any_roles = has_any_roles
        self.has_all_roles = has_all_roles

    def __call__(self, *args: any, **kwargs: any) -> any:
        try:
            event = args[0]
            roles = event['requestContext']['authorizer']['roles'].split(",,")
            if len(self.has_any_roles) > 0:
                at_least_one = False
                for current_role in self.has_any_roles:
                    if any(current_role in role for role in roles):
                        at_least_one = True
                        break
                if not at_least_one:
                    raise Exception('Unauthorized')
            if len(self.has_all_roles) > 0:
                for current_role in self.has_all_roles:
                    if not any(current_role in role for role in roles):
                        raise Exception('Unauthorized')
            return self.func(*args, **kwargs)
        except:
            return {"statusCode": 401, "body": jsons.dump("Unauthorized")}

    def __get__(self, instance: any, instancetype: any) -> any:
        return functools.partial(self.__call__, instance)


def preauthorize(func=None, has_any_roles: List[str] = [], has_all_roles: List[str] = []):
    if func:
        return _preauthorize(func)
    else:
        def wrapper(func):
            return _preauthorize(func, has_any_roles, has_all_roles)

        return wrapper


def delay(func=None, seconds: int = 0):
    if func:
        return _delay(func)
    else:
        def wrapper(func):
            return _delay(func, seconds)

        return wrapper


class _delay:
    def __init__(self, func: any = None, seconds: int = 0):
        self.func = func
        self.seconds = seconds

    def __call__(self, *args: any, **kwargs: any) -> any:
        time.sleep(self.seconds)
        res = self.func(*args, **kwargs)
        return res

    def __get__(self, instance: any, instancetype: any) -> any:
        return functools.partial(self.__call__, instance)
