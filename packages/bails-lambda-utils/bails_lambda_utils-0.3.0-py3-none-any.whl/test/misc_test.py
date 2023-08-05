from bails_lambda_utils.misc import is_http_event, safe_get_param


def test_safe_param_handles_no_params():
    assert safe_get_param({}, "yep") is None


def test_safe_param_handles_none_param():
    assert safe_get_param({"queryStringParameters": None}, "yep") is None


def test_safe_param_handles_missing_param():
    assert (
        safe_get_param({"queryStringParameters": {"nope": "almost"}}, "yep")
        is None
    )


def test_safe_param_handles_expected_param():
    assert (
        safe_get_param({"queryStringParameters": {"yep": "y"}}, "yep") == "y"
    )


def test_is_http_event():
    assert is_http_event({"httpMethod": "GET"})


def test_is_not_http_event():
    assert not is_http_event({"records": []})
