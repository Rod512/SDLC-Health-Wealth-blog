from django.urls import path
from . import views

urlpatterns = [
    path("post_category/", views.post_category, name="post_category"),
    path("get_category/", views.get_category, name="get_category"),
    path("patch_category/<int:id>/", views.patch_category, name="pacth_category"),
    path("put_category/<int:id>/", views.put_category, name="put_category"),
    path("delete_category/<int:id>/", views.delete_category, name="delete_category"),
]
