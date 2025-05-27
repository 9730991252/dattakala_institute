from django.urls import path
from . import views
urlpatterns = [
path('hostel/', views.hostel, name='hostel'),
]
