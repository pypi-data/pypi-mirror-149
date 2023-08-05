import json
from dataclasses import dataclass
from typing import Optional
from .encoders import ModelEncoder


@dataclass
class Response:
    status_code: int
    event: Optional[object] = None
    body: Optional[object] = None
    message: Optional[str] = None
    extra_headers: Optional[object] = None
    disable_cors: Optional[bool] = None

    def to_dict(self):
        res = {"statusCode": self.status_code, "headers": {}}
        if self.body is not None:
            res["body"] = json.dumps(self.body, cls=ModelEncoder)
        elif self.message is not None:
            res["body"] = json.dumps({"message": self.message})
        if self.extra_headers is not None:
            res["headers"] = self.extra_headers
        if not self.disable_cors:
            res["headers"]["Access-Control-Allow-Origin"] = "*"
            res["headers"][
                "Access-Control-Allow-Methods"
            ] = "POST, GET, PUT, OPTIONS"
            res["headers"]["Access-Control-Allow-Headers"] = "*"
            res["headers"]["Access-Control-Expose-Headers"] = "*"
            res["headers"]["Access-Control-Allow-Credentials"] = True
        return res


class NotFoundResponse(Response):
    def __init__(self):
        self.status_code = 404
        self.message = "Not Found"


class ForbiddenResponse(Response):
    def __init__(self, message):
        self.status_code = 403
        self.message = message or "Not Allowed"


class ErrorResponse(Response):
    def __init__(self, message):
        self.status_code = 400
        self.message = message


class RequiredErrorResponse(ErrorResponse):
    def __init__(self, property):
        super().__init__("{0} is required".format(property))


class InternalErrorResponse(Response):
    def __init__(self, reference_id):
        self.status_code = 500
        self.message = (
            "An internal error occurred, if it persists please contact support"
            f" and provide the following id: {reference_id}"
        )
