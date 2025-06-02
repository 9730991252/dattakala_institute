from django.shortcuts import render, redirect, get_object_or_404
from home.models import *
from office.models import *
# from school_admin.models import *
from django.contrib import messages
from datetime import date
from django.db.models import *
from django.db.models import Avg, Sum, Min, Max
from django.db.models import F
import os
import base64
from django.core.files.base import ContentFile

# Create your views here.

# def check_clerk_available_amount(request, batch):
#     clerks = []
#     for c in Clerk.objects.filter(status=1, batch=batch):     
#         available_cash = Student_received_Fee_Cash.objects.filter(added_by=c).aggregate(Sum('received_amount'))['received_amount__sum'] or 0
#         available_cash -= Cash_Transfer_To_Bank.objects.filter(batch=batch, from_clerk=c).aggregate(Sum('amount'))['amount__sum'] or 0
#         available_cash -= Cash_Transfer_To_Admin.objects.filter(batch=batch, from_clerk=c).aggregate(Sum('amount'))['amount__sum'] or 0
#         available_cash -= Expenses.objects.filter(batch=batch, type='cash', added_by=c).aggregate(Sum('amount'))['amount__sum'] or 0
#         if available_cash > 0:
#             clerks.append({
#                 'clerk': c,
#                 'available_cash': available_cash
#             })
#     return clerks

# def check_banks_available_amount(request, batch):
#     banks=[]
#     for b in Bank_Account.objects.filter(status=1):               
#         avalable_cash = Cash_Transfer_To_Bank.objects.filter(batch=batch, to_bank=b).aggregate(Sum('amount'))['amount__sum'] or 0
#         avalable_cash += Student_recived_Fee_Bank.objects.filter(added_by__batch=batch, account=b).aggregate(Sum('recived_amount'))['recived_amount__sum'] or 0
#         banks.append({
#             'bank_name': b.bank_name,
#             'account_number': b.account_number,
#             'avalable_amount': avalable_cash
#         })
#     return banks



def index(request):
    context = {
    }
    return render(request, 'index.html', context)

def self_registration_student(request):
    batch = Batch.objects.filter(start_date__year__lte=date.today().year, end_date__year__gte=date.today().year).first()
    student = ''
    what_to_show_status = 'Form'
    if 'submit_student_detail'in request.POST:
        registration_qr_count = Self_registration_qr_count.objects.filter().first()
        if registration_qr_count:
            registration_qr_count.count += 1
            registration_qr_count.save()
        else:
            Self_registration_qr_count.objects.create(count=1)
            
        name = request.POST.get('name')
        aadhaar_number = request.POST.get('aadhaar_number')
        if len(aadhaar_number) < 12:
            messages.error(request, 'Aadhaar Number should be 12 digits')
            return redirect('/self_registration_student/#home')
        else:
            student = Student.objects.filter(aadhaar_number=aadhaar_number).first()
            if student:
                student_approval = Student_approval.objects.filter(student=student, batch=batch).first() 
                if student_approval:
                    if student_approval.office_approval_status == 0 and student_approval.account_approval_status == 0 and student_approval.store_approval_status == 0:
                        print('yes')
                        pass
                    else:
                        messages.success(request, 'Your Form Is Successfully Submitted. Please Visit to Office!')
                        return redirect('/#home')
            else:
                Student.objects.create(
                    name=name,
                    aadhaar_number=aadhaar_number,
                )
                student = Student.objects.filter(aadhaar_number=aadhaar_number).first()
    if 'submit_student_full_detail'in request.POST:
        # Save in student start
        s_id = request.POST.get('s_id')
        name = request.POST.get('name')
        student_name_as_per_ssc_marksheet = request.POST.get('student_name_as_per_ssc_marksheet')
        aadhaar_number = request.POST.get('aadhaar_number')
        pan_number = request.POST.get('pan_number').upper()
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('date_of_birth')
        blood_group = request.POST.get('blood_group')
        mobile = request.POST.get('mobile')
        parent_mobile = request.POST.get('parent_mobile')
        email = request.POST.get('email')
        address = request.POST.get('address')
        district = request.POST.get('district')
        taluka = request.POST.get('taluka')
        current_address = request.POST.get('current_address')
        father_name = request.POST.get('father_name')
        mother_name = request.POST.get('mother_name')
        mother_mobile = request.POST.get('mother_mobile')
        cast_category = request.POST.get('cast_category')
        whatsapp_number = request.POST.get('whatsapp_number')
        cast = request.POST.get('cast')
        pin_code = request.POST.get('pin_code')
        is_father_alive = request.POST.get('is_father_alive')
        nominee_name = request.POST.get('nominee_name')
        relation_with_nominee = request.POST.get('relation_with_nominee')
        # Save in student end
        # Save in college detail start
        how_to_arrive_college = request.POST.get('come_to_college')
        college_id = request.POST.get('college_id')
        branch_id = request.POST.get('branch_id')
        year_id = request.POST.get('year_id')
        admission_year = request.POST.get('admission_year')
        admission_quota = request.POST.get('admission_quota') 
        current_admission_type = request.POST.get('current_admission_type')
        # Save in college detail end
        student = Student.objects.filter(id=s_id).first()
        if len(mobile) < 10:
            messages.error(request, 'Mobile number should be of 10 digits')
            return redirect('self_registration_student')
        elif len(parent_mobile) < 10:
            messages.error(request, 'Parent mobile number should be of 10 digits')
        elif len(mother_mobile) < 10:
            messages.error(request, 'Mother mobile number should be of 10 digits')
            return redirect('self_registration_student')
        elif len(whatsapp_number) < 10:
            messages.error(request, 'Whatsapp number should be of 10 digits')
            return redirect('self_registration_student')
        elif len(pin_code) < 6:
            messages.error(request, 'Pin Code should be of 6 digits')
            return redirect('self_registration_student')
        elif len(aadhaar_number) < 12:
            messages.error(request, 'Aadhaar number should be of 12 digits')
            return redirect('self_registration_student')
        else:
            if Student.objects.filter(aadhaar_number=aadhaar_number).exclude(id=student.id).exists():
                messages.error(request, 'Student Already Exists with this Aadhaar Number')
                return redirect('student_registration')
            else:
                student.name = name
                student.student_name_as_per_ssc_marksheet = student_name_as_per_ssc_marksheet
                student.mobile = mobile
                student.aadhaar_number = aadhaar_number
                student.gender = gender
                student.address = address
                student.date_of_birth = date_of_birth
                student.father_name = father_name
                student.mother_name = mother_name
                student.parent_mobile = parent_mobile
                student.mother_mobile = mother_mobile
                student.blood_group = blood_group
                student.email = email
                student.current_address = current_address
                student.pan_number = pan_number
                student.nominee_name = nominee_name
                student.relation_with_nominee = relation_with_nominee
                student.district_id = district
                student.taluka_id = taluka
                student.cast_category_id = cast_category
                student.whatsapp_number = whatsapp_number
                student.cast = cast
                student.pin_code = pin_code
                student.is_father_alive = is_father_alive
                student.save()
                student_college_detail = Student_college_detail.objects.filter(student_id=s_id, batch=batch).first()
                if student_college_detail:
                    student_college_detail.batch=batch
                    student_college_detail.student_id = s_id
                    student_college_detail.how_to_arrive_college = how_to_arrive_college
                    student_college_detail.college_id = college_id
                    student_college_detail.branch_id = branch_id
                    student_college_detail.year_id = year_id
                    student_college_detail.admission_year = admission_year
                    student_college_detail.admission_quota = admission_quota
                    student_college_detail.current_admission_type = current_admission_type
                    student_college_detail.save()
                else:
                    student_college_detail = Student_college_detail(
                        batch=batch,
                        student_id=s_id,
                        how_to_arrive_college=how_to_arrive_college,
                        college_id=college_id,
                        branch_id=branch_id,
                        year_id=year_id,
                        admission_year=admission_year,
                        admission_quota=admission_quota,
                        current_admission_type=current_admission_type,
                    )
                    student_college_detail.save()
                student = Student.objects.get(id=s_id)
                what_to_show_status = 'Upload_Image'
                messages.success(request, 'College Details Added Successfully. Now Add Your Image and Conform.')
            
    if student:
        student_college_detail = Student_college_detail.objects.filter(batch=batch, student=student).first()
    else:
        student_college_detail = None
    if 'add_image' in request.POST:
        id = request.POST.get('id')
        img_data = request.POST.get('img')  # base64 string
        student = Student.objects.filter(id=id).first()
        if student.image:
            old_image_path = student.image.path
            if os.path.isfile(old_image_path):
                os.remove(old_image_path)
        format, imgstr = img_data.split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr), name=f'{id}.{ext}')
        student.image.save(f'{student.name}.webp', data, save=True)

        messages.success(request, 'Your Registration is Completed.')
        return redirect('/')
    admission_year = []
    current_year = date.today().year
    for i in range(0, 11):
        start_year = current_year - i
        end_year_short = str((current_year - i + 1))[-2:]
        admission_year.append({'year': f'{start_year} - {end_year_short}'})
    context = {
        'student':student,
        'district':District.objects.filter(status=1).order_by('name'),
        'college':College.objects.filter(batch=batch),
        'years':Year.objects.filter(batch=batch),
        'admission_year':admission_year,
        'cast_category':Cast_category.objects.filter(status=1),
        'what_to_show_status':what_to_show_status,
        'student_college_detail':student_college_detail
        
    }
    return render(request, 'self_registration_student.html', context)

def logout(request):
    if request.session.has_key('admin_mobile'):
        del request.session['admin_mobile']
        
    if request.session.has_key('school_mobile'):
        del request.session['school_mobile']
        
    if request.session.has_key('parent_mobile'):
        del request.session['parent_mobile']
        
    if request.session.has_key('teacher_mobile'):
        del request.session['teacher_mobile']
        
    return redirect('/')

def office_login(request):
    if request.method == "POST":
        batch_id=request.POST ['batch_id']
        number=request.POST ['mobile']
        pin=request.POST ['pin']
        a = Admin_detail.objects.filter(batch_id=batch_id,mobile=number,pin=pin,status=1)
        if a:
            request.session['admin_mobile'] = request.POST["mobile"]
            return redirect('admin_home')
        c= Employee.objects.filter(batch_id=batch_id,mobile=number,secret_pin=pin,status=1)
        if c:
            request.session['office_mobile'] = request.POST["mobile"]
            return redirect('office_home')
        else:
            messages.error(request,f"Mobile Number or Secret Pin invalid.")
            return redirect('/office_login/')
    context = {
        'batch':Batch.objects.all(),
    }
    return render(request, 'office_login.html', context)






def office_logout(request):
    if request.session.has_key('office_mobile'):
        del request.session['office_mobile']
    return redirect('/')