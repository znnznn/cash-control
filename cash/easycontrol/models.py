from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as msg
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone


GENDER_CHOICE = (
    ('M', 'Male'),
    ('F', 'Female'),
)

STATUS_CHOICE = (
    ('AC', 'Active'),
    ('P', 'Payed'),
    ('US', 'Unsuccessful'),
)

# Create your models here.
class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model.(not Base)"""
    username = None
    email = models.EmailField(msg('email address'), unique=True)
    phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$")
    mobile = models.CharField(validators=[phoneNumberRegex], max_length=16, unique=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICE, null=True)
    avatar = models.ImageField(upload_to='uploads/image', blank=True, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()


class Organization(models.Model):
    full_name = models.CharField(max_length=500, blank=True, null=True)
    short_name = models.CharField(max_length=500, blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, null=True)
    user_id = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.short_name


class Currency(models.Model):
    currency_name = models.CharField(max_length=500, blank=True, null=True)
    country = models.CharField(max_length=500, blank=True, null=True)
    code = models.CharField(max_length=55, blank=True, null=True)

    def __str__(self):
        return self.currency_name


class CashRegister(models.Model):
    name = models.CharField(max_length=500, blank=True, null=True)
    currency_id = models.ForeignKey(Currency, on_delete=models.SET_NULL, blank=True, null=True)
    organisation_id = models.ForeignKey(Organization, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    user_id = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    debit = models.DecimalField(max_digits=6, decimal_places=2)
    credit = models.DecimalField(max_digits=6, decimal_places=2)
    status = models.CharField(max_length=55, choices=STATUS_CHOICE, default='Active')
    created_at = models.DateField(default=timezone.now)
    cash_register_id = models.ForeignKey(CashRegister, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.description









