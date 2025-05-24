from django.urls import path
from . import views

urlpatterns = [
    path('office_home/', views.office_home, name='office_home'),
    path('add_college/', views.add_college, name='add_college'),
    path('add_student/', views.add_student, name='add_student'),
    path('add_branch/', views.add_branch, name='add_branch'),
    path('add_year/', views.add_year, name='add_year'),
    path('student_detail/<id>', views.student_detail, name='student_detail'),
]