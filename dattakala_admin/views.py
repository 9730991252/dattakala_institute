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
        
        student = get_object_or_404(Student, id=id)
        if student:
            student_approval = Student_approval.objects.filter(student=student).first()
            if student_approval:
                if student_approval.office_approval_status == 0 or student_approval.store_approval_status == 0 or student_approval.account_approval_status == 0:
                    messages.error(request, 'Please Approve the Student First')
                    return redirect('student_fees')
                if student_approval.office_approval_status == 2 or student_approval.store_approval_status == 2 or student_approval.account_approval_status == 2:
                    messages.error(request, 'You Cant Open Rejected Student')
                    return redirect('student_fees')
            else:
                messages.error(request, 'Please Approve the Student First')
                return redirect('student_fees')
            

        cash_fee = Student_received_Fee_Cash.objects.filter(student=student, added_by__batch=a.batch)
        bank_fee = Student_received_Fee_Bank.objects.filter(student=student, added_by__batch=a.batch)
        received_cash_hostel_fee = Student_Received_Fee_Cash_Hostel.objects.filter(student=student, added_by__batch=a.batch)
        received_bank_hostel_fee = Student_received_Fee_Bank_hostel.objects.filter(student=student, added_by__batch=a.batch)
        paid_fee = int(cash_fee.aggregate(Sum('received_amount'))['received_amount__sum'] or 0) + int(bank_fee.aggregate(Sum('received_amount'))['received_amount__sum'] or 0) +  int(received_cash_hostel_fee.aggregate(Sum('received_amount'))['received_amount__sum'] or 0) +  int(received_bank_hostel_fee.aggregate(Sum('received_amount'))['received_amount__sum'] or 0)
        student_hostel_fee = Student_Hostel_Fee.objects.filter(batch=a.batch, student=student).first()
        total_fee = student_fee.objects.filter(student=student, batch=a.batch).aggregate(Sum('amount'))['amount__sum'] or 0
        if student_hostel_fee:
            total_fee += int(student_hostel_fee.hostel_fee.amount)
        print('total_fee', total_fee)
        student_fee_detail = []
        for cdt in Credit_Debit_category.objects.filter(status=1):
            detail_total_fee = student_fee.objects.filter(credit_debit_category=cdt, student=student).aggregate(Sum('amount'))['amount__sum'] or 0
            detail_paid_fee = Student_received_Fee_Cash.objects.filter(credit_debit_category=cdt, student=student).aggregate(Sum('received_amount'))['received_amount__sum'] or 0
            detail_paid_fee += Student_received_Fee_Bank.objects.filter(credit_debit_category=cdt, student=student).aggregate(Sum('received_amount'))['received_amount__sum'] or 0
            if detail_total_fee >0:
                student_fee_detail.append({
                    'category': cdt,
                    'total_fee': detail_total_fee,
                    'detail_paid_fee': detail_paid_fee,
                    'remaining_fee': detail_total_fee - detail_paid_fee
                })

        context = {
            'student_fee_detail': student_fee_detail,
            'a': a,
            'student': student,
            'today_date':date.today(),
            'cash_fee':cash_fee,
            'bank_fee':bank_fee,
            'paid_fee':paid_fee,
            'remaining_fee':int(total_fee)-int(paid_fee),
            'accounts':Bank_Account.objects.filter(status=1),
            'total_fee': total_fee,
            'credit_debit_category': Credit_Debit_category.objects.filter(status=1),
            'student_fee': student_fee.objects.filter(student=student, batch=a.batch),
            'student_hostel_fee': student_hostel_fee,
            'student_college': Student_college_detail.objects.filter(student=student, batch=a.batch).first(),
            'received_cash_hostel_fee':received_cash_hostel_fee,
            'received_bank_hostel_fee':received_bank_hostel_fee,
            'all_hostel_fee_installment':Hostel_Fee_installment.objects.filter(status=1, batch=a.batch)
        }
        
        context={
            'a':a,
            'accounts':Bank_Account.objects.all(),
        }
        return render(request, 'admin_student_detail.html', context)
    else:
        return redirect('/')