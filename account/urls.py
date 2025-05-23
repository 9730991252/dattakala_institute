from django.urls import path
from . import views
urlpatterns = [
    path('add_bank_account/', views.add_bank_account, name='add_bank_account'),
    path('add_bank_opening_balance/',   views.add_bank_opening_balance, name='add_bank_opening_balance'),
    path('office_account_category/',    views.office_account_category, name='office_account_category'),
    path('student_fees/',    views.student_fees, name='student_fees'),
    path('student_fee_detail/<id>',    views.student_fee_detail, name='student_fee_detail'),
    path('office_expenses/', views.office_expenses, name='office_expenses'),

] 