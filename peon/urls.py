from django.urls import path
from . import views

urlpatterns = [
    path('peon_home/', views.peon_home, name='peon_home'),
] 