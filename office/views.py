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
    
@csrf_exempt
def student_detail(request, id):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        clerk = Clerk.objects.filter(mobile=mobile).first()
        if not clerk:
            return redirect('office_login')
        student = Student.objects.filter(id=id).first()
        if 'submit_basic_details' in request.POST:
            name = request.POST.get('name')
            student.name = name

            aadhaar_number = request.POST.get('aadhaar')
            if Student.objects.filter(aadhaar_number=aadhaar_number).exclude(id=student.id).exists():
                messages.error(request, 'Aadhaar Number already exists So Skipped!')
                return redirect('student_detail', id=student.id)
            else:
                student.aadhaar_number = aadhaar_number

            dob = request.POST.get('dob')
            student.date_of_birth = dob

            student_mobile = request.POST.get('mobile')
            student.mobile = student_mobile

            address = request.POST.get('address')
            student.address = address

            student.save()
            messages.success(request, 'Student details updated successfully!')
            return redirect('student_detail', id=student.id)
        if 'submit_parent_details'in request.POST:
            father_name = request.POST.get('father_name')
            student.father_name = father_name

            mother_name = request.POST.get('mother_name')
            student.mother_name = mother_name

            parent_mobile = request.POST.get('parent_mobile')
            if len(str(int(parent_mobile))) != 10:
                messages.error(request, 'Parent Mobile number must be 10 digits!')
                return redirect('student_detail', id=student.id)
            student.parent_mobile = parent_mobile

            student.save()
            messages.success(request, 'Parent details updated successfully!')
            return redirect('student_detail', id=student.id)
        if 'submit_college_details'in request.POST:
            college_id = request.POST.get('college_id')
            branch_id = request.POST.get('branch_id')
            year_id = request.POST.get('year_id')
            if Student_college_detail.objects.filter(batch=clerk.batch, student=student).exists():
                sc = Student_college_detail.objects.filter(batch=clerk.batch, student=student).first()
                sc.college_id = college_id
                sc.branch_id = branch_id
                sc.year_id = year_id
                sc.save()
                messages.success(request, 'College details updated successfully!')
                return redirect('student_detail', id=student.id)
            else:
                Student_college_detail(
                    batch=clerk.batch,
                    student=student,
                    college_id=college_id,
                    branch_id=branch_id,
                    year_id=year_id,
                    added_by=clerk
                ).save()
                messages.success(request, 'College details added successfully!')
            return redirect('student_detail', id=student.id)
        if 'submit_hostel_fee_details' in request.POST:
            hostel_fee_id = request.POST.get('hostel_fee_id')
            if Student_Hostel_Fee.objects.filter(batch=clerk.batch, student=student).exists():
                sh = Student_Hostel_Fee.objects.filter(batch=clerk.batch, student=student).first()
                sh.hostel_fee_id = hostel_fee_id
                sh.save()
                messages.success(request, 'Hostel fee updated successfully!')
                return redirect('student_detail', id=student.id)
            else:
                Student_Hostel_Fee(
                    batch=clerk.batch,
                    student=student,
                    hostel_fee_id=hostel_fee_id,
                    added_by=clerk
                ).save()
                messages.success(request, 'Hostel fee added successfully!')

            return redirect('student_detail', id=student.id)
        context={
            'clerk':clerk,
            'student':student,
            'colleges':College.objects.filter(batch=clerk.batch, status=1),
            'branches':Branch.objects.filter(batch=clerk.batch, status=1),
            'years':Year.objects.filter(batch=clerk.batch, status=1),
            'student_college_details':Student_college_detail.objects.filter(student=student, batch=clerk.batch).first(),
            'hostel_fee':Hostel_Fee_installment.objects.filter(batch=clerk.batch, status=1),
            'student_hostel_fee':Student_Hostel_Fee.objects.filter(student=student, batch=clerk.batch).first(),
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
    
def add_college(request):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        clerk = Clerk.objects.filter(mobile=mobile).first()
        if not clerk:
            return redirect('office_login')
        if 'add_college' in request.POST:
            name = request.POST.get('name')
            College.objects.create(
                batch=clerk.batch,
                name=name,
                added_by=clerk
            )
            messages.success(request, 'College added successfully!')
            return redirect('add_college')
        if 'edit_college' in request.POST:
            name = request.POST.get('name')
            college_id = request.POST.get('college_id')
            college = College.objects.filter(id=college_id).first()
            college.name = name
            college.save()
            messages.success(request, 'College updated successfully!')
            return redirect('add_college')
        if 'change_status' in request.POST:
            college_id = request.POST.get('college_id')
            college = College.objects.filter(id=college_id).first()
            if college.status == 1:
                college.status = 0
                messages.success(request, 'College deactivated successfully!')
            else:
                college.status = 1
                messages.success(request, 'College activated successfully!')
            college.save()
            return redirect('add_college')
        context={
            'clerk':clerk,
            'colleges':College.objects.filter(batch=clerk.batch),
        }
        return render(request, 'add_college.html', context)
    else:
        return redirect('office_login')
    
def add_branch(request):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        clerk = Clerk.objects.filter(mobile=mobile).first()
        if not clerk:
            return redirect('office_login')
        if 'add_branch' in request.POST:
            college_id = request.POST.get('college_id')
            name = request.POST.get('name')
            Branch.objects.create(
                batch=clerk.batch,
                college_id=college_id,
                name=name,
                added_by=clerk
            )
            messages.success(request, 'Branch added successfully!')
            return redirect('add_branch')
        if 'edit_branch' in request.POST:
            id = request.POST.get('branch_id')
            name = request.POST.get('name')
            college_id = request.POST.get('college_id')
            branch = Branch.objects.filter(id=id).first()
            branch.name = name
            branch.college_id = college_id
            branch.save()
            messages.success(request, 'Branch updated successfully!')
            return redirect('add_branch')
        if 'change_status' in request.POST:
            branch_id = request.POST.get('branch_id')
            branch = Branch.objects.filter(id=branch_id).first()
            if branch.status == 1:
                branch.status = 0
                messages.success(request, 'Branch deactivated successfully!')
            else:
                branch.status = 1
                messages.success(request, 'Branch activated successfully!')
            branch.save()
            return redirect('add_branch')
        context={
            'clerk':clerk,
            'branch':Branch.objects.filter(batch=clerk.batch),
            'colleges':College.objects.filter(batch=clerk.batch),
        }
        return render(request, 'add_branch.html', context)
    else:
        return redirect('office_login')
    
def add_year(request):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        clerk = Clerk.objects.filter(mobile=mobile).first()
        if not clerk:
            return redirect('office_login')
        if 'add_year' in request.POST:
            name = request.POST.get('name')
            Year.objects.create(
                batch=clerk.batch,
                name=name,
                added_by=clerk
            )
            messages.success(request, 'Year added successfully!')
            return redirect('add_year')
        if 'edit_year' in request.POST:
            id = request.POST.get('year_id')
            name = request.POST.get('name')
            year = Year.objects.filter(id=id).first()
            year.name = name
            year.save()
            messages.success(request, 'Year updated successfully!')
            return redirect('add_year')
        if 'change_status' in request.POST:
            year_id = request.POST.get('year_id')
            year = Year.objects.filter(id=year_id).first()
            if year.status == 1:
                year.status = 0
                messages.success(request, 'Year deactivated successfully!')
            else:
                year.status = 1
                messages.success(request, 'Year activated successfully!')
            year.save()
            return redirect('add_year')
        context={
            'clerk':clerk,
            'years':Year.objects.filter(batch=clerk.batch),
        }
        return render(request, 'add_year.html', context)
    else:
        return redirect('office_login')

