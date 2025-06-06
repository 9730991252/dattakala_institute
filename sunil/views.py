from dattakala_institute.includes import *
# Create your views here.
def sunil_login(request):
    if request.method == 'POST':
        a =int(request.POST["first_number"])
        b =int(request.POST["seconde_number"])
        s = a+b 
        su = sunil.objects.filter().first()
        if s == int(su.sum) :
            request.session['sunil_mobile'] = s
            return redirect('/sunil/sunil_home/')
        else:
            return redirect('sunil_login')
    return render(request, 'sunil_login.html')

def sunil_home(request):
    if request.session.has_key('sunil_mobile'):
        if 'Add_batch'in request.POST:
            name = request.POST.get('name')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            Batch(
                name=name,
                start_date=start_date,
                end_date=end_date
            ).save()
            return redirect('sunil_home')
        if 'edit_batch' in request.POST:
            batch_id = request.POST.get('id')
            batch = Batch.objects.get(id=batch_id)
            batch.name = request.POST.get('name')
            batch.start_date = request.POST.get('start_date')
            batch.end_date = request.POST.get('end_date')
            batch.save()
            return redirect('sunil_home')
        if 'batch_active' in request.POST:
            batch_id = request.POST.get('id')
            batch = Batch.objects.get(id=batch_id)
            batch.status = 0
            batch.save()
            return redirect('sunil_home')
        if 'batch_deactive' in request.POST:
            batch_id = request.POST.get('id')
            batch = Batch.objects.get(id=batch_id)
            batch.status = 1
            batch.save()
            return redirect('sunil_home')
        if 'add_employee_category'in request.POST:
            category_name = request.POST.get('name').upper()
            category = Employee_category.objects.create(name=category_name)
            category.save()
            return redirect('sunil_home')
        if 'edit_category'in request.POST:
            category_id = request.POST.get('id')
            category_name = request.POST.get('name').upper()
            category = Employee_category.objects.get(id=category_id)
            category.name = category_name
            category.save()
            return redirect('sunil_home')
        if 'update_status'in request.POST:
            category_id = request.POST.get('id')
            category = Employee_category.objects.get(id=category_id)
            if category.status == 1:
                category.status = 0
            else:
                category.status = 1
            category.save()
            return redirect('sunil_home')
        if 'Add_Admin' in request.POST:
            batch_id = request.POST.get('batch_id')
            mobile = request.POST.get('mobile')
          
            if Admin_detail.objects.filter(batch_id=batch_id,mobile=mobile).exists():
                return redirect('sunil_home')
            else:
                Admin_detail(
                    batch_id=batch_id,
                    name=request.POST.get('name'),
                    mobile=mobile,
                    pin=request.POST.get('secret_pin')
                ).save()
            return redirect('sunil_home')
        if 'Add_Employee' in request.POST:
            batch_id = request.POST.get('batch_id')
            category = request.POST.get('category')
            name = request.POST.get('name')
            aadhar_number = request.POST.get('aadhar_number')
            mobile = request.POST.get('mobile')
          
            if Employee.objects.filter(batch_id=batch_id,aadhar_number=aadhar_number).exists():
                return redirect('sunil_home')
            else:
                Employee(
                    batch_id=batch_id,
                    name=name,
                    mobile=mobile,
                    secret_pin=0,
                    aadhar_number=aadhar_number,
                    category_id=category
                ).save()
            messages.success(request, 'Employee Added Successfully')
            return redirect('sunil_home')
        if 'edit_admin' in request.POST:
            admin_id = request.POST.get('id')
            mobile = request.POST.get('mobile')
            batch_id = request.POST.get('batch_id')

            if Admin_detail.objects.filter(mobile=mobile, batch_id=batch_id).exists():
                existing_admin = Admin_detail.objects.get(mobile=mobile, batch_id=batch_id)
                if existing_admin.id != int(admin_id):
                    return redirect('sunil_home')
            admin = Admin_detail.objects.get(id=admin_id)
            admin.name = request.POST.get('name')
            admin.mobile = mobile
            admin.pin = request.POST.get('secret_pin')
            admin.batch_id = batch_id
            admin.save()
            return redirect('sunil_home')
        if 'admin_active' in request.POST:
            admin_id = request.POST.get('id')
            admin = Admin_detail.objects.get(id=admin_id)
            admin.status = 0
            admin.save()
            return redirect('sunil_home')
        if 'admin_deactive' in request.POST:
            admin_id = request.POST.get('id')
            admin = Admin_detail.objects.get(id=admin_id)
            admin.status = 1
            admin.save()
            return redirect('sunil_home')
        context = {
            'batches': Batch.objects.all().order_by('name'),
            'admins': Admin_detail.objects.all().order_by('name'),
            'employee_category':Employee_category.objects.all(),
            'employee':Employee.objects.all(),
            'admin_used_count':admin_used_count.objects.all().first()
        }
        return render(request, 'sunil_home.html', context)
    else:
        return redirect('sunil_login')