from django.urls import path
from . import views

urlpatterns = [
    path('admin_home/', views.admin_home, name='admin_home'),
    path('admin_account/', views.admin_account, name='admin_account'),
    path('credit/', views.credit, name='credit'),
]
