from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser


# Create your models here.
class UserManager(BaseUserManager):
    def createUser(self, email, name=None, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError("Email required")
        if not password:
            raise ValueError("Password required")
        user_obj = self.model(
            email=self.normalize_email(email),
            name=name
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.is_active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def createStaff(self, email, name=None, password=None):
        user = self.createUser(
            email,
            name=name,
            password=password,
            is_staff=True
        )
        return user

    def create_superuser(self, email, name=None, password=None):
        user = self.createUser(
            email,
            name=name,
            password=password,
            is_staff=True,
            is_admin=True
        )
        return user


class User(AbstractUser):
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=True)
    admin = models.BooleanField(default=True)

    date_registered = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        if self.name:
            return self.email

    def get_short_name(self):
        return self.email

    def has_perms(self, perm_list, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        if self.is_admin:
            return True
        return self.is_staff

    @property
    def is_admin(self):
        return self.admin
