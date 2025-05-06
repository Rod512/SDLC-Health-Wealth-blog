from django.urls import path
from . import views

urlpatterns = [
    path("post_blog/", views.post_blog, name="post_blog")
    
]
