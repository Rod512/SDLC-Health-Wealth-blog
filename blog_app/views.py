import os
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from django.conf import settings
from rest_framework import status
from .models import Blog
from category.models import Categories
from account.models import User
from .serializer import BlogSerializer
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def post_blog(request):
    if 'image' not in request.FILES:
        return Response({'error': 'No image file provided.'}, status=status.HTTP_400_BAD_REQUEST)
    

    title = request.data.get('title')
    content = request.data.get('content')
    category_name = request.data.get('category')
    author_id = request.data.get('author')
    tags = request.data.getlist('tags')
    image_file = request.FILES['image']
    file_path = os.path.join(settings.MEDIA_ROOT, image_file.name)

    

    try:
        category = Categories.objects.get(name=category_name)

    except Categories.DoesNotExist:
        return Response({'Message': "Category not found"}, status=400)
    
    try :
        user = User.objects.get(id=author_id)

    except User.DoesNotExist:
        return Response({'message': 'User not found'}, status=404)


    

    with open(file_path, 'wb+') as destination:
        for chunk in image_file.chunks():
            destination.write(chunk)

    blog = Blog.objects.create(
        title=title,
        content=content,
        category=category,
        author = user,
        tags=tags,
        filename=image_file.name  
    )

    image_url = request.build_absolute_uri(settings.MEDIA_URL + 'blog_images/' + image_file.name)

    return Response({
        'message': 'Blog created successfully!',
        'blog': {
            'title': blog.title,
            'filename': blog.filename,
            'image_url': image_url,
            'created_at' : blog.created_at,
            'category_name' : category.name,
            'author_id' : author_id,
            'author_name' : user.name

        }
    }, status=status.HTTP_201_CREATED)