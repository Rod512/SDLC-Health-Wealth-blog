from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Bookmark
from blog_app.models import Blog
from .serializer import BookmarkSerializer
from account.authentication import JWTauthentication

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTauthentication])
def bookmark(request):
    id = request.data.get("id")
    try:
        blog = Blog.objects.get(id=id)
    except Blog.DoesNotExist:
        return Response({"Message": "Blog not found"})
    
    user = request.user
    
    bookmark = Bookmark.objects.filter(blog=blog, user=user).first()

    if  bookmark:
        bookmark.delete()
        return Response({"message":"Bookmark Deleted"}, status=200)
    else:
        Bookmark.objects.create(
            user = user,
            blog = blog,
        )
        return Response({
            "message" : "Blog saved",
            "user" : user.name,
            "blog" : blog.title
        }, status=201)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTauthentication])
def get_bookmark_blog(request):
        user = request.user
        bookmark = Bookmark.objects.filter(user=user)
        if not bookmark.exists():
             return Response({
            "message": "no bookmark blog found",
            }, status=400)
        else:
            bookmarkSerializer = BookmarkSerializer(bookmark, many=True)
            return Response({
                "message": "All bookmarked blogs",
                "blog": bookmarkSerializer.data,
                },status=200)

       
    

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTauthentication])
def delete_bookmark_blog(request):
    id = request.data.get("id")
    try:
        blog = Blog.objects.get(id=id)
    except Blog.DoesNotExist:
        return Response({"Message": "Blog not found"})
    
    user = request.user
    
    bookmark = Bookmark.objects.filter(blog=blog, user=user).first()

    if  bookmark:
        bookmark.delete()
        return Response({"message":"Bookmark Deleted"}, status=200)



