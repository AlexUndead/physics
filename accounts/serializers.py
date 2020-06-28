from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()


class AccountSettingsDetailSerializer(serializers.ModelSerializer):
    #user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
