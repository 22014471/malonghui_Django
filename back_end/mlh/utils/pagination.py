from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 20


class TalksPagination(PageNumberPagination):
    """吐槽列表分页"""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50
