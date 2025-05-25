from django.urls import path
from . import views
urlpatterns = [
    path('search_student_for_edit/', views.search_student_for_edit, name='search_student_for_edit'),
    path('search_student_for_fees/', views.search_student_for_fees, name='search_student_for_fees'),
    path('check_student_aadhaar/', views.check_student_aadhaar, name='check_student_aadhaar'),
    path('get_college_branch/', views.get_college_branch, name='get_college_branch'),
    path('search_student_for_new_admission/', views.search_student_for_new_admission, name='search_student_for_new_admission'),
]  