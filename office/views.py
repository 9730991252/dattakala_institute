from dattakala_institute.includes import *

# Create your views here.
def office_home(request):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        clerk = Clerk.objects.filter(mobile=mobile).first()
        if not clerk:
            return redirect('office_login')
        messages.success(request, 'Welcome to Dattakala Shikshan Sanstha School!')
        context={
            'clerk':clerk
        }
        return render(request, 'office_home.html', context)
    else:
        return redirect('office_login')
    
def student_detail(request, id):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        clerk = Clerk.objects.filter(mobile=mobile).first()
        if not clerk:
            return redirect('office_login')
        context={
            'clerk':clerk,
            'student':Student.objects.filter(id=id).first(),
        }
        return render(request, 'student_detail.html', context)
    else:
        return redirect('office_login')

def add_student(request):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        clerk = Clerk.objects.filter(mobile=mobile).first()
        if not clerk:
            return redirect('office_login')
        if 'add_student'in request.POST:
            name = request.POST.get('name')
            aadhaar_number = request.POST.get('aadhaar')
            if Student.objects.filter(aadhaar_number=aadhaar_number).exists():
                pass
            else:
                Student.objects.create(name=name, aadhaar_number=aadhaar_number)
            student = Student.objects.filter(aadhaar_number=aadhaar_number).first()
            return redirect('student_detail', id=student.id)
        context={
            'clerk':clerk,

        }
        return render(request, 'add_student.html', context)
    else:
        return redirect('office_login')
    
def add_department(request):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        clerk = Clerk.objects.filter(mobile=mobile).first()
        if not clerk:
            return redirect('office_login')
        if 'add_department' in request.POST:
            name = request.POST.get('name')
            Department.objects.create(
                batch=clerk.batch,
                name=name,
                added_by=clerk
            )
            messages.success(request, 'Department added successfully!')
            return redirect('add_department')
        if 'edit_department' in request.POST:
            name = request.POST.get('name')
            department_id = request.POST.get('department_id')
            department = Department.objects.filter(id=department_id).first()
            department.name = name
            department.save()
            messages.success(request, 'Department updated successfully!')
            return redirect('add_department')
        if 'change_status' in request.POST:
            department_id = request.POST.get('department_id')
            department = Department.objects.filter(id=department_id).first()
            if department.status == 1:
                department.status = 0
                messages.success(request, 'Department deactivated successfully!')
            else:
                department.status = 1
                messages.success(request, 'Department activated successfully!')
            department.save()
            return redirect('add_department')
        context={
            'clerk':clerk,
            'departments':Department.objects.filter(batch=clerk.batch),
        }
        return render(request, 'add_department.html', context)
    else:
        return redirect('office_login')