from django.urls import path
from . import views

urlpatterns = [
    path('peon_home/', views.peon_home, name='peon_home'),
    path('book_appointment/', views.book_appointment, name='book_appointment'),
] 