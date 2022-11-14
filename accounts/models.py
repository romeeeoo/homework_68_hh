from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField


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
        null=True,
        blank=True,
    )
    phone_number = PhoneNumberField(
        blank=False,
        null=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    @receiver(post_save, sender=get_user_model())
    def update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()
