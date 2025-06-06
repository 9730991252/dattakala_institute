from dattakala_institute.includes import *


# Create your views here.
from django.db import transaction
from django.utils import timezone

@csrf_exempt
def peon_home(request):
    if not request.session.get('peon_mobile'):
        return redirect('peon_login')

    mobile          = request.session['peon_mobile']
    employee        = Employee.objects.filter(mobile=mobile).first()
    if not employee:
        return redirect('office_login')

    if 'update_order_by'in request.POST:
        appointment_id = request.POST.get('appointment_id')
        order_by = request.POST.get('order_by')
        Appointment.objects.filter(id=appointment_id).update(order_by=order_by)
        return redirect("peon_home")
    if 'update_status_running'in request.POST:
        appointment_id = request.POST.get('appointment_id')
        Appointment.objects.filter(id=appointment_id).update(
            meeting_status=1,
            meeting_start_time=datetime.now()
            )
        return redirect("peon_home")
    if 'update_status_cancelled'in request.POST:
        appointment_id = request.POST.get('appointment_id')
        Appointment.objects.filter(id=appointment_id).update(meeting_status=3)
        return redirect("peon_home")
    if 'update_status_completed'in request.POST:
        appointment_id = request.POST.get('appointment_id')
        Appointment.objects.filter(id=appointment_id).update(
            meeting_status=2,
            meeting_end_time=datetime.now()
            )
        return redirect("peon_home")
    todays_appointments = []
    for t in Appointment.objects.filter(book_date_time__date=date.today()).exclude(meeting_status=3).order_by('-meeting_status', '-order_by'):
        booked_date_time = timezone.localtime(t.book_date_time)
        now = timezone.localtime(timezone.now())  # Make sure both are timezone-aware and in same timezone

        waiting_from = now - booked_date_time

        if not t.meeting_status == 2:
            todays_appointments.append(
                                       {
                                        'id':t.id,
                                        'visitor':t.visitor,
                                        'added_by':t.added_by,
                                        'visit_reason':t.visit_reason,
                                        'book_date_time':t.book_date_time,
                                        'meeting_start_time':t.meeting_start_time,
                                        'meeting_end_time':t.meeting_end_time,
                                        'order_by':t.order_by,
                                        'meat_to':t.meat_to,
                                        'meeting_status':t.meeting_status,
                                        'waiting_from':waiting_from,
                                        'waiting_from_total_seconds':waiting_from.total_seconds()
                                       } 
                                       )
    context = {
        "employee": employee,
        "todays_appointments":todays_appointments
        }
    return render(request, "peon_home.html", context)

@csrf_exempt
def book_appointment(request):
    if not request.session.get('peon_mobile'):
        return redirect('peon_login')

    mobile = request.session['peon_mobile']
    employee = Employee.objects.filter(mobile=mobile).first()
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
        )
        messages.success(request, "Appointment Booked Successfully")
        return redirect("peon_home")
    context = {
        "employee": employee,
        }
    return render(request, "book_appointment.html", context)
