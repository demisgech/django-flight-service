from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator,MaxLengthValidator

# Create your models here.


class User(AbstractUser):
    phone_number = models.CharField(
        validators=[MaxLengthValidator(12),MinLengthValidator(10)], unique=True
    )
    email = models.EmailField(unique=True)