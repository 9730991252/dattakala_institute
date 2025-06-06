from dattakala_institute.includes import *
from django.utils import timezone
from datetime import datetime, timedelta
# Create your views here.
def admin_home(request):
    if request.session.has_key('admin_mobile'):
        mobile = request.session['admin_mobile']
        a = Admin_detail.objects.filter(mobile=mobile).first()
        context={
            'a':a,
        }
        return render(request, 'admin_home.html', context)
    else:
        return redirect('/')
    
def admin_student_hostel(request):
    if request.session.has_key('admin_mobile'):
        mobile = request.session['admin_mobile']
        a = Admin_detail.objects.filter(mobile=mobile).first()
        context={
            'a':a,
        }
        return render(request, 'admin_student_hostel.html', context)
    else:
        return redirect('/')
    
def todays_appointment(request):
    if request.session.has_key('admin_mobile'):
        mobile = request.session['admin_mobile']
        a = Admin_detail.objects.filter(mobile=mobile).first()
        if 'update_status_running'in request.POST:
            appointment_id = request.POST.get('appointment_id')
            Appointment.objects.filter(id=appointment_id).update(
                meeting_status=1,
                meeting_start_time=datetime.now()
                )
            return redirect("todays_appointment")
        if 'update_status_cancelled'in request.POST:
            appointment_id = request.POST.get('appointment_id')
            Appointment.objects.filter(id=appointment_id).update(meeting_status=3)
            return redirect("todays_appointment")
        if 'update_status_completed'in request.POST:
            appointment_id = request.POST.get('appointment_id')
            Appointment.objects.filter(id=appointment_id).update(
                meeting_status=2,
                meeting_end_time=datetime.now()
                )
            return redirect("todays_appointment")
        todays_appointments = []
        for t in Appointment.objects.filter(book_date_time__date=date.today(), meeting_status=0).order_by('order_by', 'meeting_status'):
            booked_date_time = timezone.localtime(t.book_date_time)
            now = timezone.localtime(timezone.now())  # Make sure both are timezone-aware and in same timezone

            waiting_from = now - booked_date_time


            todays_appointments.append(
                                       {
                                        'id':t.id,
                                        'visitor':t.visitor,
                                        'added_by':t.added_by,
                                        'visit_reason':t.visit_reason,
                                        'book_date_time':t.book_date_time,
                                        'meeting_start_time':t.meeting_start_time,
                                        'meeting_end_time':t.meeting_end_time,
                                        'order_by':t.order_by,
                                        'meat_to':t.meat_to,
                                        'meeting_status':t.meeting_status,
                                        'waiting_from':waiting_from,
                                        'waiting_from_total_seconds':waiting_from.total_seconds()
                                       } 
                                       )
        context={
            'a':a,
            'todays_appointments':todays_appointments
        }
        return render(request, 'todays_appointment.html', context)
    else:
        return redirect('/')
    
def admin_student(request):
    if request.session.has_key('admin_mobile'):
        mobile = request.session['admin_mobile']
        a = Admin_detail.objects.filter(mobile=mobile).first()
        context={
            'a':a,
        }
        return render(request, 'admin_student.html', context)
    else:
        return redirect('/')
    
def admin_account(request):
    if request.session.has_key('admin_mobile'):
        mobile = request.session['admin_mobile']
        a = Admin_detail.objects.filter(mobile=mobile).first()
        context={
            'a':a,
        }
        return render(request, 'admin_account.html', context)
    else:
        return redirect('/')
    
def credit(request):
    if request.session.has_key('admin_mobile'):
        mobile = request.session['admin_mobile']
        a = Admin_detail.objects.filter(mobile=mobile).first()
        context={
            'a':a,
            'accounts':Bank_Account.objects.all(),
        }
        return render(request, 'credit.html', context)
    else:
        return redirect('/')
    
def admin_employee(request):
    if request.session.has_key('admin_mobile'):
        mobile = request.session['admin_mobile']
        a = Admin_detail.objects.filter(mobile=mobile).first()
        context={
            'a':a,
        }
        return render(request, 'admin_employee.html', context)
    else:
        return redirect('/')
    
def admin_student_detail(request, id):
    if request.session.has_key('admin_mobile'):
        mobile = request.session['admin_mobile']
        a = Admin_detail.objects.filter(mobile=mobile).first()
        student = Student.objects.filter(id=id).first()
        student_approval, created = Student_approval.objects.get_or_create(
                student=student,
                batch=a.batch,
                defaults={
                    'store_approved_by': None,
                    'office_approved_by': None,
                    'account_approved_by': None,
                }
            )

        admission_year = []
        current_year = date.today().year
        for i in range(0, 11):
            start_year = current_year - i
            end_year_short = str((current_year - i + 1))[-2:]
            admission_year.append({'year': f'{start_year} - {end_year_short}'})
        student_hostel_fee = Student_Hostel_Fee.objects.filter(batch=a.batch, student=student).first()
        total_fee = 0
        if student_hostel_fee:
            total_fee += int(student_hostel_fee.hostel_fee.amount)
            
        cash_fee = Student_college_fee_received_cash.objects.filter(student=student, added_by__batch=a.batch)
        bank_fee = Student_college_fee_received_bank.objects.filter(student=student, added_by__batch=a.batch)
        received_cash_hostel_fee = Student_Received_Fee_Cash_Hostel.objects.filter(student=student, added_by__batch=a.batch)
        received_bank_hostel_fee = Student_received_Fee_Bank_hostel.objects.filter(student=student, added_by__batch=a.batch)
        paid_fee = int(cash_fee.aggregate(Sum('received_amount'))['received_amount__sum'] or 0) + int(bank_fee.aggregate(Sum('received_amount'))['received_amount__sum'] or 0) +  int(received_cash_hostel_fee.aggregate(Sum('received_amount'))['received_amount__sum'] or 0) +  int(received_bank_hostel_fee.aggregate(Sum('received_amount'))['received_amount__sum'] or 0)
 
        context = {
            'a': a, 
            'remaining_fee':int(total_fee)-int(paid_fee),
            'student':student,
            'colleges':College.objects.filter(batch=a.batch, status=1),
            'branches':Branch.objects.filter(batch=a.batch, status=1),
            'years':Year.objects.filter(batch=a.batch, status=1),
            'student_college_details':Student_college_detail.objects.filter(student=student, batch=a.batch).first(),
            'hostel_fee':Hostel_Fee_installment.objects.filter(batch=a.batch, status=1),
            'student_hostel_fee':Student_Hostel_Fee.objects.filter(student=student, batch=a.batch).first(),
            'student_approval':Student_approval.objects.filter(student=student, batch=a.batch).first(),
            'district':District.objects.filter(status=1).order_by('name'),
            'cast_category':Cast_category.objects.filter(status=1),
            'admission_year':admission_year,
            'total_fee':total_fee,
            'paid_fee':paid_fee,
            'received_cash_hostel_fee':received_cash_hostel_fee,
            'received_bank_hostel_fee':received_bank_hostel_fee,
        }

        return render(request, 'admin_student_detail.html', context)
    else:
        return redirect('/')