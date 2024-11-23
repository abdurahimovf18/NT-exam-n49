from django.db import models
from django.contrib.auth.models import AbstractUser

from django.utils.translation import gettext_lazy as _

from .managers import UserModelManager


class UserModel(AbstractUser):
    email = models.EmailField(_("Email Address"), max_length=255, unique=True)
    password = models.CharField(_("Password"), max_length=255)
    first_name = models.CharField(_("First Name"), max_length=255)
    last_name = models.CharField(_("Last Name"), max_length=255)

    username = models.CharField(_("Username"), max_length=50, null=True, blank=True)

    created_at = models.DateTimeField(_("Created Time"), auto_now=True)
    updated_at = models.DateTimeField(_("Last Updated Time"), auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("first_name", "last_name", "password")

    objects = UserModelManager()

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
