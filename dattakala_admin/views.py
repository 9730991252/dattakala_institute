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