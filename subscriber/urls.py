from django.urls import path
from . import views

urlpatterns = [
    path("post_subscriber/", views.subscribe, name="post_subscribe"),
    path("get_subscriber/", views.get_subscriber, name="get_subscriber"),
    path("delete_subscriber/", views.delete_subscriber, name="delete_subscriber")
]
