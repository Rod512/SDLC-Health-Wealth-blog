import os
from rest_framework.decorators import api_view, parser_classes,permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.conf import settings
from rest_framework import status
from .models import Blog
from category.models import Categories
from account.models import User
from .serializer import BlogSerializer
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser

from .permissions import CanViewBlog,IsAdminCanEdit
from account.authentication import JWTauthentication



@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
@authentication_classes([JWTauthentication])
@permission_classes([IsAuthenticated, IsAdminCanEdit])
def post_blog(request):
    title = request.data.get('title')
    content = request.data.get('content')
    category_name = request.data.get('category')
    author_id = request.data.get('author')
    tags = request.data.getlist('tags')
    image = request.FILES.get('image')

    if not image:
        return Response({'error': 'No image file provided.'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        category = Categories.objects.get(name__iexact=category_name)

    except Categories.DoesNotExist:
        return Response({'Message': "Category not found"}, status=400)
    
    try :
        user = User.objects.get(id=author_id)

    except User.DoesNotExist:
        return Response({'message': 'User not found'}, status=404)
    
    blog = Blog.objects.create(
        title=title,
        content=content,
        category=category,
        author = user,
        tags=tags,
        image=image 
    )

    image_url = request.build_absolute_uri(blog.image.url)

    return Response({
        'message': 'Blog created successfully!',
        'blog': {
            'title': blog.title,
            'filename': blog.image.name,
            'image_url': image_url,
            'created_at' : blog.created_at,
            'category_name' : category.name,
            'author_id' : author_id,
            'author_name' : user.name,
            'tags' : tags

        }
    }, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_blogs(request):
    try:
        blogs = Blog.objects.all().order_by('-created_at')
        serializer = BlogSerializer(blogs, many=True, context={"request":request})
        return Response(serializer.data, status=200)
    
    except Exception as e:
        return Response({
            "message": " Sometimes it's not possible to fetch the blogs",
            "details" : str(e)
    })
    
        
        
@api_view(['GET'])
def get_single_blog(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    serializer = BlogSerializer(blog, context={"request":request})
    data = serializer.data
    return Response(data)


@api_view(['PATCH'])
@parser_classes([MultiPartParser, FormParser])
@authentication_classes([JWTauthentication])
@permission_classes([IsAuthenticated, IsAdminCanEdit])
def patch_blog(request, pk):
    try:
        blog = Blog.objects.get(pk=pk)
    except Blog.DoesNotExist:
        return Response({'Response':"Blog does not exist"})
    
    serializer = BlogSerializer(blog, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@parser_classes([MultiPartParser, FormParser])
@authentication_classes([JWTauthentication])
@permission_classes([IsAuthenticated, IsAdminCanEdit])
def put_blog(request, pk):
    try:
        blog = Blog.objects.get(pk=pk)
    except Blog.DoesNotExist:
        return Response({'Response':"Blog does not exist"})
    
    serializer = BlogSerializer(blog, data=request.data,)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@authentication_classes([JWTauthentication])
@permission_classes([IsAuthenticated, IsAdminCanEdit])
def delete_blog(request):
    id = request.data.get("id")
    if not id:
        return Response({"Message": "Blog id not provided"})
    try:
        blog = Blog.objects.get(id=id)
        blog.delete()
        return Response({'message': 'Blog deleted successfully'}, status=200)
    except:
        return Response({"message":"User invalid"})


@api_view(['GET'])
@authentication_classes([ JWTauthentication])
@permission_classes([IsAuthenticated, CanViewBlog])
def blogListView(request):
    blog = Blog.objects.all()
    serializer = BlogSerializer(blog, many=True)
    return Response({'Blog' : serializer.data})


