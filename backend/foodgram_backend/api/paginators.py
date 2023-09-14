from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size_query_param = "limit"


class NoPagination(PageNumberPagination):
    page_size = 10000


class RecipePagination(PageNumberPagination):
    page_size_query_param = "recipes_limit"
