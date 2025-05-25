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
        return redirect('Admin_detail')