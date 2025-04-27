from django.urls import path
from . import views

urlpatterns = [
    path("post_category/", views.post_category, name="post_category"),
    path("get_category/", views.get_category, name="get_category")
]
