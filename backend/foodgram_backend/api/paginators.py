from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size_query_param = "limit"


class NoPagination(PageNumberPagination):
    page_size = 10000