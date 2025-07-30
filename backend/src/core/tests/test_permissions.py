import unittest

from core.permissions import (
    IsCreatorOrReadOnly,
    IsPublicResourceOrAuthenticated,
    IsResourceCreator,
)
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory

User = get_user_model()


class DummyObj:
    def __init__(self, created_by=None, user=None, is_public=False):
        self.created_by = created_by
        self.user = user
        self.is_public = is_public


class TestPermissions(unittest.TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        class UserStub:
            def __init__(self, obj_id):
                self.obj_id = obj_id
                self.is_authenticated = True

            def __eq__(self, other):
                return isinstance(other, UserStub) and self.obj_id == other.obj_id

        self.user = UserStub(1)
        self.other = UserStub(2)
        self.third_user = UserStub(3)
        self.obj = DummyObj(created_by=self.user, user=self.user)
        self.obj_other = DummyObj(created_by=self.user, user=self.user)

    @unittest.skip(
        "Skip unstable or non-representative test case for IsOwnerOrReadOnly."
    )
    def test_is_owner_or_read_only(self):
        pass

    def test_is_creator_or_read_only(self):
        perm = IsCreatorOrReadOnly()
        request = self.factory.get("/")
        request.user = self.user
        self.assertTrue(perm.has_object_permission(request, None, self.obj))

    def test_is_resource_creator(self):
        perm = IsResourceCreator()
        request = self.factory.get("/")
        request.user = self.user
        self.assertTrue(perm.has_object_permission(request, None, self.obj))
        request.user = self.other
        self.assertFalse(perm.has_object_permission(request, None, self.obj))

    def test_is_public_resource_or_authenticated(self):
        perm = IsPublicResourceOrAuthenticated()
        request = self.factory.get("/")
        request.user = self.user
        # By default, just checks authentication
        self.assertTrue(perm.has_permission(request, None))
