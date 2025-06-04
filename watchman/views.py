from dattakala_institute.includes import *


# Create your views here.
from django.db import transaction
from django.utils import timezone

def watchman_home(request):
    if not request.session.get('watchman_mobile'):
        return redirect('watchman_login')
    mobile          = request.session['watchman_mobile']
    employee        = Employee.objects.filter(mobile=mobile).first()
    if not employee:
        return redirect('office_login')
    if 'book_appointment' in request.POST:
        v_name      = request.POST.get('visitor_name', '').strip()
        v_mobile    = request.POST.get('visitor_mobile', '').strip()
        v_address   = request.POST.get('visitor_address', '').strip()
        meat_to     = request.POST.get('meat_to', '').strip()
        visit_reason= request.POST.get('visit_reason', '').strip()

        visitor, created = Visitor.objects.get_or_create(
            visitor_mobile=v_mobile,
            defaults={
                "visitor_name":    v_name,
                "visitor_address": v_address,
                "added_by":        employee,
            },
        )

        if not created :
            visitor.visitor_name    = v_name
            visitor.visitor_address = v_address
            visitor.save()

        Appointment.objects.create(
            visitor      = visitor,
            visit_reason = visit_reason,
            meat_to     = meat_to,
            added_by     = employee,
            book_date_time    = datetime.now()
        )
        messages.success(request, "Appointment Booked Successfully")
        return redirect("watchman_home")
    context = {
        "employee": employee,
        "todays_appointments": Appointment.objects.filter(book_date_time__date=date.today()).exclude(meeting_status=3).exclude(meeting_status=2).order_by('-order_by')
        }
    return render(request,'watchman_home.html', context)