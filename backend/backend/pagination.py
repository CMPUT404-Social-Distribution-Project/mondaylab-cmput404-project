from rest_framework import pagination
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from django.core.paginator import InvalidPage

class CustomPagination(pagination.PageNumberPagination):
    page_size = 5
    page_size_query_param = "size"
    max_page_size = 100
    page_query_param = "page"

    def get_paginated_response(self, data):
        print("hereee??")
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
    page_number = 1

    def get_paginated_response(self, data):
        return Response(
            {
                "page" : self.page.number,
                "size" : self.page_size,
                "results" : data
            }
        )

    def paginate_queryset(self, queryset, view=None):
        """
        Paginate a queryset if required, either returning a
        page object, or `None` if pagination is not configured for this view.
        """
        page_size = self.page_size

        paginator = self.django_paginator_class(queryset, page_size)

        try:
            self.page = paginator.page(self.page_number)
        except InvalidPage as exc:
            msg = self.invalid_page_message.format(
                page_number=self.page_number, message=str(exc)
            )
            raise NotFound(msg)

        if paginator.num_pages > 1 and self.template is not None:
            # The browsable API should display pagination controls.
            self.display_page_controls = True

        return list(self.page)