from django.urls import path
from . import views

urlpatterns = [
    path("post_blogs/", views.post_blog, name="post_blog"),
    path("get_blogs/", views.get_blogs, name="get_blogs"),
    path("get_blogs/<int:pk>/", views.get_single_blog, name="get_blogs"),
    path('patch_blogs/<int:pk>/', views.patch_blog, name='update_patch'),
    path('put_blogs/<int:pk>/', views.put_blog, name='update_put'),
    path('delete_blogs/', views.delete_blog, name="delete_blog")
]
