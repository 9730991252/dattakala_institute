from dattakala_institute.includes import *
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

    