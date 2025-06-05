from django import template
from django.db.models import Avg, Sum, Min, Max
from math import *
import math
import datetime
from datetime import datetime, date, time

from sunil.models import *
from office.models import * 
from dattakala_admin.models import * 
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
from collections import defaultdict

# This inclusion tag will be used in a Django template to show student counts by branch and year
# It will display: number of male, female, and total students in each branch and year
# It excludes already approved students and those without a form number

@register.inclusion_tag('inclusion_tag/college_branches_student_details_admin.html')
def college_branches_student_details_admin(batch_id):
    # Step 1: Get all student records for the given batch
    # - We exclude students without a form number
    # - We include related student, branch, and year objects for faster access
    student_details = Student_college_detail.objects.filter(
        batch_id=batch_id
    ).exclude(form_number=None).select_related('student', 'branch', 'year')

    # Step 2: Get the IDs of students who are fully approved (by office, account, and store)
    # - These students will be excluded from our count
    approved_ids = set(Student_approval.objects.filter(
        batch_id=batch_id,
        office_approval_status=2,
        account_approval_status=2,
        store_approval_status=2
    ).values_list('student_id', flat=True))

    # Step 3: Prepare two dictionaries to keep track of counts
    year_counts = {}     # Counts by (branch, year)
    branch_counts = {}   # Total counts by branch only

    # Step 4: Loop through each student detail and count based on gender
    for detail in student_details:
        student = detail.student
        if not student or student.id in approved_ids:
            continue  # Skip this student if missing or already approved

        branch = detail.branch
        year = detail.year
        gender = student.gender

        # Get IDs for easy use
        b_id = branch.id
        y_id = year.id if year else None

        # Initialize branch totals if not already done
        branch_counts.setdefault(b_id, {'male': 0, 'female': 0, 'total': 0})

        # Initialize year totals if year is present
        if y_id:
            year_counts.setdefault((b_id, y_id), {'male': 0, 'female': 0, 'total': 0})

        # Count based on gender for branch
        branch_counts[b_id]['total'] += 1
        if gender == 'Male':
            branch_counts[b_id]['male'] += 1
            if y_id:
                year_counts[(b_id, y_id)]['male'] += 1
        elif gender == 'Female':
            branch_counts[b_id]['female'] += 1
            if y_id:
                year_counts[(b_id, y_id)]['female'] += 1

        # Always increase total count for year if year exists
        if y_id:
            year_counts[(b_id, y_id)]['total'] += 1

    # Step 5: Get the list of all branches and years for the current batch
    branches = Branch.objects.filter(batch_id=batch_id).order_by('college')
    years = Year.objects.filter(added_by__batch_id=batch_id)

    # Step 6: Now prepare a clean structure (list of dictionaries) to send to the template
    branches_data = []
    for branch in branches:
        year_data = []
        for year in years:
            # Get the count for this branch and year combination
            stats = year_counts.get((branch.id, year.id), {'male': 0, 'female': 0, 'total': 0})
            
            if int(stats['total']) != 0:
                year_data.append({
                    'id': year.id,
                    'name': year.name,
                    'male': stats['male'],
                    'female': stats['female'],
                    'total': stats['total'],
                })

        # Get the overall total for this branch
        total_stats = branch_counts.get(branch.id, {'male': 0, 'female': 0, 'total': 0})
        if int(total_stats['total']) != 0:
            # Add the final branch data
            branches_data.append({
                'id': branch.id,
                'name': branch.name,
                'college': branch.college,
                'years': year_data,
                'male': total_stats['male'],
                'female': total_stats['female'],
                'total': total_stats['total'],
            })

    # Step 7: Calculate the total number of male, female, and all students in the batch
    total_male = sum(branch['male'] for branch in branch_counts.values())
    total_female = sum(branch['female'] for branch in branch_counts.values())
    total_students = sum(branch['total'] for branch in branch_counts.values())
    

    # Step 8: Return all the data to the Django template
    return {
        'branches': branches_data,     # List of all branches with year-wise and gender-wise counts
        'total': total_students,       # Total number of students (excluding approved ones)
        'male': total_male,            # Total male students
        'female': total_female,        # Total female students
        'batch_id': batch_id,          # Current batch ID (can be used in template logic)
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
        'batch_id':batch_id,
            
        })


    return {
        'all_total_amount':all_total_amount,
        'all_received':all_received,
        'all_pending':all_total_amount-all_received,
        'branches':branches,
        'total_student':Student_Hostel_Fee.objects.filter(batch_id=batch_id).exclude(student__approval_status=2).count(),
        'male_student':Student_Hostel_Fee.objects.filter(batch_id=batch_id, student__gender='Male').exclude(student__approval_status=2).count(),
        'female_student':Student_Hostel_Fee.objects.filter(batch_id=batch_id, student__gender='Female').exclude(student__approval_status=2).count(),
        'college':college,
        'batch_id':batch_id,
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
    
@register.inclusion_tag('inclusion_tag/district_taluka_student_details_admin.html')
def district_taluka_student_details_admin(batch_id):
    from operator import itemgetter

    districts = []

    # Loop through each district
    for d in District.objects.all():
        # Total students (excluding fully approved ones)
        total_student = Student_college_detail.objects.filter(student__district=d).exclude(form_number=None).count()
        total_student -= Student_approval.objects.filter(
            batch_id=batch_id,
            student__district=d,
            office_approval_status=2,
            account_approval_status=2,
            store_approval_status=2
        ).count()

        male_student = Student_college_detail.objects.filter(student__district=d, student__gender='Male').exclude(form_number=None).count()
        male_student -= Student_approval.objects.filter(
            batch_id=batch_id,
            student__gender='Male',
            student__district=d,
            office_approval_status=2,
            account_approval_status=2,
            store_approval_status=2
        ).count()

        female_student = Student_college_detail.objects.filter(student__district=d, student__gender='Female').exclude(form_number=None).count()
        female_student -= Student_approval.objects.filter(
            batch_id=batch_id,
            student__gender='Female',
            student__district=d,
            office_approval_status=2,
            account_approval_status=2,
            store_approval_status=2
        ).count()

        if total_student > 0:
            taluka_list = []

            # Loop through each taluka under this district
            for t in Taluka.objects.filter(district=d):
                taluka_total_student = Student_college_detail.objects.filter(student__taluka=t).exclude(form_number=None).count()
                taluka_total_student -= Student_approval.objects.filter(
                    batch_id=batch_id,
                    student__taluka=t,
                    office_approval_status=2,
                    account_approval_status=2,
                    store_approval_status=2
                ).count()

                taluka_male_student = Student_college_detail.objects.filter(student__taluka=t, student__gender='Male').exclude(form_number=None).count()
                taluka_male_student -= Student_approval.objects.filter(
                    batch_id=batch_id,
                    student__gender='Male',
                    student__taluka=t,
                    office_approval_status=2,
                    account_approval_status=2,
                    store_approval_status=2
                ).count()

                taluka_female_student = Student_college_detail.objects.filter(student__taluka=t, student__gender='Female').exclude(form_number=None).count()
                taluka_female_student -= Student_approval.objects.filter(
                    batch_id=batch_id,
                    student__gender='Female',
                    student__taluka=t,
                    office_approval_status=2,
                    account_approval_status=2,
                    store_approval_status=2
                ).count()

                # Only include taluka if it has students
                if taluka_total_student > 0:
                    taluka_list.append({
                        'name': t.name,
                        'total_student': taluka_total_student,
                        'male_student': taluka_male_student,
                        'female_student': taluka_female_student,
                    })

            # Sort taluka list by highest total_student
            taluka_list = sorted(taluka_list, key=itemgetter('total_student'), reverse=True)

            # Append district with its sorted talukas
            districts.append({
                'district': d,
                'taluka': taluka_list,
                'total_student': total_student,
                'male_student': male_student,
                'female_student': female_student,
            })

    # Sort district list by highest total_student
    districts = sorted(districts, key=itemgetter('total_student'), reverse=True)

    return {
        'districts': districts
    }

    
@register.inclusion_tag('inclusion_tag/employee_detail_admin.html')
def employee_detail_admin(batch):
    employee = Employee.objects.filter(batch=batch, status=1)
    employee_post = Employee_category.objects.filter(status=1)
    employee_category = []
    for e in employee_post:
        employee_category.append({
            'category':e,
            'total_employee':employee.filter(category=e).count(),
            'male':employee.filter(category=e, gender='Male').count(),
            'female':employee.filter(category=e, gender='Female').count(),
        })
    return {
        'total':employee.count(),
        'male':employee.filter(gender='Male').count(),
        'female':employee.filter(gender='Female').count(),
        'employee_category':employee_category
    }
    
@register.inclusion_tag('inclusion_tag/todayes_appointment_status_summary.html')
def todayes_appointment_status_summary(request):
    todayes_appointment = Appointment.objects.filter(book_date_time__date=date.today())
    return{
        'total_appointment':todayes_appointment.count(),
        'waiting_appointment':todayes_appointment.filter(meeting_status=0).count(),
        'Running_appointment':todayes_appointment.filter(meeting_status=1).count(),
        'completed_appointment':todayes_appointment.filter(meeting_status=2).count(),
        'cancelled_appointment':todayes_appointment.filter(meeting_status=3).count(),
    }