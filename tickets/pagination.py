from rest_framework.pagination import PageNumberPagination, CursorPagination


class CostumCursorPagination(CursorPagination):
    page_size = 5
    ordering = '-id'

class TicketPagination(PageNumberPagination):
    page_size = 3 
    max_page_size = 5
    page_size_query_param = 'page_size' # can user manage it in urls