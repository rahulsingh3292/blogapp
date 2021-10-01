
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static 
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path("",include("blog_app.urls")),
    path("ckeditor/",include('ckeditor_uploader.urls')),
 
] + static(settings.STATIC_URL,docoument_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL,docoument_root=settings.MEDIA_ROOT)

handler404 = "blog_app.views.page_not_found_404"