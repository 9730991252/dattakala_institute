
from dattakala_institute.includes import *
# Create your views here.
def search_student_for_edit(request):
    if request.method == 'GET':
        words = request.GET['words']
        student = list(Student.objects.filter(name__icontains=words))
        student += Student.objects.filter(mobile__icontains=words)
        student += Student.objects.filter(aadhar_number__icontains=words)
        context = {
            'students':student
        }
        t = render_to_string('search_student_for_edit.html', context)
    return JsonResponse({'t': t})

def check_student_aadhaar(request):
    if request.method == 'GET':
        aadhaar = request.GET['aadhaar']
        student = Student.objects.filter(aadhaar_number=aadhaar).first()
        return_status = 0
        student_id = None
        if student:
            student_id = student.id
            return_status = 1

    return JsonResponse({'student_id': student_id, 'return_status': return_status})

def get_college_branch(request):
    if request.method == 'GET':
        c_id = request.GET['c_id']
        branches = Branch.objects.filter(college__id=c_id, status=1)
        context = {
            'branches': branches
        }
        t = render_to_string('get_college_branch.html', context)
    return JsonResponse({'t': t})

def change_employee_permission_status(request):
    if request.method == 'GET':
        tab_id = request.GET['tab_id']
        employee_id = request.GET['employee_id']
        tp = Tab_permissions.objects.filter(employee_id=employee_id, tab_id=tab_id).first()
        if tp:
            if tp.status == 1:
                tp.status = 0
                tp.save()
            else:
                tp.status = 1
                tp.save()
        else:
            Tab_permissions.objects.create(employee_id=employee_id, tab_id=tab_id, status=1)
    return JsonResponse({'t': 't'})

def get_taluka(request):
    if request.method == 'GET':
        c_id = request.GET['c_id']
        taluka = Taluka.objects.filter(district__id=c_id, status=1)
        context = {
            'taluka': taluka
        }
        t = render_to_string('get_taluka.html', context)
    return JsonResponse({'t': t})

def search_student_for_fees(request):
    batch = Batch.objects.filter(start_date__year__lte=date.today().year, end_date__year__gte=date.today().year).first()
    if request.method == 'GET':
        words = request.GET['words']
        st = []
        if words:
            student = list(Student.objects.filter(name__icontains=words))
            student += Student.objects.filter(mobile__icontains=words)
            student += Student.objects.filter(aadhaar_number__icontains=words)
            for s in student:
                st.append({
                    'id':s.id,
                    'name':s.name,
                    'mobile':s.mobile,
                    'aadhaar_number':s.aadhaar_number,
                    'updated_by':s.updated_by,
                    'secret_pin':s.secret_pin,
                    'gender':s.gender,
                    'added_by':s.added_by,
                    'img': s.image, 
                    'approval':Student_approval.objects.filter(student=s, batch=batch).first,
                    
                })
        context = {
            'student':st
        }
        t = render_to_string('search_student_for_fees.html', context)
    return JsonResponse({'t': t})

def search_student_for_admin(request):
    batch = Batch.objects.filter(start_date__year__lte=date.today().year, end_date__year__gte=date.today().year).first()
    if request.method == 'GET':
        words = request.GET['words']
        st = []
        if words:
            student = list(Student.objects.filter(name__icontains=words))
            student += Student.objects.filter(mobile__icontains=words)
            student += Student.objects.filter(aadhaar_number__icontains=words)
            for s in student:
                approval = Student_approval.objects.filter(student=s, batch=batch).first()
                if approval is None or (approval.office_approval_status != 2 and approval.account_approval_status != 2 and approval.store_approval_status != 2):
                    st.append({
                         'id':s.id,
                        'name':s.name,
                        'mobile':s.mobile,
                        'aadhar_number':s.aadhaar_number,
                        'secret_pin':s.secret_pin,
                        'gender':s.gender,
                        'approval_status':s.approval_status,
                        'img': s.image, 
                        'approval':approval,
                        
                    })
        context = {
            'student':st
        }
        t = render_to_string('search_student_for_admin.html', context)
    return JsonResponse({'t': t})

def search_student_for_new_admission(request):
    batch = Batch.objects.filter(start_date__year__lte=date.today().year, end_date__year__gte=date.today().year).first()
    t = ''
    status = 0
    if request.method == 'GET':
        words = request.GET.get('words', '')
        st = []
        if words:
            status = 1
            students = Student.objects.filter(
                Q(name__icontains=words) |
                Q(mobile__icontains=words) |
                Q(aadhaar_number__icontains=words)
            ).distinct()

            for s in students:
                st.append({
                    'id': s.id,
                    'name': s.name,
                    'mobile': s.mobile,
                    'aadhaar_number': str(s.aadhaar_number),
                    'secret_pin': s.secret_pin,
                    'gender': s.gender,
                    'added_by':s.added_by,
                    'updated_by':s.updated_by,
                    'approval':Student_approval.objects.filter(student=s, batch=batch).first,
                    'img': s.image, 
                })

        context = {'student': st}
        t = render_to_string('search_student_for_new_admission.html', context)

    return JsonResponse({'t': t, 'status': status})