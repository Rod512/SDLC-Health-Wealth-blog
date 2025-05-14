from django.urls import path
from . import views

urlpatterns = [
    path("post_subscriber/", views.subscribe, name="post_subscribe")
]
