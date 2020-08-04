from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars', default='')

    class Meta:
        db_table = 'accounts_user_settings'
