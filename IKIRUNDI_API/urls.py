from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.views.generic import TemplateView
from . import settings

admin.site.site_header = 'IKIRUNDI'
admin.site.index_title = 'Ikibanza Kidasanzwe'
admin.site.site_title = 'Administration'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include('api.urls')),
    re_path("^(?!media)(?!admin)(?!api)(?!static).*$", TemplateView.as_view(template_name='index.html')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)