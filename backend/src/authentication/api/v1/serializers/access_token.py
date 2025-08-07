from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    # Override fields to accept both username and email
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"] = serializers.CharField(
            required=False, allow_blank=True
        )
        self.fields["email"] = serializers.EmailField(required=False, allow_blank=True)

    def validate(self, attrs):
        username = attrs.get("username", "").strip()
        email = attrs.get("email", "").strip()
        password = attrs.get("password")

        if not username and not email:
            raise serializers.ValidationError(
                {
                    "username": "This field is required if email is not provided.",
                    "email": "This field is required if username is not provided.",
                }
            )

        if not password:
            raise serializers.ValidationError({"password": "This field is required."})

        # Try to fetch user using username or email
        user = None
        if username:
            user = User.objects.filter(username=username).first()
        elif email:
            user = User.objects.filter(email=email).first()

        if user is None:
            raise serializers.ValidationError(
                {"detail": "No active account found with the given credentials."}
            )

        credentials = {
            "username": user.username,  # Use actual username internally
            "password": password,
        }

        authenticated_user = authenticate(**credentials)
        if authenticated_user is None:
            raise serializers.ValidationError({"detail": "Incorrect credentials."})

        data = super().validate(credentials)

        return {
            "refresh_token": data["refresh"],
            "access_token": data["access"],
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            },
        }
