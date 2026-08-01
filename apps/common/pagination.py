from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    """Default pagination for all list endpoints (docs/06-api-design.md:
    "cursor or limit/offset... default page size 20-50")."""

    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 50
