from django.db import models


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribeOn = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    
