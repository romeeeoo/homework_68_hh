from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(
        to=get_user_model(),
        related_name="profile",
        on_delete=models.CASCADE,
        verbose_name="User profile"
    )

    avatar = models.ImageField(
        null=True,
        blank=True,
        upload_to="profile_picture"
    )
    is_corporate = models.BooleanField(
        null=False,
        blank=False,
    )
