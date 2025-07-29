from core.pagination import CustomPagination
from rest_framework.response import Response
from rest_framework.test import APITestCase


class TestCustomPagination(APITestCase):
    def test_get_paginated_response(self):
        paginator = CustomPagination()
        paginator.page = type(
            "Page",
            (),
            {"paginator": type("Paginator", (), {"count": 100})(), "number": 1},
        )()
        paginator.page_size = 10
        paginator.get_next_link = lambda: None
        paginator.get_previous_link = lambda: None
        data = [1, 2, 3]
        response = paginator.get_paginated_response(data)
        self.assertIsInstance(response, Response)
        self.assertEqual(response.data["status"], "success")
        self.assertEqual(response.data["data"]["count"], 100)
        self.assertEqual(response.data["data"]["results"], data)
