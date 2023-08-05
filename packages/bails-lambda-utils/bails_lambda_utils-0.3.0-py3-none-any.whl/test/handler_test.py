from bails_lambda_utils.errors import RequiredParamException
from bails_lambda_utils.handler import lambda_handler
from bails_lambda_utils.responses import Response
from pynamodb.exceptions import DoesNotExist


@lambda_handler
def fake_func(err, message=None):
    raise err(message)


@lambda_handler
def fake_permission_error():
    raise PermissionError()


@lambda_handler
def happy_func():
    return Response(status_code=204).to_dict()


@lambda_handler
def fake_internal_func(_event, _context):
    raise Exception()


class FakeContext:
    aws_request_id = "id"


def test_normal():
    res = happy_func()
    assert res["statusCode"] == 204


def test_handles_dne():
    res = fake_func(DoesNotExist)
    assert res["statusCode"] == 404
    assert res["body"] == '{"message": "Not Found"}'


def test_handles_forbidden():
    res = fake_permission_error()
    assert res["statusCode"] == 403
    assert res["body"] == '{"message": "Not Allowed"}'


def test_handles_forbidden_custom_message():
    res = fake_func(PermissionError, "only admins can see this")
    assert res["statusCode"] == 403
    assert res["body"] == '{"message": "only admins can see this"}'


def test_handles_required():
    res = fake_func(RequiredParamException, "gotta have it")
    assert res["statusCode"] == 400
    assert res["body"] == '{"message": "gotta have it"}'


def test_handles_internal_error():
    res = fake_internal_func(Exception, FakeContext())
    assert res["statusCode"] == 500
    assert "An internal error occurred" in res["body"]
    assert (
        ", if it persists please contact support and provide the following id: id"
        in res["body"]
    )
