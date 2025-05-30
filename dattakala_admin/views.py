from dattakala_institute.includes import *
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
        context = {
            'a': a,
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
            'admission_year':admission_year
        }

        return render(request, 'admin_student_detail.html', context)
    else:
        return redirect('/')