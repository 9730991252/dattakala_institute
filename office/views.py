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

def add_student(request):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        clerk = Clerk.objects.filter(mobile=mobile).first()
        if not clerk:
            return redirect('office_login')
        return_name = ''
        return_mobile = ''
        return_aadhar_number = ''
        return_address = ''
        if 'Add_Student'in request.POST:
            name = request.POST.get('name').lower()
            mobile = request.POST.get('mobile')
            aadhar_number = request.POST.get('aadhar_number')
            pin = request.POST.get('pin')
            gender = request.POST.get('gender')
            address = request.POST.get('address')
            date_of_birth = request.POST.get('date_of_birth')
            if name == '':
                messages.error(request, 'Please enter Student name!')
            elif address == '':
                messages.error(request, 'Please enter Student address!')
            elif mobile == '':
                messages.error(request, 'Please enter Parent mobile number!')
            elif date_of_birth == '':
                messages.error(request, 'Please enter date_of_birth number!')

            elif aadhar_number == '' :
                messages.error(request, 'Please enter Student Aadhar_number number!')
            elif int(aadhar_number) < 12:
                messages.error(request, 'Please enter Student Aadhar_number 12 digit!')
            elif gender == '':
                messages.error(request, 'Please Select Student gender!')
                

            elif Student.objects.filter(aadhar_number=aadhar_number).exists():
                messages.error(request, 'This Student is already registered!')
            else:
                Student(
                    name=name,
                    address=address,
                    mobile=mobile,
                    aadhar_number=aadhar_number,
                    secret_pin=pin or str('0000'),
                    gender=gender,
                    added_by=clerk,
                    date_of_birth=date_of_birth
                ).save()
                messages.success(request, 'Student added successfully!')
                return redirect('add_student')
            return_name = name
            return_address = address
            return_mobile = mobile
            return_aadhar_number = aadhar_number
        if 'edit_student' in request.POST:
            student_id = request.POST.get('student_id')
            name = request.POST.get('name').lower()
            address = request.POST.get('address')
            mobile = request.POST.get('mobile')
            aadhar_number = request.POST.get('aadhar_number')
            pin = request.POST.get('pin')
            gender = request.POST.get('gender')
            date_of_birth = request.POST.get('date_of_birth')
            if name == '':
                messages.error(request, 'Please enter Student name!')
            elif address == '':
                messages.error(request, 'Please enter Student address!')
            elif mobile == '':
                messages.error(request, 'Please enter Parent mobile number!')

            elif aadhar_number == '':
                messages.error(request, 'Please enter Student Aadhar_number number!')
                
            elif date_of_birth == '':
                messages.error(request, 'Please Select Student date_of_birth!')
                
            elif gender == '':
                messages.error(request, 'Please Select Student gender!')
                
            elif Student.objects.filter(aadhar_number=aadhar_number).exclude(id=student_id).exists():
                messages.error(request, 'This Student is already registered!')
            else:
                Student.objects.filter(id=student_id).update(
                    name=name,
                    address=address,
                    mobile=mobile,
                    aadhar_number=aadhar_number,
                    secret_pin=pin,
                    gender=gender,
                    date_of_birth=date_of_birth
                )
                messages.success(request, 'Student updated successfully!')
                return redirect('add_student')
        if 'active'in request.POST:
            student_id = request.POST.get('id')
            student = Student.objects.get(id=student_id)
            student.status = 0
            student.save()
            return redirect('add_student')
        if 'deactive'in request.POST:
            student_id = request.POST.get('id')
            student = Student.objects.get(id=student_id)
            student.status = 1
            student.save()
            return redirect('add_student')
        if 'test'in request.POST:
            name = request.POST.get('name')
            print(name)
        s = Student.objects.all().order_by('name')[:20]
        context={
            'clerk':clerk,
            'students': s,
            'return_name': return_name,
            'return_mobile': return_mobile,
            'return_aadhar_number': return_aadhar_number,
            'return_address': return_address,
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