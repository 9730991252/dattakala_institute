from django.urls import path
from . import views
urlpatterns = [
path('hostel/', views.hostel, name='hostel'),
path('student/', views.student, name='student'),
path('employee_report/', views.employee_report, name='employee_report'),
path('hostel_form_summary/', views.hostel_form_summary, name='hostel_form_summary'),
path('download_student_admission_details_college/<id>/', views.download_student_admission_details_college, name='download_student_admission_details_college'),
]
   