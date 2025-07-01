from django.contrib.auth.models import User
from rest_framework import serializers


class UserViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email")
        read_only_fields = fields
