from asf.api import HttpMethod
import asf.utils.keys as keys
from typing import List, Optional
from asf.response import BaseResponse, FailResponse

_functions = {}

class RestApi(object):
    
    def execute(self, event: any, context: any) -> BaseResponse:
        path = event.get(keys.PATH)
        http_method = event.get( keys.HTTPMETHOD)
        http_method = HttpMethod(http_method)
        if f'{path}#{http_method}' not in _functions:
            return FailResponse(status_code=502, message='Bad Gateway')
        func_dict = _functions[f'{path}#{http_method}']
        func = func_dict.get(keys.FUNCTION)
        any_roles = func_dict.get( keys.HAS_ANY_ROLES, [])
        all_roles = func_dict.get( keys.HAS_ALL_ROLES, [])
        if any_roles or all_roles:
            oauth = self.preauthorize(event, any_roles, all_roles)
            if oauth:
                return oauth
        return func(event, context)
    

    def preauthorize(self, event: any, has_any_roles: List[str] = [], has_all_roles: List[str] = []) -> Optional[FailResponse]:
        try:
            roles = event['requestContext']['authorizer']['roles'].split(",,")
            if len(has_any_roles) > 0:
                at_least_one = False
                for current_role in has_any_roles:
                    if any(current_role in role for role in roles):
                        at_least_one = True
                        break
                if not at_least_one:
                    raise Exception('Unauthorized')
            if len(has_all_roles) > 0:
                for current_role in has_all_roles:
                    if not any(current_role in role for role in roles):
                        raise Exception('Unauthorized')
            return None
        except:
            return FailResponse(status_code=401, message='Unauthorized')
        
        
    def route(func: any, name: str, method: HttpMethod, has_any_roles: List[str] = [], has_all_roles: List[str] = []) -> any:

        def wrapper(func):
            global _functions
            
            _functions[f'{name}#{str(method)}'] = {
                keys.FUNCTION: func,   
                keys.HAS_ANY_ROLES: has_any_roles,
                keys.HAS_ALL_ROLES: has_all_roles,
            }

        return wrapper
