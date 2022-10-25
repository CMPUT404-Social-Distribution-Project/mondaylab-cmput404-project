from rest_framework import pagination
from rest_framework.response import Response


class CustomPagination(pagination.PageNumberPagination):
    page_size = 5
    page_size_query_param = "size"
    max_page_size = 100
    page_query_param = "page"

    def get_paginated_response(self, data):
        return Response(
            {
                "page" : self.page.number,
                "size" : self.page.paginator.count,
                "results" : data
            }
        )

class CustomPaginationCommentsSrc(pagination.PageNumberPagination):
    page_size = 5
    page_size_query_param = "size"
    max_page_size = 5
    page_query_param = "page"

    def get_paginated_response(self, data):
        return Response(
            {
                "page" : self.page.number,
                "size" : self.page_size,
                "results" : data
            }
        )
