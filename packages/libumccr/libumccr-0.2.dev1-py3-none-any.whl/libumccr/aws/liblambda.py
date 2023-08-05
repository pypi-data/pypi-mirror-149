import copy
import json


def transpose_fn_url_event(event: dict):
    """See Request event payload schema - Amazon API Gateway payload format version 2.0
    https://docs.aws.amazon.com/lambda/latest/dg/urls-invocation.html
    https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html

    :param event:
    :return: transposed Lambda-native event dict or passthrough event as-is
    """
    if not all(k in event.keys() for k in ("version", "routeKey", "headers", "requestContext", "isBase64Encoded")):
        # don't seem to be HTTP request, passing it through
        return event

    http_method = event['requestContext']['http']['method']

    # If request parameter and POST body having the same payload key then we merge them
    # and, POST body payload value take precedence
    payload = {}

    # transpose GET request parameter as Lambda event payload
    if "queryStringParameters" in event.keys():
        payload.update(event['queryStringParameters'])

    # transpose POST request body as Lambda event payload
    if http_method == "POST" and "body" in event.keys():
        body = event['body']
        content_type = event['headers']['content-type']
        # is_base64_encoded = event['isBase64Encoded']

        if "json" in content_type:
            if isinstance(body, str):
                payload.update(json.loads(body))
            else:
                payload.update(body)
        else:
            # If the content type of the request is binary, the body is base64-encoded.
            # Passthrough for now
            return event

    if not payload:
        # We can't seem to transpose the event, passthrough for now
        return event

    return copy.deepcopy(payload)
