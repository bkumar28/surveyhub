from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size = 10

    def get_paginated_response(self, data):
        return Response({
            "status": "success",
            "code": status.HTTP_200_OK,
            'data': {
                'count': self.page.paginator.count,
                'page_size': self.page_size,
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'results': data
            }
        })