from django import template
from django.db.models import Avg, Sum, Min, Max
from math import *
import math
import datetime
from datetime import datetime, date, time

from sunil.models import *
from office.models import * 
from num2words import num2words

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
    for b in Branch.objects.filter(batch_id=batch_id).order_by('college'):
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
    
@register.inclusion_tag('inclusion_tag/college_branches_hostel_student_details_admin.html')
def college_branches_hostel_student_details_admin(batch_id):
    branches = []
    for b in Branch.objects.filter(batch_id=batch_id).order_by('college'):
        year = []
        branch_total_amount = 0
        branch_received = 0
        for y in Year.objects.filter(added_by__batch_id=batch_id):
            male = Student_college_detail.objects.filter(branch=b, year=y, student__gender='Male').count()
            female = Student_college_detail.objects.filter(branch=b, year=y, student__gender='Female' ).count()
            total = Student_college_detail.objects.filter(branch=b, year=y).count()

            s_id = []
            for s in Student_college_detail.objects.filter(branch=b, year=y):
                s_id.append(s.student.id)
                # print(s.student.id, s.student.name)
            year_total_amount = Student_Hostel_Fee.objects.filter(student__id__in=s_id, batch_id=batch_id).aggregate(Sum('hostel_fee__amount'))['hostel_fee__amount__sum'] or 0
            # print(branch_total_amount)
            year_received = Student_received_Fee_Bank_hostel.objects.filter(student__id__in=s_id, batch_id=batch_id).aggregate(Sum('received_amount'))['received_amount__sum'] or 0
            year_received += Student_Received_Fee_Cash_Hostel.objects.filter(student__id__in=s_id, batch_id=batch_id).aggregate(Sum('received_amount'))['received_amount__sum'] or 0
            branch_total_amount += year_total_amount
            branch_received += year_received
            year.append({
                'id': y.id,
                'name': y.name,
                'male': male,
                'female': female,
                'total': total,
                'year_total_amount': year_total_amount,
                'year_received': year_received,
                'year_pending_amount': year_total_amount - year_received,
            })
        branches.append({
            'id': b.id,
            'name': b.name,
            'college':b.college,
            'years':year,
            'male':Student_college_detail.objects.filter(branch=b, student__gender='Male').count(),
            'female':Student_college_detail.objects.filter(branch=b, student__gender='Female').count(),
            'total':Student_college_detail.objects.filter(branch=b).count(),
            'branch_total_amount':branch_total_amount,
            'branch_received':branch_received,
            'pending_amount':branch_total_amount-branch_received,
        })

    all_total_amount = Student_Hostel_Fee.objects.filter(batch_id=batch_id).aggregate(Sum('hostel_fee__amount'))['hostel_fee__amount__sum'] or 0
    all_received = Student_received_Fee_Bank_hostel.objects.filter(batch_id=batch_id).aggregate(Sum('received_amount'))['received_amount__sum'] or 0
    all_received += Student_Received_Fee_Cash_Hostel.objects.filter(batch_id=batch_id).aggregate(Sum('received_amount'))['received_amount__sum'] or 0

    college = []
    for c in College.objects.filter(batch_id=batch_id):
        s_id = []
        for s in Student_college_detail.objects.filter(college=c):
            s_id.append(s.student.id)
        college_total_amount = Student_Hostel_Fee.objects.filter(student__id__in=s_id, batch_id=batch_id).aggregate(Sum('hostel_fee__amount'))['hostel_fee__amount__sum'] or 0
        all_received_college = Student_received_Fee_Bank_hostel.objects.filter(student_id__in=s_id,batch_id=batch_id).aggregate(Sum('received_amount'))['received_amount__sum'] or 0
        all_received_college += Student_Received_Fee_Cash_Hostel.objects.filter(student_id__in=s_id,batch_id=batch_id).aggregate(Sum('received_amount'))['received_amount__sum'] or 0
        college.append({
            'id': c.id,
            'name': c.name,
            'male':Student_college_detail.objects.filter(college=c, student__gender='Male').count(),
            'female':Student_college_detail.objects.filter(college=c, student__gender='Female').count(),
            'total':Student_college_detail.objects.filter(college=c).count(),
            'college_total_amount':college_total_amount,
            'college_received':all_received_college,
            'college_pending_amount':college_total_amount-all_received_college,
        })


    return {
        'all_total_amount':all_total_amount,
        'all_received':all_received,
        'all_pending':all_total_amount-all_received,
        'branches':branches,
        'total_student':Student_Hostel_Fee.objects.filter(batch_id=batch_id).count(),
        'male_student':Student_Hostel_Fee.objects.filter(batch_id=batch_id, student__gender='Male').count(),
        'female_student':Student_Hostel_Fee.objects.filter(batch_id=batch_id, student__gender='Female').count(),
        'college':college,
    } 
    
@register.inclusion_tag('inclusion_tag/hostel_summary_admin.html')
def hostel_summary_admin(batch_id):
    all_total_amount = Student_Hostel_Fee.objects.filter(batch_id=batch_id).aggregate(Sum('hostel_fee__amount'))['hostel_fee__amount__sum'] or 0
    all_received = Student_received_Fee_Bank_hostel.objects.filter(batch_id=batch_id).aggregate(Sum('received_amount'))['received_amount__sum'] or 0
    all_received += Student_Received_Fee_Cash_Hostel.objects.filter(batch_id=batch_id).aggregate(Sum('received_amount'))['received_amount__sum'] or 0
    word_total_amount = num2words(all_total_amount, lang='en_IN').replace(',', '')
    p = all_total_amount-all_received
    
    return {
        'all_total_amount': f'{all_total_amount:,}',
        'all_received': f'{all_received:,}',
        'all_pending': f'{all_total_amount-all_received:,}',
        'total_student':Student_Hostel_Fee.objects.filter(batch_id=batch_id).count(),
        'male_student':Student_Hostel_Fee.objects.filter(batch_id=batch_id, student__gender='Male').count(),
        'female_student':Student_Hostel_Fee.objects.filter(batch_id=batch_id, student__gender='Female').count(),
        'word_total_amount':word_total_amount,
        'word_all_received':num2words(all_received, lang='en_IN').replace(',', ''),
        'word_all_pending':num2words(p, lang='en_IN').replace(',', '')
    }