from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user_api/', include("account.urls")),
    path('category_api/', include("category.urls")),
    path('blog_api/', include("blog_app.urls")),
    path('subscriber_api/', include("subscriber.urls"))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
