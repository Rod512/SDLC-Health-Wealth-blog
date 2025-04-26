from django.urls import path
from . import views

urlpatterns = [
    path("register_user/", views.create_register_api, name="register"),
    path("get_user/", views.get_registerd_user, name="get_user"),
    path("patch_user/<int:id>/", views.patch_user, name="patch_user"),
    path("delete_user/<int:id>/", views.delete_user, name="delete"),
    path("user_login/", views.user_login, name="login")

]
