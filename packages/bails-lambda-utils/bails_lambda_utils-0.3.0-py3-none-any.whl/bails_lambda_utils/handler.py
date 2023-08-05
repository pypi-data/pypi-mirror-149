from .errors import RequiredParamException
from .responses import (
    ErrorResponse,
    ForbiddenResponse,
    NotFoundResponse,
    InternalErrorResponse,
)
from functools import wraps
from pynamodb.exceptions import DoesNotExist


def lambda_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except DoesNotExist:
            return NotFoundResponse().to_dict()
        except PermissionError as e:
            return ForbiddenResponse(str(e)).to_dict()
        except RequiredParamException as e:
            return ErrorResponse(str(e)).to_dict()
        except Exception as e:
            # In an ideal world, nothing should ever get to this in production
            # If this gets hit it means this was an exception we were not expecting
            ref = args[1].aws_request_id
            print("{0} {1}".format(ref, str(e)))
            return InternalErrorResponse(ref).to_dict()

    return wrapper
