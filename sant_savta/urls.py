from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('home.urls')),
    path('sunil/', include('sunil.urls')),
    path('office/', include('office.urls')),
    path('ajax/', include('ajax.urls')),
    path('member/', include('member.urls')),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
