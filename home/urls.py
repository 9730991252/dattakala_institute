from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('office_login/', views.office_login, name='office_login'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('parent_login/', views.parent_login, name='parent_login'),
    path('teacher_login/', views.teacher_login, name='teacher_login'),
    path('logout/', views.logout, name='logout'),
]