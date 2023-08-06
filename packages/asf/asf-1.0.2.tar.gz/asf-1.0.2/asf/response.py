import jsons
from typing import Optional


class BaseResponse:
    def __init__(self, status_code: int) -> None:
        self.statusCode = status_code  # pylint: disable=invalid-name


class SuccessResponse(BaseResponse):
    def __init__(self, status_code: int = 200, body: Optional[any] = None, content_type: str = "application/json") -> None:
        super().__init__(status_code)
        self.headers = {"content-type": content_type, "access-control-allow-origin": "*"}
        self.body = jsons.dumps(body) if body else None


class FailResponse(BaseResponse):
    def __init__(self, status_code: int, message: str, description: Optional[str] = None) -> None:
        super().__init__(status_code)
        self.headers = {"content-type": "application/json", "access-control-allow-origin": "*"}
        self.body = jsons.dumps({"fault": {"code": self.statusCode, "message": message, "description": description}})
