from rest_framework import serializers
from .models import Blog

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'

    def get_image_url(self,obj):
        request = self.context.get("request")
        return request.build.absolute_uri(obj.image.url)