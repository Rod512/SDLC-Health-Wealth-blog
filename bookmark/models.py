from django.db import models
from django.contrib.auth import get_user_model
from blog_app.models import Blog



class Bookmark(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='bookmarks')

    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="bookmarked_by")

    created_at = models.DateTimeField(auto_now_add=True)

