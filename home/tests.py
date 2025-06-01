total -= Student_approval.objects.filter(batch_id=batch_id, student__district=d, office_approval_status = 2, account_approval_status = 2, store_approval_status = 2).count()
    male -= Student_approval.objects.filter(batch_id=batch_id,student__gender='Male', student__district=d, office_approval_status = 2, account_approval_status = 2, store_approval_status = 2).count()
    female -= Student_approval.objects.filter(batch_id=batch_id,student__gender='Female', student__district=d, office_approval_status = 2, account_approval_status = 2, store_approval_status = 2).count()
