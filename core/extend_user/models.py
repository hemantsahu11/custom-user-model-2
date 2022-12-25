from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from django.utils.translation import gettext_lazy

# Create your models here.

user_type = [  # we can declare this inside model also
    ("Admin", 'create admin user'),
    ("Staff", 'create staff user'),
    ("Demo", 'create demo user')
    # store in db   # displayed to the user
]

# class NewUser(AbstractUser):  # when we are extending the User we have to user AbstractUser while in case of proxy we have to user User model
#
#     class UserType(models.TextChoices):
#         Admin = 'create admin user'
#         Staff = 'create staff user'
#         Demo = 'create user demo'
#
#     age = models.IntegerField(null=True, blank=True)
#     nickname = models.CharField(max_length=50, null=True, blank=True)
#     user_type = models.CharField(max_length=50, choices=UserType.choices, default="Demo")


""" more extended fields and model manager """


class CustomAccountManager(BaseUserManager):

    def create_user(self, email, user_name, first_name, password, **other_fields):   # we are overriding this predefined functions
        if not email:
            raise ValueError(gettext_lazy("You must provide an email address "))

        email = self.normalize_email(email)    # converting email to lowercase
        user = self.model(email=email, user_name=user_name, first_name=first_name, **other_fields)
        user.set_password(password)   # encrypting password
        user.save()
        return user

    def create_superuser(self, email, user_name, first_name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError("Superuser must be assigned to is_staff=True.")
        if other_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must be assigned to is_superuser=True.")

        return self.create_user(email, user_name, first_name, password, **other_fields)


class NewUser(AbstractUser, PermissionsMixin):
    email = models.EmailField(gettext_lazy('email address'), unique=True)
    user_name = models.CharField(max_length=60, unique=True)
    first_name = models.CharField(max_length=60, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    about = models.TextField(gettext_lazy('about'), max_length=200, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = CustomAccountManager()   # overriding existing objects field

    USERNAME_FIELD = 'email'  # by specifying this email will become the username by default username is the default username
    REQUIRED_FIELDS = ['user_name', 'first_name']  # user must enter user_name

    def __str__(self):
        return self.user_name
