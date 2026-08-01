"""Custom API exceptions + DRF exception handler enforcing the
{"error": {"code": ..., "message": ...}} envelope from docs/06-api-design.md.
"""

from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler as drf_exception_handler


class ApplicationError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "An unexpected error occurred."
    default_code = "error"


class ConflictError(ApplicationError):
    status_code = status.HTTP_409_CONFLICT
    default_code = "conflict"


class PermissionDeniedError(ApplicationError):
    status_code = status.HTTP_403_FORBIDDEN
    default_code = "permission_denied"


class NotFoundError(ApplicationError):
    status_code = status.HTTP_404_NOT_FOUND
    default_code = "not_found"


def custom_exception_handler(exc, context):
    """Reshapes DRF's default error response into the doc's envelope.

    Single-`detail` exceptions (NotFound, PermissionDenied, our own
    ApplicationError subclasses, ...) become
    {"error": {"code": <exc code>, "message": <text>}}.

    Field-level validation errors (a serializer's {"field": ["msg"]} dict)
    aren't single-message — docs/06-api-design.md doesn't specify how
    these nest, so they're wrapped as
    {"error": {"code": "validation_error", "message": {<field errors>}}}
    rather than flattened, so the field map isn't lost.
    """

    response = drf_exception_handler(exc, context)
    if response is None:
        return None

    if isinstance(response.data, dict) and list(response.data.keys()) == ["detail"]:
        code = exc.get_codes() if hasattr(exc, "get_codes") else "error"
        response.data = {"error": {"code": code, "message": str(response.data["detail"])}}
    else:
        response.data = {"error": {"code": "validation_error", "message": response.data}}

    return response
