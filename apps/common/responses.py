"""Success response envelope. The error side lives in exceptions.py, since
DRF renders errors through the exception handler, not a view helper.

Success envelope shape isn't specified in docs/06-api-design.md (only the
error shape is) — {"data": ..., "message": ...} is this project's own
convention, kept deliberately symmetric with the error envelope's
top-level "error" key.
"""

from rest_framework import status
from rest_framework.response import Response


def success_response(data=None, message=None, status_code=status.HTTP_200_OK):
    body = {"data": data}
    if message is not None:
        body["message"] = message
    return Response(body, status=status_code)
