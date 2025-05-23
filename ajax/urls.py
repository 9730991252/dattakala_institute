from django.urls import path
from . import views
urlpatterns = [
    path('search_student_for_edit/', views.search_student_for_edit, name='search_student_for_edit'),
    path('search_student_for_fees/', views.search_student_for_fees, name='search_student_for_fees'),
] 