from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework.exceptions import (
    ValidationError,
    NotFound,
    PermissionDenied,
    AuthenticationFailed,
    ParseError,
    APIException
)
from rest_framework import status
from django.http import Http404
from django.core.exceptions import PermissionDenied as DjangoPermissionDenied


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    # Standard error format
    error_response = {
        "message": "",
        "errors": {}
    }

    if response is not None:
        # Map exceptions to messages
        if isinstance(exc, ValidationError):
            error_response["message"] = "Validation failed."
            if isinstance(response.data, dict):
                # Flatten non_field_errors if present
                if "non_field_errors" in response.data:
                    error_response["errors"] = response.data["non_field_errors"]
                else:
                    error_response["errors"] = response.data
            else:
                error_response["errors"] = response.data

        elif isinstance(exc, NotFound) or isinstance(exc, Http404):
            error_response["message"] = "Resource not found."
            if hasattr(exc, "detail"):
                error_response["errors"] = exc.detail
            else:
                error_response["errors"] = str(exc) or "Requested resource does not exist."

        elif isinstance(exc, PermissionDenied) or isinstance(exc, DjangoPermissionDenied):
            error_response["message"] = "You do not have permission to perform this action."
            error_response["errors"] = str(exc.detail if hasattr(exc, 'detail') else str(exc))

        elif isinstance(exc, AuthenticationFailed):
            error_response["message"] = "Authentication failed."
            error_response["errors"] = str(exc.detail)

        elif isinstance(exc, ParseError):
            error_response["message"] = "Malformed request."
            error_response["errors"] = str(exc.detail)

        elif isinstance(exc, APIException):
            error_response["message"] = "An error occurred."
            error_response["errors"] = str(exc.detail)

        else:
            error_response["message"] = "Unexpected error."
            error_response["errors"] = str(exc)

        response.data = error_response

    else:
        # If DRF doesn't handle it, fallback here
        return Response({
            "message": "Internal server error.",
            "errors": str(exc)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response

