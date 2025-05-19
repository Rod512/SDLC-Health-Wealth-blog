from django.db import models
from django.contrib.auth import get_user_model


class Categories(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    class Meta:
        permissions = [
            ("can_edit_category", "Can create/edit/delete Categories"),
        ]

    def __str__(self):
        return self.name