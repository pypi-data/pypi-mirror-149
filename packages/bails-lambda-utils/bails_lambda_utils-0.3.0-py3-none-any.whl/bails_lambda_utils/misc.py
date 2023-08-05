def safe_get_param(event, param_key):
    return (
        event["queryStringParameters"][param_key]
        if "queryStringParameters" in event
        and event["queryStringParameters"] is not None
        and param_key in event["queryStringParameters"]
        else None
    )


def is_http_event(event):
    return "httpMethod" in event
