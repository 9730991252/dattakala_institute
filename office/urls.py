from django.urls import path
from . import views

urlpatterns = [
    path('office_home/', views.office_home, name='office_home'),
    path('add_department/', views.add_department, name='add_department'),
    path('add_student/', views.add_student, name='add_student'),
    path('student_detail/<id>', views.student_detail, name='student_detail'),
]