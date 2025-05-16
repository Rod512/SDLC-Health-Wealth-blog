from django.urls import path
from . import views

urlpatterns = [
    path("register_user/", views.create_register_api, name="register"),
    path("get_user/", views.get_registerd_user, name="get_user"),
    path("patch_user/<int:id>/", views.patch_user, name="patch_user"),
    path("put_user/<int:id>/", views.put_user, name="put_user"),
    path("delete_user/", views.delete_user, name="delete"),
    path("user_login/", views.user_login, name="login"),
    path("user_api_view/", views.user_api, name="user_api"),
    path("user_logout/", views.user_logout, name="logout"),
    path("new_token/", views.refresh_view_check, name="new_token"),


]
