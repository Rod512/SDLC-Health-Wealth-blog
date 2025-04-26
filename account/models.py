from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = None
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    #password = models.CharField(max_length=100)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name

