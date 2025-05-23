from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', include('home.urls')),
    path('sunil/', include('sunil.urls')),
    path('office/', include('office.urls')),
    path('ajax/', include('ajax.urls')),
    path('account/', include('account.urls')),
    # path('teacher/', include('teacher.urls')),
    # path('school_admin/', include('school_admin.urls')),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)