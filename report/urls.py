from django.urls import path
from . import views
urlpatterns = [
path('hostel/', views.hostel, name='hostel'),
path('student/', views.student, name='student'),
path('employee_report/', views.employee_report, name='employee_report'),
]
