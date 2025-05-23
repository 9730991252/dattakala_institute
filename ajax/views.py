
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

def search_student_for_fees(request):
    if request.method == 'GET':
        words = request.GET['words']
        st = []
        if words:
            student = list(Student.objects.filter(name__icontains=words))
            student += Student.objects.filter(mobile__icontains=words)
            student += Student.objects.filter(aadhar_number__icontains=words)
            for s in student:
                st.append({
                    'id':s.id,
                    'name':s.name,
                    'mobile':s.mobile,
                    'aadhar_number':s.aadhar_number,
                    'secret_pin':s.secret_pin,
                    'gender':s.gender,
                    # 'img':Student_Image.objects.filter(student=s).first(),
                })
        context = {
            'student':st
        }
        t = render_to_string('search_student_for_fees.html', context)
    return JsonResponse({'t': t})
