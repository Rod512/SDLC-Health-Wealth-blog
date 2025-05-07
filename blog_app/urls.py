from django.urls import path
from . import views

urlpatterns = [
    path("post_blog/", views.post_blog, name="post_blog"),
    path("get_blogs/", views.get_blogs, name="get_blogs"),
    path("get_blogs/<int:pk>/", views.get_single_blog, name="get_blogs"),
    path('partial_update/<int:pk>/', views.partial_update_blog, name='update_patch'),
    path('update_blog/<int:pk>/', views.update_blog, name='update_put'),
    path('delete_blog/', views.delete_blog, name="delete_blog")
]
