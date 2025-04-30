from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user_api/', include("account.urls")),
    path('category_api/', include("category.urls")),
]
