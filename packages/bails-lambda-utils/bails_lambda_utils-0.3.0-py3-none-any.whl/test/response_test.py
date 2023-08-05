from bails_lambda_utils.responses import Response, RequiredErrorResponse


def test_response_to_dict():
    response = Response(
        status_code=200, body={"id": 200, "something": "simple"}
    )
    real_response = response.to_dict()
    assert real_response["statusCode"] == 200
    assert real_response["body"] == '{"id": 200, "something": "simple"}'


def test_response_to_dict_no_body():
    response = Response(status_code=200)
    real_response = response.to_dict()
    assert "body" not in real_response


def test_response_to_dict_with_extra_headers():
    response = Response(
        status_code=200,
        extra_headers={"extra": "header"},
    )
    real_response = response.to_dict()
    assert real_response["headers"]["extra"] == "header"


def test_response_cors_disabled():
    response = Response(status_code=200, disable_cors=True)
    real_response = response.to_dict()
    assert "Access-Control-Allow-Origin" not in real_response["headers"]
    assert "Access-Control-Allow-Methods" not in real_response["headers"]
    assert "Access-Control-Allow-Headers" not in real_response["headers"]
    assert "Access-Control-Allow-Credentials" not in real_response["headers"]


def test_required_response_error():
    response = RequiredErrorResponse("FooBar")
    real_response = response.to_dict()
    assert real_response["body"] == '{"message": "FooBar is required"}'
