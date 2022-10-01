from rest_framework import pagination


class FoodgramPagination(pagination.PageNumberPagination):
    """
    Пажинация с query параметрами limit, page.
    """
    page_size = 10
    page_query_param = 'page'
    page_size_query_param = 'limit'
