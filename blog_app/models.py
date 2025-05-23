from django.db import models
from category.models import Categories
from account.models import User

class Blog(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to="blog_image/", blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True)
    tags = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
         permissions = [
            ("can_edit_blog", "Can create/edit/delete Blog"),
            ("can_view_blog", "Can view Blog"),
        ]
    def __str__(self):
        return self.title
    



