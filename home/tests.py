@register.inclusion_tag('inclusion_tag/college_branches_hostel_student_details_admin.html')
def college_branches_hostel_student_details_admin(batch_id):
    branches = []
    for b in Branch.objects.filter(batch_id=batch_id).order_by('college'):
        year = []
        branch_total_amount = 0
        branch_received = 0
        for y in Year.objects.filter(added_by__batch_id=batch_id):
            male = Student_college_detail.objects.filter(branch=b, year=y, student__gender='Male').count()
            female = Student_college_detail.objects.filter(branch=b, year=y, student__gender='Female' ).count()
            total = Student_college_detail.objects.filter(branch=b, year=y).count()

            s_id = []
            for s in Student_college_detail.objects.filter(branch=b, year=y):
                s_id.append(s.student.id)
                # print(s.student.id, s.student.name)
            year_total_amount = Student_Hostel_Fee.objects.filter(student__id__in=s_id, batch_id=batch_id).aggregate(Sum('hostel_fee__amount'))['hostel_fee__amount__sum'] or 0
            # print(branch_total_amount)
            year_received = Student_received_Fee_Bank_hostel.objects.filter(student__id__in=s_id, batch_id=batch_id).aggregate(Sum('received_amount'))['received_amount__sum'] or 0
            year_received += Student_Received_Fee_Cash_Hostel.objects.filter(student__id__in=s_id, batch_id=batch_id).aggregate(Sum('received_amount'))['received_amount__sum'] or 0
            branch_total_amount += year_total_amount
            branch_received += year_received
            year.append({
                'id': y.id,
                'name': y.name,
                'male': male,
                'female': female,
                'total': total,
                'year_total_amount': year_total_amount,
                'year_received': year_received,
                'year_pending_amount': year_total_amount - year_received,
            })
        branches.append({
            'id': b.id,
            'name': b.name,
            'college':b.college,
            'years':year,
            'male':Student_college_detail.objects.filter(branch=b, student__gender='Male').count(),
            'female':Student_college_detail.objects.filter(branch=b, student__gender='Female').count(),
            'total':Student_college_detail.objects.filter(branch=b).count(),
            'branch_total_amount':branch_total_amount,
            'branch_received':branch_received,
            'pending_amount':branch_total_amount-branch_received,
        })

    all_total_amount = Student_Hostel_Fee.objects.filter(batch_id=batch_id).aggregate(Sum('hostel_fee__amount'))['hostel_fee__amount__sum'] or 0
    all_received = Student_received_Fee_Bank_hostel.objects.filter(batch_id=batch_id).aggregate(Sum('received_amount'))['received_amount__sum'] or 0
    all_received += Student_Received_Fee_Cash_Hostel.objects.filter(batch_id=batch_id).aggregate(Sum('received_amount'))['received_amount__sum'] or 0

    college = []
    for c in College.objects.filter(batch_id=batch_id):
        s_id = []
        for s in Student_college_detail.objects.filter(college=c):
            s_id.append(s.student.id)
        college_total_amount = Student_Hostel_Fee.objects.filter(student__id__in=s_id, batch_id=batch_id).aggregate(Sum('hostel_fee__amount'))['hostel_fee__amount__sum'] or 0
        all_received_college = Student_received_Fee_Bank_hostel.objects.filter(student_id__in=s_id,batch_id=batch_id).aggregate(Sum('received_amount'))['received_amount__sum'] or 0
        all_received_college += Student_Received_Fee_Cash_Hostel.objects.filter(student_id__in=s_id,batch_id=batch_id).aggregate(Sum('received_amount'))['received_amount__sum'] or 0
        college.append({
            'id': c.id,
            'name': c.name,
            'male':Student_college_detail.objects.filter(college=c, student__gender='Male').count(),
            'female':Student_college_detail.objects.filter(college=c, student__gender='Female').count(),
            'total':Student_college_detail.objects.filter(college=c).count(),
            'college_total_amount':college_total_amount,
            'college_received':all_received_college,
            'college_pending_amount':college_total_amount-all_received_college,
        'batch_id':batch_id,

        })


    return {
        'all_total_amount':all_total_amount,
        'all_received':all_received,
        'all_pending':all_total_amount-all_received,
        'branches':branches,
        'total_student':Student_Hostel_Fee.objects.filter(batch_id=batch_id).exclude(student__approval_status=2).count(),
        'male_student':Student_Hostel_Fee.objects.filter(batch_id=batch_id, student__gender='Male').exclude(student__approval_status=2).count(),
        'female_student':Student_Hostel_Fee.objects.filter(batch_id=batch_id, student__gender='Female').exclude(student__approval_status=2).count(),
        'college':college,
        'batch_id':batch_id,
    }
