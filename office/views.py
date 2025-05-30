from dattakala_institute.includes import *

# Create your views here.
def office_home(request):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        clerk = Clerk.objects.filter(mobile=mobile).first()
        if not clerk:
            return redirect('office_login')
        
        messages.success(request, f'Welcome {clerk.name}!')
        context={
            'clerk':clerk,
            'self_registration_qr_count':Self_registration_qr_count.objects.filter().first()
        }
        return render(request, 'office_home.html', context)
    else:
        return redirect('office_login')
    
def cast_category(request):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        clerk = Clerk.objects.filter(mobile=mobile).first()
        if not clerk:
            return redirect('office_login')
        if 'add_cast_category'in request.POST:
            name = request.POST.get('name').upper()
            if Cast_category.objects.filter(name=name).exists():
                messages.error(request, 'Cast Category already exists!')
            else:
                Cast_category.objects.create(
                    name=name,
                    created_by=clerk,
                    )
                messages.success(request, 'Cast Category added successfully!')
            return redirect('cast_category')
        if 'edit_cast_category'in request.POST:
            cast_category_id = request.POST.get('cast_category_id')
            name = request.POST.get('name').upper()
            if Cast_category.objects.filter(name=name).exclude(id=cast_category_id).exists():
                messages.error(request, 'Cast Category already exists!')
            else:
                Cast_category.objects.filter(id=cast_category_id).update(
                    name=name,
                ) 
                messages.success(request, 'Cast Category updated successfully!')
            return redirect('cast_category')
        if 'change_cast_category'in request.POST:
            cast_category_id = request.POST.get('cast_category_id')
            cast_category = Cast_category.objects.get(id=cast_category_id)
            cast_category.status = 1 if cast_category.status == 0 else 0
            cast_category.save()
            messages.success(request, 'Cast Category status updated successfully!')
            return redirect('cast_category')
        context={
            'clerk':clerk,
            'cast_category':Cast_category.objects.all(),
        }
        return render(request, 'cast_category.html', context)
    else:
        return redirect('office_login')
    
def address(request):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        clerk = Clerk.objects.filter(mobile=mobile).first()
        if not clerk:
            return redirect('office_login')
        if 'add_district'in request.POST:
            name = request.POST.get('name').upper()
            if District.objects.filter(name=name).exists():
                messages.error(request, 'District already exists!')
            else:
                District.objects.create(
                    name=name,
                    created_by=clerk,
                    )
                messages.success(request, 'District added successfully!')
            return redirect('address')
        if 'add_taluka'in request.POST:
            name = request.POST.get('name').upper()
            district = request.POST.get('district')
            if Taluka.objects.filter(name=name).exists():
                messages.error(request, 'Taluka already exists!')
            else:
                Taluka.objects.create(
                    name=name,
                    district_id=district,
                    created_by=clerk,
                    )
                messages.success(request, 'Taluka added successfully!')
        if 'edit_district'in request.POST:
            district_id = request.POST.get('district_id')
            name = request.POST.get('name').upper()
            if District.objects.filter(name=name).exclude(id=district_id).exists():
                messages.error(request, 'District already exists!')
            else:
                District.objects.filter(id=district_id).update(
                    name=name,
                )
                messages.success(request, 'District updated successfully!')
            return redirect('address')
        if 'edit_taluka'in request.POST:
            taluka_id = request.POST.get('taluka_id')
            name = request.POST.get('name').upper()
            district = request.POST.get('district')
            if Taluka.objects.filter(name=name).exclude(id=taluka_id).exists():
                messages.error(request, 'Taluka already exists!')
            else:
                Taluka.objects.filter(id=taluka_id).update(
                    name=name,
                    district_id=district,
                )
                messages.success(request, 'Taluka updated successfully!')
            return redirect('address')
        if 'change_district_status'in request.POST:
            district_id = request.POST.get('district_id')
            district = District.objects.get(id=district_id)
            district.status = 1 if district.status == 0 else 0
            district.save()
            messages.success(request, 'District status updated successfully!')
            return redirect('address')
        if 'change_taluka_status'in request.POST:
            taluka_id = request.POST.get('taluka_id')
            taluka = Taluka.objects.get(id=taluka_id)
            taluka.status = 1 if taluka.status == 0 else 0
            taluka.save()
            messages.success(request, 'Taluka status updated successfully!')
            return redirect('address')
        context={
            'clerk':clerk,
            'districts':District.objects.all().order_by('name'),
            'taluka':Taluka.objects.all().order_by('name').order_by('district'),
        }
        return render(request, 'address.html', context)
    else:
        return redirect('office_login')
    
def download_qr_code(request):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        clerk = Clerk.objects.filter(mobile=mobile).first()
        if not clerk:
            return redirect('office_login')
        
        context={
            'clerk':clerk
        }
        return render(request, 'download_qr_code.html', context)
    else:
        return redirect('office_login')
    
def profile(request):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        clerk = Clerk.objects.filter(mobile=mobile).first()
        if not clerk:
            return redirect('office_login')
        if 'change_profile'in request.POST:
            name = request.POST.get('name')
            secret_pin = request.POST.get('secret_pin')
            clerk.name = name
            clerk.secret_pin = secret_pin
            clerk.save()
            messages.success(request, 'Profile Updated Successfully!')
            return redirect('profile')
        context={
            'clerk':clerk
        }
        return render(request, 'profile.html', context)
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
            student_name_as_per_ssc_marksheet = request.POST.get('student_name_as_per_ssc_marksheet')
            aadhaar_number = request.POST.get('aadhaar_number')
            pan_number = request.POST.get('pan_number').upper()
            gender = request.POST.get('gender')
            date_of_birth = request.POST.get('date_of_birth')
            blood_group = request.POST.get('blood_group')
            mobile = request.POST.get('mobile')
            email = request.POST.get('email')
            address = request.POST.get('address')
            district = request.POST.get('district')
            taluka = request.POST.get('taluka')
            current_address = request.POST.get('current_address')
            cast_category = request.POST.get('cast_category')
            whatsapp_number = request.POST.get('whatsapp_number')
            cast = request.POST.get('cast')
            pin_code = request.POST.get('pin_code')
            # Save in student end

            if len(mobile) < 10:
                messages.error(request, 'Mobile number should be of 10 digits')
                return redirect('student_registration')
            elif len(whatsapp_number) < 10:
                messages.error(request, 'Whatsapp number should be of 10 digits')
                return redirect('student_registration')
            elif len(pan_number) < 10:
                messages.error(request, 'Pan number should be of 10 digits')
                return redirect('student_registration')
            elif len(pin_code) < 6:
                messages.error(request, 'Pin Code should be of 6 digits')
                return redirect('student_registration')
            elif len(aadhaar_number) < 12:
                messages.error(request, 'Aadhaar number should be of 12 digits')
                return redirect('student_registration')
            else:
                if Student.objects.filter(aadhaar_number=aadhaar_number).exclude(id=student.id).exists():
                    messages.error(request, 'Student Already Exists with this Aadhaar Number')
                    return redirect('student_registration')
                else:
                    student.updated_date = datetime.now()
                    student.updated_by = clerk
                    student.name = name
                    student.student_name_as_per_ssc_marksheet = student_name_as_per_ssc_marksheet
                    student.mobile = mobile
                    student.aadhaar_number = aadhaar_number
                    student.gender = gender
                    student.address = address
                    student.date_of_birth = date_of_birth
                    student.blood_group = blood_group
                    student.email = email
                    student.current_address = current_address
                    student.pan_number = pan_number
                    student.district_id = district
                    student.taluka_id = taluka
                    student.cast_category_id = cast_category
                    student.whatsapp_number = whatsapp_number
                    student.cast = cast
                    student.pin_code = pin_code
                    student.save()
                    messages.success(request, 'Student Basic Details Added Successfully')
                return redirect('student_detail', id=student.id)
        if 'submit_parent_details'in request.POST:
            parent_mobile = request.POST.get('parent_mobile')
            father_name = request.POST.get('father_name')
            mother_name = request.POST.get('mother_name')
            mother_mobile = request.POST.get('mother_mobile')
            is_father_alive = request.POST.get('is_father_alive')
            if len(parent_mobile) < 10:
                messages.error(request, 'Parent mobile number should be of 10 digits')
            elif len(mother_mobile) < 10:
                messages.error(request, 'Mother mobile number should be of 10 digits')
            else:
                student.parent_mobile = parent_mobile
                student.father_name = father_name
                student.mother_name = mother_name
                student.mother_mobile = mother_mobile
                student.is_father_alive = is_father_alive
                student.updated_date = datetime.now()
                student.updated_by = clerk
                student.save()
                messages.success(request, 'Parent Details Added Successfully')
            return redirect('student_detail', id=student.id)
        if 'submit_college_details'in request.POST:
            how_to_arrive_college = request.POST.get('come_to_college')
            college_id = request.POST.get('college_id')
            branch_id = request.POST.get('branch_id')
            year_id = request.POST.get('year_id')
            admission_year = request.POST.get('admission_year')
            admission_quota = request.POST.get('admission_quota') 
            current_admission_type = request.POST.get('current_admission_type')
            student_college_detail = Student_college_detail.objects.filter(student=student, batch=clerk.batch).first()
            if student_college_detail:
                student_college_detail.updated_date = datetime.now()
                student_college_detail.updated_by = clerk
                student_college_detail.batch=clerk.batch
                student_college_detail.student = student
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
                    batch=clerk.batch,
                    student=student,
                    how_to_arrive_college=how_to_arrive_college,
                    college_id=college_id,
                    branch_id=branch_id,
                    year_id=year_id,
                    admission_year=admission_year,
                    admission_quota=admission_quota,
                    current_admission_type=current_admission_type,
                    added_by=clerk
                )
                student_college_detail.save()
            messages.success(request, 'College details added successfully!')
            return redirect('student_detail', id=student.id)
        if 'submit_hostel_fee_details' in request.POST:
            hostel_fee_id = request.POST.get('hostel_fee_id')
            form_number = request.POST.get('form_number')
            if Student_Hostel_Fee.objects.filter(batch=clerk.batch, student=student).exists():
                sh = Student_Hostel_Fee.objects.filter(batch=clerk.batch, student=student).first()
                sh.hostel_fee_id = hostel_fee_id
                sh.form_number = form_number
                sh.form_issued_by = clerk
                sh.updated_date = datetime.now()
                sh.form_issued_date = date.today()  
                sh.updated_by = clerk  
                sh.save()
                messages.success(request, 'Hostel fee updated successfully!')
                return redirect('student_detail', id=student.id)
            else:
                Student_Hostel_Fee(
                    batch=clerk.batch,
                    student=student,
                    form_number=form_number,
                    form_issued_date=date.today(),
                    form_issued_by=clerk,
                    hostel_fee_id=hostel_fee_id,
                    added_by=clerk
                ).save()
                messages.success(request, 'Hostel fee added successfully!')

            return redirect('student_detail', id=student.id)
        student_approval, created = Student_approval.objects.get_or_create(
                student=student,
                batch=clerk.batch,
                defaults={
                    'store_approved_by': None,
                    'office_approved_by': None,
                    'account_approved_by': None,
                }
            )

            # --- Handle Store Approval ---
        if 'submit_store_student_approval' in request.POST:
            approve_status = int(request.POST.get('approve_status'))
            reject_reason = request.POST.get('reject_Reason', '')

            student_approval.store_approval_status = approve_status
            student_approval.store_rejected_reason = reject_reason if approve_status == 2 else None
            student_approval.store_approved_by = clerk
            student_approval.store_approved_date = datetime.now()
            student_approval.save()

            messages.success(request, "Store approval status updated successfully!")
            return redirect('student_detail', id=student.id)

        # --- Handle Office Approval ---
        if 'submit_office_student_approval' in request.POST:
            approve_status = int(request.POST.get('approve_status'))
            reject_reason = request.POST.get('reject_Reason', '')

            student_approval.office_approval_status = approve_status
            student_approval.office_rejected_reason = reject_reason if approve_status == 2 else None
            student_approval.office_approved_by = clerk
            student_approval.office_approved_date = datetime.now()
            student_approval.save()

            messages.success(request, "Office approval status updated successfully!")
            return redirect('student_detail', id=student.id)

        # --- Handle Account Approval ---
        if 'submit_account_student_approval' in request.POST:
            approve_status = int(request.POST.get('approve_status'))
            reject_reason = request.POST.get('reject_Reason', '')

            student_approval.account_approval_status = approve_status
            student_approval.account_rejected_reason = reject_reason if approve_status == 2 else None
            student_approval.account_approved_by = clerk
            student_approval.account_approved_date = datetime.now()
            student_approval.save()

            messages.success(request, "Account approval status updated successfully!")
            return redirect('student_detail', id=student.id)
        admission_year = []
        current_year = date.today().year
        for i in range(0, 11):
            start_year = current_year - i
            end_year_short = str((current_year - i + 1))[-2:]
            admission_year.append({'year': f'{start_year} - {end_year_short}'})
        context={
            'clerk':clerk,
            'student':student,
            'colleges':College.objects.filter(batch=clerk.batch, status=1),
            'branches':Branch.objects.filter(batch=clerk.batch, status=1),
            'years':Year.objects.filter(batch=clerk.batch, status=1),
            'student_college_details':Student_college_detail.objects.filter(student=student, batch=clerk.batch).first(),
            'hostel_fee':Hostel_Fee_installment.objects.filter(batch=clerk.batch, status=1),
            'student_hostel_fee':Student_Hostel_Fee.objects.filter(student=student, batch=clerk.batch).first(),
            'student_approval':Student_approval.objects.filter(student=student, batch=clerk.batch).first(),
            'district':District.objects.filter(status=1).order_by('name'),
            'cast_category':Cast_category.objects.filter(status=1),
            'admission_year':admission_year
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
                Student.objects.create(name=name, aadhaar_number=aadhaar_number, added_by=clerk)
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
            college.updated_date = datetime.now()
            college.updated_by = clerk
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
            branch.updated_date = datetime.now()
            branch.updated_by = clerk
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
            year.updated_date = datetime.now()
            year.updated_by = clerk
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

