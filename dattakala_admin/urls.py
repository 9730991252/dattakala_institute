from django.urls import path
from . import views

urlpatterns = [
    path('admin_home/', views.admin_home, name='admin_home'),
    path('admin_account/', views.admin_account, name='admin_account'),
    path('credit/', views.credit, name='credit'),
    path('admin_student/', views.admin_student, name='admin_student'),
    path('admin_employee/', views.admin_employee, name='admin_employee'),
    path('admin_notice/', views.admin_notice, name='admin_notice'),
    path('todays_appointment/', views.todays_appointment, name='todays_appointment'),
    path('admin_student_hostel/', views.admin_student_hostel, name='admin_student_hostel'),
    path('admin_student_detail/<id>', views.admin_student_detail, name='admin_student_detail'),
]
