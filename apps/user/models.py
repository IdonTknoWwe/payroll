from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import PermissionsMixin,AbstractUser, User
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager

# Create your models here.

class UserManager(BaseUserManager, models.Manager):
    def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
        email = self.normalize_email(email)
        User = self.model(username=username, email=email, is_active=True,
        is_staff=is_staff, is_superuser=is_superuser, **extra_fields)
        User.set_password(password)
        User.save(using=self._db)
        return User

    def create_user(self, username, email, password=None, **extra_fields):
      return self._create_user(username, email, password, False, False,
        **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
      return self._create_user(username, email, password, True, True,
      **extra_fields)

    def get_by_natural_key(self, username):
      return self.get(username=username)

class UserModel(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=False)
    username = models.CharField(null=False, max_length=80, unique=True)
    first_name = models.CharField(null=False, max_length=80)
    last_name = models.CharField(null=False, max_length=80)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __unicode__(self):
        return '%s' %(self.email)

    def get_short_name(self):
        return self.first_name

class PermissionUser(models.Model):

    permission = models.SmallIntegerField(unique=True)
    description = models.CharField(blank=False, max_length=50)

    class Meta:
        verbose_name = "Permiso Usuario"
        verbose_name_plural = "Permiso Usuarios"

    def __unicode__(self):
        return '%s' %(self.description)
