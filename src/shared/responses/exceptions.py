from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError, ParseError
from django.utils.timezone import now

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    error_type = "client_error"
    errors = []

    if isinstance(exc, ValidationError):
        error_type = "validation_error"
        def flatten_errors(error_dict, parent_key=''):
            result = []
            for key, value in error_dict.items():
                full_key = f"{parent_key}.{key}" if parent_key else key
                if isinstance(value, dict):
                    result.extend(flatten_errors(value, full_key))
                elif isinstance(value, list):
                    for msg in value:
                        result.append({"parameter": full_key, "message": str(msg)})
                else:
                    result.append({"parameter": full_key, "message": str(value)})
            return result

        errors = flatten_errors(exc.detail if hasattr(exc, "detail") else {})

    elif isinstance(exc, ParseError):
        error_type = "parse_error"
        errors = [{"parameter": None, "message": str(exc.detail)}]

    elif response and response.data:
        if isinstance(response.data, dict):
            errors = [
                {"parameter": key, "message": str(value)}
                for key, value in response.data.items()
            ]

    if response is not None:
        response.data = {
            "success": False,
            "response": {
                "code": error_type,
                "invalidParameters": errors,
            },
            "timestamp": now().isoformat(),
        }

    return response
