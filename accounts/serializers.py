from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()


class AccountSettingsDetailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
