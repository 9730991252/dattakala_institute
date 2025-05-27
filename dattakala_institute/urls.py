from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', include('home.urls')),
    path('sunil/', include('sunil.urls')),
    path('office/', include('office.urls')),
    path('ajax/', include('ajax.urls')),
    path('account/', include('account.urls')),
    path('dattakala_admin/', include('dattakala_admin.urls')),
    path('report/', include('report.urls')),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)