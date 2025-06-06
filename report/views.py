from dattakala_institute.includes import *
from home.templatetags.admin_tag import *
import csv
from office.views import check_employee_permissions
# Create your views here.
@check_employee_permissions
def hostel(request):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        clerk = Employee.objects.filter(mobile=mobile).first()
        if not clerk:
            return redirect('office_login')        
        if 'download_excel'in request.POST:
            date_time = datetime.now()
            name = f'excel_reports/Hostel_Fee_Report-{date.today()}-{date_time.hour}-{date_time.minute}-{date_time.second}.csv'
            with open(name, 'w+', newline='', encoding='utf-8') as f:
                lnwriter = csv.writer(f, quoting=csv.QUOTE_ALL)
                
                lnwriter.writerow([
                    'Collage Name',
                    'Branch Name',
                    'Year',
                    'Student Name',
                    'Mobile',
                    'Gender',
                    'Total Fee',
                    'Received Amount',
                    'Pending Amount'
                ])

                for student in Student.objects.all():
                    college = Student_college_detail.objects.filter(batch=clerk.batch, student=student).first()
                    hostel_fee = Student_Hostel_Fee.objects.filter(batch=clerk.batch, student=student).first()
                    
                    total_amount = hostel_fee.hostel_fee.amount if hostel_fee else 0
                    received_amount = Student_received_Fee_Bank_hostel.objects.filter(batch=clerk.batch, student=student).aggregate(Sum('received_amount'))['received_amount__sum'] or 0
                    received_amount += Student_Received_Fee_Cash_Hostel.objects.filter(batch=clerk.batch, student=student).aggregate(Sum('received_amount'))['received_amount__sum'] or 0
                    pending_amount = int(total_amount) - int(received_amount)

                    lnwriter.writerow([
                        college.college.name if college else '',
                        college.branch.name if college else '',
                        college.year.name if college else '',
                        student.name,
                        student.mobile,
                        student.gender,
                        f"{total_amount:,}",
                        f"{received_amount:,}",
                        f"{pending_amount:,}"
                    ])
            return redirect(f'/{name}')
        context={
            'clerk':clerk,
        }
        return render(request, 'report/hostel.html', context)
    else:
        return redirect('office_login')
    
@check_employee_permissions
def student(request):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        clerk = Employee.objects.filter(mobile=mobile).first()
        if not clerk:
            return redirect('office_login')        
        context={
            'clerk':clerk,
        }
        return render(request, 'report/student.html', context)
    else:
        return redirect('office_login')
    
@check_employee_permissions
def hostel_form_summary(request):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        clerk = Employee.objects.filter(mobile=mobile).first()
        if not clerk:
            return redirect('office_login')        
        hostel_form_pending_count = 0
        hostel_form_accepted_count = 0
        hostel_form_account_rejected_count = 0
        for s in Student_Hostel_Fee.objects.filter(batch=clerk.batch).exclude(form_number=None):
            if Student_approval.objects.filter(student=s.student, account_approval_status=0):
                hostel_form_pending_count += 1
            if Student_approval.objects.filter(student=s.student, account_approval_status=1):
                hostel_form_accepted_count += 1
            if Student_approval.objects.filter(student=s.student, account_approval_status=2):
                hostel_form_account_rejected_count += 1
        st = []
        account_rejected_student = []
        status = 1
        students = Student_Hostel_Fee.objects.filter(batch=clerk.batch).exclude(form_number=None)

        for s in students:
            approval = Student_approval.objects.filter(student=s.student, batch=clerk.batch).first()
            if approval.account_approval_status == 0:
                st.append({
                    'id': s.student.id,
                    'name': s.student.name,
                    'mobile': s.student.mobile,
                    'aadhaar_number': str(s.student.aadhaar_number),
                    'secret_pin': s.student.secret_pin,
                    'gender': s.student.gender,
                    'added_by':s.student.added_by,
                    'updated_by':s.student.updated_by,
                    'img': s.student.image, 
                })
            if approval.account_approval_status == 2:
                account_rejected_student.append({
                    'id': s.student.id,
                    'name': s.student.name,
                    'mobile': s.student.mobile,
                    'aadhaar_number': str(s.student.aadhaar_number),
                    'secret_pin': s.student.secret_pin,
                    'gender': s.student.gender,
                    'added_by':s.student.added_by,
                    'updated_by':s.student.updated_by,
                    'img': s.student.image, 
                })
        context={
            'clerk':clerk,
            'student_sell_form':Student_Hostel_Fee.objects.filter(batch=clerk.batch).exclude(form_number=None).count(),
            'hostel_form_pending_count':hostel_form_pending_count,
            'hostel_form_accepted_count':hostel_form_accepted_count,
            'hostel_form_account_rejected_count':hostel_form_account_rejected_count,
            'pending_student':st,
            'account_rejected_student':account_rejected_student
        }
        return render(request, 'report/hostel_form_summary.html', context)
    else:
        return redirect('office_login')
    
@check_employee_permissions
def employee_report(request):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        clerk = Employee.objects.filter(mobile=mobile).first()
        if not clerk:
            return redirect('office_login')        
        context={
            'clerk':clerk,
        }
        return render(request, 'report/employee_report.html', context)
    else:
        return redirect('office_login')

def get_correct_status(status):
    if int(status) == 0:
        return 'Pending'
    elif int(status) == 1:
        return 'Approved'
    elif int(status) == 2:
        return 'Rejected'
    elif int(status) == 3:
        return 'Not Required'

def download_student_admission_details_college(request, id):
    college = College.objects.filter(id=id).first()
    name = f'excel_reports/student_admission_details_college-{date.today()}.csv'
    with open(name, 'w+', newline='', encoding='utf-8') as f:
        lnwriter = csv.writer(f, quoting=csv.QUOTE_ALL)

        lnwriter.writerow([
           college.name
        ])
        lnwriter.writerow([])
        
        lnwriter.writerow([
            'Student Name (As per Aadhaar)',
            'Student Name (As per SSC Mark Sheet )',
            'Aadhaar Number',
            'PAN Number',
            'Gender',
            'Date of Birth',
            'Blood Group',
            'Contact/Mobile No.',
            'Whatsapp No.',
            'Email',
            'Permanent Address',
            'District',
            'Taluka',
            'Pin Code',
            'Current Address',
            'Is Father Alive',
            'Fathers /Parent Full Name',
            'Father Mobile No.',
            'Mothers Full Name',
            'Mother Mobile No.',
            'Nominee Name',
            'Relation With Nominee',
            'How to Arrive College',
            'College',
            'Admission Branch',
            'Current Year',
            'Year of Admission (first Year / Direct Second Year)',
            'Admission Quota',
            'Category',
            'Cast',
            'Current Admission Type',
            'Hostel Form Number',
            'Hostel Form Issued By',
            'Hostel Form Issued Date',
            'College Form Number',
            'College Form Issued By',
            'college Form Issued Date',
            'Office Approval Status',
            'Office Approved By',
            'Office Approved Date',
            'Office Rejected Reason',
            'Store Approval Status',
            'Store Approved By',
            'Store Approved Date',
            'Store Rejected Reason',
            'Hostel Account Approval Status',
            'Hostel Account Approved By',
            'Hostel Account Approved Date',
            'Hostel Account Rejected Reason',
            'College Account Approval Status',
            'College Account Approved By',
            'College Account Approved Date',
            'College Account Rejected Reason',
            'Travel Account Approval Status',
            'Travel Account Approved By',
            'Travel Account Approved Date',
            'Travel Account Rejected Reason',
        ])
        
        
        for c in Student_college_detail.objects.filter(college=college).exclude(form_number=None):
            student_hostel_fee = Student_Hostel_Fee.objects.filter(student=c.student, batch=c.batch).first()
            student_approval = Student_approval.objects.filter(student=c.student, batch=c.batch).first()
            lnwriter.writerow([
                c.student.name, # Student Name (As per Aadhaar)
                c.student.student_name_as_per_ssc_marksheet, # Student Name (As per SSC Mark Sheet )
                c.student.aadhaar_number, # Aadhaar Number
                c.student.pan_number, # PAN Number
                c.student.gender, # Gender
                c.student.date_of_birth, # Date of Birth
                c.student.blood_group, # Blood Group
                c.student.mobile, # Contact/Mobile No.
                c.student.whatsapp_number, # Whatsapp No.
                c.student.email, # Email
                c.student.address, # Permanent Address
                c.student.district.name, # District
                c.student.taluka.name, # Taluka
                c.student.pin_code, # Pin Code
                c.student.current_address, # Current Address
                c.student.is_father_alive, # Is Father Alive
                c.student.father_name, # Fathers /Parent Full Name
                c.student.parent_mobile, # Father Mobile No.
                c.student.mother_name, # Mothers Full Name
                c.student.mother_mobile, # Mother Mobile No.
                c.student.nominee_name, # Nominee Name
                c.student.relation_with_nominee, # Relation With Nominee
                c.how_to_arrive_college, # How to Arrive College
                c.college.name, # College
                c.branch.name, # Admission Branch
                c.year.name, # Current Year
                c.admission_year, # Year of Admission (first Year / Direct Second Year)
                c.admission_quota, # Admission Quota
                c.student.cast_category.name, # Category
                c.student.cast, # Cast
                c.current_admission_type, # Current Admission Type
                student_hostel_fee.form_number if student_hostel_fee else '', # Hostel Form Number
                student_hostel_fee.form_issued_by.name if student_hostel_fee and student_hostel_fee.form_issued_by else '', # Hostel Form Issued By
                student_hostel_fee.form_issued_date if student_hostel_fee else '', # Hostel Form Issued Date
                c.form_number, # College Form Number
                c.form_issued_by.name, # College Form Issued By
                c.form_issued_date, # college Form Issued Date
                get_correct_status(student_approval.office_approval_status), # Office Approval Status
                student_approval.office_approved_by.name if student_approval.office_approved_by else '' , # Office Approved By
                student_approval.office_approved_date, # Office Approved Date
                student_approval.office_rejected_reason, # Office Rejected Reason
                get_correct_status(student_approval.store_approval_status), # Store Approval Status
                student_approval.store_approved_by.name if student_approval.store_approved_by else '' , # Store Approved By
                student_approval.store_approved_date, # Store Approved Date
                student_approval.store_rejected_reason, # Store Rejected Reason
                get_correct_status(student_approval.account_approval_status), # Hostel Account Approval Status
                student_approval.account_approved_by.name if student_approval.account_approved_by else '' , # Hostel Account Approved By
                student_approval.account_approved_date, # Hostel Account Approved Date
                student_approval.account_rejected_reason, # Hostel Account Rejected Reason
                get_correct_status(student_approval.college_account_approval_status), # College Account Approval Status
                student_approval.college_account_approved_by.name if student_approval.college_account_approved_by else '' , # College Account Approved By
                student_approval.college_account_approved_date, # College Account Approved Date
                student_approval.college_account_rejected_reason, # College Account Rejected Reason
                get_correct_status(student_approval.travel_account_approval_status), # Travel Account Approval Status
                student_approval.travel_account_approved_by.name if student_approval.travel_account_approved_by else '' , # Travel Account Approved By
                student_approval.travel_account_approved_date, # Travel Account Approved Date
                student_approval.travel_account_rejected_reason, # Travel Account Rejected Reason
            ])
            
        
        
    return redirect(f'/{name}')
    