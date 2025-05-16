from rest_framework import serializers
from .models import Bookmark


class BookmarkSerializer(serializers.ModelSerializer):
    blog_name = serializers.ReadOnlyField(source='blog.title')
    class Meta:
        model = Bookmark
        fields = ["user", "blog_name"]