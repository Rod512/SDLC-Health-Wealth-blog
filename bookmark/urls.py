from django.urls import path
from . import views

urlpatterns = [
    path("save_bookmark/", views.bookmark, name="book_mark"),
    path("get_bookmark/", views.get_bookmark_blog, name="get_bookmark"),
    path("delete_bookmark/", views.delete_bookmark_blog, name="delete_bookmark")
]