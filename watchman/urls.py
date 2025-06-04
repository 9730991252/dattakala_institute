from django.urls import path
from . import views

urlpatterns = [
    path('watchman_home/', views.watchman_home, name='watchman_home'),
] 