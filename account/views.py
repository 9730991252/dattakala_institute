from dattakala_institute.includes import *

# Create your views here.
def add_bank_account(request):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        clerk = Clerk.objects.filter(mobile=mobile).first()
        if not clerk:
            return redirect('office_login')
        if 'Add_Bank_Account' in request.POST:
            bank_name = request.POST.get('bank_name')
            account_number = request.POST.get('account_number')
            
            Bank_Account(
                added_by=clerk,
                bank_name=bank_name,
                account_number=account_number
            ).save()
            messages.success(request, 'Bank Account Added Successfully!')
            return redirect('add_bank_account')
        if 'edit_bank_account' in request.POST:
            id = request.POST.get('id')
            bank_name = request.POST.get('bank_name')
            account_number = request.POST.get('account_number')
            Bank_Account.objects.filter(id=id).update(
                bank_name=bank_name,
                account_number=account_number
            )
            messages.success(request, 'Bank Account Updated Successfully!')
            return redirect('add_bank_account')
        if 'active'in request.POST:
            bank_id = request.POST.get('id')
            bank = Bank_Account.objects.get(id=bank_id)
            bank.status = 0
            bank.save()
            return redirect('add_bank_account')
        if 'deactive'in request.POST:
            bank_id = request.POST.get('id')
            bank = Bank_Account.objects.get(id=bank_id)
            bank.status = 1
            bank.save()
            return redirect('add_bank_account')
        context={
            'clerk': clerk,
            'bank_accounts': Bank_Account.objects.filter(added_by=clerk)
        }
        return render(request, 'add_bank_account.html', context)
    else:
        return redirect('office_login')
    
def add_bank_opening_balance(request):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        clerk = Clerk.objects.filter(mobile=mobile).first()
        if not clerk:
            return redirect('office_login')
        if 'add_opening_balance' in request.POST:
            account_id = request.POST.get('account_id')
            amount = request.POST.get('amount')
            if Bank_Account_Opening_Balance.objects.filter(account_id=account_id).exists():
                messages.error(request, 'This account already has an opening balance!')
            else:
                Bank_Account_Opening_Balance.objects.create(
                    account_id=account_id,
                    opening_balance=amount,
                    added_by=clerk
                )
                messages.success(request, 'Opening balance added successfully!')
            return redirect('add_bank_opening_balance')
        context={
            'clerk':clerk,
            'bank_accounts':Bank_Account.objects.filter(status=1),
            'opening_balances':Bank_Account_Opening_Balance.objects.filter(),
        }
        return render(request, 'add_bank_opening_balance.html', context)
    else:
        return redirect('office_login')

def office_account_category(request):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        clerk = Clerk.objects.filter(mobile=mobile).first()
        if not clerk:
            return redirect('office_login')
        if 'add_category'in request.POST:
            name = request.POST.get('name')
            Credit_Debit_category(
                category_name=name,
                added_by=clerk
            ).save()
            messages.success(request, 'Account Category Added Successfully!')
            return redirect('office_account_category')
        if 'edit_category'in request.POST:
            name = request.POST.get('name')
            id = request.POST.get('id')
            Credit_Debit_category.objects.filter(id=id).update(category_name=name)
            messages.success(request, 'Account Category Updated Successfully!')
            return redirect('office_account_category')
        if 'change_status'in request.POST:
            id = request.POST.get('id')
            c = Credit_Debit_category.objects.filter(id=id).first()
            if c.status == 1:
                c.status = 0
            else:
                c.status = 1
            c.save() 
            messages.success(request, 'Account Category Status Updated Successfully!')
            return redirect('office_account_category')                    
        context={
            'clerk':clerk,
            'category':Credit_Debit_category.objects.filter(added_by__batch=clerk.batch)
        }
        return render(request, 'office_account_category.html', context)
    else:
        return redirect('office_login')

def student_fees(request):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        clerk = Clerk.objects.filter(mobile=mobile).first()
        if not clerk:
            return redirect('office_login')
        context={
            'clerk':clerk,
        }
        return render(request, 'student_fees.html', context)
    else:
        return redirect('office_login')
    
    
@csrf_exempt
def student_fee_detail(request, id):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        clerk = Clerk.objects.filter(mobile=mobile).first()
        if not clerk:
            return redirect('office_login')
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
            

        cash_fee = Student_received_Fee_Cash.objects.filter(student=student, added_by__batch=clerk.batch)
        bank_fee = Student_received_Fee_Bank.objects.filter(student=student, added_by__batch=clerk.batch)
        received_cash_hostel_fee = Student_Received_Fee_Cash_Hostel.objects.filter(student=student, added_by__batch=clerk.batch)
        received_bank_hostel_fee = Student_received_Fee_Bank_hostel.objects.filter(student=student, added_by__batch=clerk.batch)
        paid_fee = int(cash_fee.aggregate(Sum('received_amount'))['received_amount__sum'] or 0) + int(bank_fee.aggregate(Sum('received_amount'))['received_amount__sum'] or 0) +  int(received_cash_hostel_fee.aggregate(Sum('received_amount'))['received_amount__sum'] or 0) +  int(received_bank_hostel_fee.aggregate(Sum('received_amount'))['received_amount__sum'] or 0)
        student_hostel_fee = Student_Hostel_Fee.objects.filter(batch=clerk.batch, student=student).first()
        if 'save_cash_hostel_fee'in request.POST:
            received_amount = request.POST.get('received_amount')
            r_date = request.POST.get('date')
            challan_number = request.POST.get('challan_number')
            Student_Received_Fee_Cash_Hostel.objects.create(
                student=student,
                received_amount=received_amount,
                paid_date=r_date, 
                added_by=clerk,
                batch=clerk.batch,
                challan_number=challan_number
            )
            messages.success(request, 'Cash Hostel Fee Received Successfully!')
            return redirect('student_fee_detail', id=id)
        if 'save_bank_fee_hostel'in request.POST:
            bank_id = request.POST.get('bank_id')
            received_amount = request.POST.get('received_amount')
            r_date = request.POST.get('date')
            utr_number = request.POST.get('utr_number')
            Student_received_Fee_Bank_hostel.objects.create(
                student=student,
                received_amount=received_amount,
                paid_date=r_date,
                added_by=clerk,
                batch=clerk.batch,
                account_id=bank_id,
                utr_number=utr_number
            ) 
            messages.success(request, 'Bank Hostel Fee Received Successfully!')
            return redirect('student_fee_detail', id=id)
        if 'edit_bank_transaction'in request.POST:
            transaction_id = request.POST.get('transaction_id')
            bank_id = request.POST.get('bank_id')
            received_amount = request.POST.get('received_amount')
            r_date = request.POST.get('date')
            utr_number = request.POST.get('utr_number')
            Student_received_Fee_Bank_hostel.objects.filter(id=transaction_id).update(
                received_amount=received_amount,
                paid_date=r_date,
                account_id=bank_id,
                utr_number=utr_number,
                updated_date=datetime.now(),
                updated_by=clerk
            ) 
            messages.success(request, 'Bank Hostel updated Successfully!')
        total_fee = student_fee.objects.filter(student=student, batch=clerk.batch).aggregate(Sum('amount'))['amount__sum'] or 0
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
            'clerk': clerk,
            'student': student,
            'today_date':date.today(),
            'cash_fee':cash_fee,
            'bank_fee':bank_fee,
            'paid_fee':paid_fee,
            'remaining_fee':int(total_fee)-int(paid_fee),
            'accounts':Bank_Account.objects.filter(status=1),
            'total_fee': total_fee,
            'credit_debit_category': Credit_Debit_category.objects.filter(status=1),
            'student_fee': student_fee.objects.filter(student=student, batch=clerk.batch),
            'student_hostel_fee': student_hostel_fee,
            'student_college': Student_college_detail.objects.filter(student=student, batch=clerk.batch).first(),
            'received_cash_hostel_fee':received_cash_hostel_fee,
            'received_bank_hostel_fee':received_bank_hostel_fee,
            'all_hostel_fee_installment':Hostel_Fee_installment.objects.filter(status=1, batch=clerk.batch)
        }
        return render(request, 'student_fee_detail.html', context)
    else:
        return redirect('office_login')
    
    
def office_expenses(request):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        clerk = Clerk.objects.filter(mobile=mobile).first()
        if not clerk:
            return redirect('office_login')
        if 'add_cash_expenses'in request.POST:
            amount = request.POST.get('amount')
            remark = request.POST.get('remark')
            cdate = request.POST.get('date')
            Expenses(
                batch=clerk.batch,
                amount=amount,
                remark=remark,
                type='cash',
                added_by=clerk,
                date=cdate
            ).save()
            messages.success(request, 'Cash Expenses Added Successfully!')
            return redirect('office_expenses')
        if 'add_bank_expenses'in request.POST:
            amount = request.POST.get('amount')
            remark = request.POST.get('remark')
            from_bank = request.POST.get('from_bank')
            check_number = request.POST.get('check_number')
            bdate = request.POST.get('date')
            Expenses(
                batch=clerk.batch,
                amount=amount,
                remark=remark,
                type='bank',
                added_by=clerk,
                from_bank_id=from_bank,
                check_number=check_number,
                date=bdate
            ).save()
            messages.success(request, 'Bank Expenses Added Successfully!')
            return redirect('office_expenses')
        if 'edit_cash_expenses' in request.POST:
            exp_id = request.POST.get('id')
            expense = Expenses.objects.get(id=exp_id)
            expense.amount = request.POST.get('amount')
            expense.remark = request.POST.get('remark')
            expense.date = request.POST.get('date')
            expense.updated_by = clerk
            expense.updated_date = datetime.now()
            expense.save()
            messages.success(request, 'Cash Expense Updated Successfully!')
            return redirect('office_expenses')

        if 'edit_bank_expenses' in request.POST:
            exp_id = request.POST.get('id')
            expense = Expenses.objects.get(id=exp_id)
            expense.amount = request.POST.get('amount')
            expense.remark = request.POST.get('remark')
            expense.date = request.POST.get('date')
            expense.from_bank_id = request.POST.get('from_bank')
            expense.check_number = request.POST.get('check_number')
            expense.updated_by = clerk
            expense.updated_date = datetime.now()
            expense.save()
            messages.success(request, 'Bank Expense Updated Successfully!')
            return redirect('office_expenses')
        context={
            'clerk':clerk,
            'expenses':Expenses.objects.filter(batch=clerk.batch),
            'bank_accounts':Bank_Account.objects.filter(status=1),
            'today_date':date.today()
        }
        return render(request, 'office_expenses.html', context)
    else:
        return redirect('office_login')
    
def hostel_fee(request):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        clerk = Clerk.objects.filter(mobile=mobile).first()
        if not clerk:
            return redirect('office_login')
        if 'add_hostel_fee' in request.POST:
            amount = request.POST.get('amount')
            installment_name = request.POST.get('installment_name')
            Hostel_Fee_installment.objects.create(
                batch=clerk.batch,
                amount=amount,
                installment_name=installment_name,
                added_by=clerk
            )
            messages.success(request, 'Hostel Fee added successfully!')
            return redirect('hostel_fee')
        if 'edit_hostel_fee' in request.POST:
            id = request.POST.get('hostel_fee_id')
            amount = request.POST.get('amount')
            installment_name = request.POST.get('installment_name')
            hostel_fee = Hostel_Fee_installment.objects.filter(id=id).first()
            if hostel_fee:
                hostel_fee.amount = amount
                hostel_fee.installment_name = installment_name
                hostel_fee.save()
                messages.success(request, 'Hostel Fee updated successfully!')
            return redirect('hostel_fee')
        if 'change_status' in request.POST:
            hostel_fee_id = request.POST.get('hostel_fee_id')
            hostel_fee = Hostel_Fee_installment.objects.filter(id=hostel_fee_id).first()
            if hostel_fee: 
                if hostel_fee.status == 1:
                    hostel_fee.status = 0
                    messages.success(request, 'Hostel Fee deactivated successfully!')
                else:
                    hostel_fee.status = 1
                    messages.success(request, 'Hostel Fee activated successfully!')
                hostel_fee.save()
            return redirect('hostel_fee')
        context={
            'clerk':clerk,
            'hostel_fees':Hostel_Fee_installment.objects.filter(batch=clerk.batch),
        }
        return render(request, 'hostel_fee.html', context)
    else:
        return redirect('office_login')