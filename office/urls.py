from django.urls import path
from . import views

urlpatterns = [
    path('office_home/', views.office_home, name='office_home'),
    path('add_college/', views.add_college, name='add_college'),
    path('add_student/', views.add_student, name='add_student'),
    path('add_branch/', views.add_branch, name='add_branch'),
    path('add_year/', views.add_year, name='add_year'),
    path('profile/', views.profile, name='profile'),
    path('student_detail/<id>', views.student_detail, name='student_detail'),
    path('print_student_admission/<id>', views.print_student_admission, name='print_student_admission'),
    path('download_qr_code/', views.download_qr_code, name='download_qr_code'),
    path('address/', views.address, name='address'),
    path('cast_category/', views.cast_category, name='cast_category'),
]