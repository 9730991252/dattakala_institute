from django import template
from django.db.models import Avg, Sum, Min, Max
from math import *
import math
import datetime
from datetime import datetime, date, time

from sunil.models import *
from office.models import *
# from school_admin.models import *
register = template.Library()

# @register.simple_tag()
# def customer_selected_item_count(category_id):
#     return selected_item_category.objects.filter(category_id=category_id,status = 1).count()

# @register.inclusion_tag('inclusion_tag/home/customer_qr_code_cart_orders.html')
# def customer_qr_code_cart_orders(hotel_id):
#     return{'customer_cart':Customer_cart.objects.filter(table__hotel_id=hotel_id)}

# @register.inclusion_tag('inclusion_tag/expenses_details.html')
# def expenses_details(batch_id):
#     print("batch_id", batch_id)
#     credit_debit_category = []
#     for c in Credit_Debit_category.objects.filter(added_by__batch_id=batch_id):
#         total_amount = student_fee.objects.filter(credit_debit_category=c, batch_id=batch_id, student__status=1).aggregate(Sum('amount'))['amount__sum'] or 0
#         received_amount = Student_received_Fee_Bank.objects.filter(credit_debit_category=c, added_by__batch_id=batch_id, student__status=1).aggregate(Sum('received_amount'))['received_amount__sum'] or 0
#         received_amount += Student_received_Fee_Cash.objects.filter(credit_debit_category=c, added_by__batch_id=batch_id, student__status=1).aggregate(Sum('received_amount'))['received_amount__sum'] or 0
#         credit_debit_category.append({
#             'id': c.id, 
#             'name': c.category_name,
#             'total_amount': total_amount,
#             'received_amount': received_amount,
#             'pending_amount': total_amount - received_amount,
            
#         })    
    
#     return {
#         'credit_debit_category': credit_debit_category,
#         'total_amount': sum([c['total_amount'] for c in credit_debit_category]),
#         'received_amount': sum([c['received_amount'] for c in credit_debit_category]),
#         'pending_amount': sum([c['pending_amount'] for c in credit_debit_category]),
#         }
    
@register.inclusion_tag('inclusion_tag/college_branches_student_details_admin.html')
def college_branches_student_details_admin(batch_id):
    branches = []
    for b in Branch.objects.filter(batch_id=batch_id):
        year = []
        for y in Year.objects.filter(added_by__batch_id=batch_id):
            male = Student_college_detail.objects.filter(branch=b, year=y, student__gender='Male').count()
            female = Student_college_detail.objects.filter(branch=b, year=y, student__gender='Female' ).count()
            total = Student_college_detail.objects.filter(branch=b, year=y).count()
            year.append({
                'id': y.id,
                'name': y.name,
                'male': male,
                'female': female,
                'total': total,
            })
        branches.append({
            'id': b.id,
            'name': b.name,
            'college':b.college,
            'years':year,
            'male':Student_college_detail.objects.filter(branch=b, student__gender='Male').count(),
            'female':Student_college_detail.objects.filter(branch=b, student__gender='Female').count(),
            'total':Student_college_detail.objects.filter(branch=b).count(),
        })

    return {
        'branches':branches
    }
    
@register.inclusion_tag('inclusion_tag/hostel_summary_admin.html')
def hostel_summary_admin(batch_id):
    installment = []
    for i in Hostel_Fee_installment.objects.filter(batch_id=batch_id):
        total = Student_Hostel_Fee.objects.filter(hostel_fee=i).aggregate(Sum('hostel_fee__amount'))['hostel_fee__amount__sum'] or 0
        received = Student_received_Fee_Bank_hostel.objects.filter(hostel_fee_installment=i).aggregate(Sum('received_amount'))['received_amount__sum'] or 0
        received += Student_Received_Fee_Cash_Hostel.objects.filter(hostel_fee_installment=i).aggregate(Sum('received_amount'))['received_amount__sum'] or 0
        
        installment.append({
            'id': i.id,
            'name': i.installment_name,
            'amount': i.amount,
            'total_amount':total,
            'received':received,
            'pending':total-received,
            'male_student':Student_Hostel_Fee.objects.filter(hostel_fee=i, student__gender='Male').count(),
            'female_student':Student_Hostel_Fee.objects.filter(hostel_fee=i, student__gender='Female').count(),
            'total_student':Student_Hostel_Fee.objects.filter(hostel_fee=i).count(),
        })
    all_total_amount = Student_Hostel_Fee.objects.filter(batch_id=batch_id).aggregate(Sum('hostel_fee__amount'))['hostel_fee__amount__sum'] or 0
    all_received = Student_received_Fee_Bank_hostel.objects.filter(batch_id=batch_id).aggregate(Sum('received_amount'))['received_amount__sum'] or 0
    all_received += Student_Received_Fee_Cash_Hostel.objects.filter(batch_id=batch_id).aggregate(Sum('received_amount'))['received_amount__sum'] or 0
    return {
        'installment':installment,
        'all_total_amount':all_total_amount,
        'all_received':all_received,
        'all_pending':all_total_amount-all_received,
        'total_student':Student_Hostel_Fee.objects.filter(batch_id=batch_id).count(),
        'male_student':Student_Hostel_Fee.objects.filter(batch_id=batch_id, student__gender='Male').count(),
        'female_student':Student_Hostel_Fee.objects.filter(batch_id=batch_id, student__gender='Female').count(),
    }