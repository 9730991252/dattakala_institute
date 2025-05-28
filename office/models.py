from django.db import models
from PIL import Image

# Create your models here.
class Batch(models.Model):
    name = models.CharField(max_length=100, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.IntegerField(default=1)
    edit_status = models.IntegerField(default=1)
    
class Admin_detail(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, null=True, related_name='batch')
    name = models.CharField(max_length=100, null=True)
    mobile = models.IntegerField(null=True)
    pin =models.CharField(max_length=10, null=True)
    status = models.IntegerField(default=1, null=True)
    
    
class Clerk(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='clerks')
    name = models.CharField(max_length=100, unique=True)
    mobile = models.IntegerField(unique=True)
    secret_pin = models.IntegerField()
    status = models.IntegerField(default=1)
    
class College(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='colleges')
    name = models.CharField(max_length=100, unique=True)
    status = models.IntegerField(default=1)
    added_by = models.ForeignKey(Clerk, on_delete=models.CASCADE, related_name='added_colleges')
    updated_date = models.DateTimeField(auto_now=True, null=True)
    updated_by = models.ForeignKey(Clerk, on_delete=models.CASCADE, null=True, related_name='updated_by_Colleges')
    
class Branch(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='branches')
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name='branches')
    name = models.CharField(max_length=100)
    status = models.IntegerField(default=1)
    added_by = models.ForeignKey(Clerk, on_delete=models.CASCADE, related_name='added_branches')
    updated_date = models.DateTimeField(auto_now=True, null=True)
    updated_by = models.ForeignKey(Clerk, on_delete=models.CASCADE, null=True, related_name='updated_by_Branches')
    
class Year(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='add_years')
    name = models.CharField(max_length=100)
    status = models.IntegerField(default=1)
    added_by = models.ForeignKey(Clerk, on_delete=models.CASCADE, related_name='added_years')
    updated_date = models.DateTimeField(auto_now=True, null=True)
    updated_by = models.ForeignKey(Clerk, on_delete=models.CASCADE, null=True, related_name='updated_by_years')
    
GENDER_CHOICES = (
    ('Male', "Male"),
    ('Female', "Female"),
)

class Student(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.IntegerField(null=True)
    aadhaar_number = models.IntegerField(unique=True)
    secret_pin = models.CharField(max_length=10, null=True)
    status = models.IntegerField(default=1)
    gender = models.CharField(max_length=10, null=True)
    added_date = models.DateField(auto_now_add=True)
    address = models.CharField(max_length=255, null=True)
    added_by = models.ForeignKey(Clerk, on_delete=models.CASCADE, null=True, related_name='added_by')
    date_of_birth = models.DateField(null=True)
    father_name = models.CharField(max_length=100, null=True)
    mother_name = models.CharField(max_length=100, null=True)
    parent_mobile = models.IntegerField(null=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)
    updated_by = models.ForeignKey(Clerk, on_delete=models.CASCADE, null=True, related_name='updated_by_student')
    approval_status = models.IntegerField(default=0)  # 0 = pending, 1 = approved, 2 = rejected
    approved_by = models.ForeignKey(Clerk, on_delete=models.CASCADE, null=True, related_name='approved_by_clerk')
    approved_date = models.DateTimeField(null=True)
    blood_group = models.CharField(max_length=100, null=True)
    email = models.EmailField(null=True)
    current_address = models.CharField(max_length=500, null=True)

class Student_college_detail(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    added_by = models.ForeignKey(Clerk, on_delete=models.CASCADE, null=True)
    added_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)
    updated_by = models.ForeignKey(Clerk, on_delete=models.CASCADE, null=True, related_name='updated_by_Student_college_detail')

class Bank_Account(models.Model):
    added_by = models.ForeignKey(Clerk, on_delete=models.CASCADE, null=True)
    account_number = models.CharField(max_length=100, null=True)
    bank_name = models.CharField(max_length=100, null=True)
    status = models.IntegerField(default=1)
    
class Bank_Account_Opening_Balance(models.Model):
    added_by = models.ForeignKey(Clerk, on_delete=models.CASCADE, null=True)
    account = models.ForeignKey(Bank_Account, on_delete=models.CASCADE, null=True)
    opening_balance = models.IntegerField(default=0)
    added_date = models.DateTimeField(auto_now_add=True, null=True)
    
class Credit_Debit_category(models.Model):
    category_name = models.CharField(max_length=100)
    order_by = models.IntegerField(default=0)
    added_by = models.ForeignKey(Clerk, on_delete=models.CASCADE, null=True, related_name='added_by_credit_debit_category')
    added_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)
    updated_by = models.ForeignKey(Clerk, on_delete=models.CASCADE, null=True, related_name='updated_by_credit_debit_category')
    status = models.IntegerField(default=1)


class Student_Image(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="student_images",default="",null=True, blank=True)
    added_date = models.DateTimeField(auto_now_add=True, null=True)
    added_by = models.ForeignKey(Clerk, on_delete=models.CASCADE, null=True)
    
class Student_received_Fee_Bank(models.Model):
    credit_debit_category = models.ForeignKey(Credit_Debit_category, on_delete=models.CASCADE, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    received_amount = models.FloatField(default=0)
    paid_date = models.DateField(null=True)
    added_by = models.ForeignKey(Clerk, on_delete=models.CASCADE, null=True, related_name='added_by_student_recived_fee')
    added_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)
    updated_by = models.ForeignKey(Clerk, on_delete=models.CASCADE, null=True, related_name='updated_by_student_recived_fee')
    account = models.ForeignKey(Bank_Account, on_delete=models.CASCADE, null=True, blank=True)
    admin_verify_status = models.IntegerField(default=0) # 0 = not verify, 1 = verify
    verify_date = models.DateTimeField(null=True, blank=True)
    verify_by = models.ForeignKey(Admin_detail, on_delete=models.CASCADE, null=True)
    verify_by_clerk = models.ForeignKey(Clerk, on_delete=models.CASCADE, null=True,related_name='added_by_student_received_fee_verify' )
    utr_number = models.CharField(max_length=100, null=True, blank=True)
    
class student_fee(models.Model):
    credit_debit_category = models.ForeignKey(Credit_Debit_category, on_delete=models.CASCADE, null=True)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    added_date = models.DateTimeField(auto_now_add=True, null=True)
    added_by = models.ForeignKey(Clerk, on_delete=models.CASCADE, null=True, related_name='added_by_student_fee')
    verify_date = models.DateTimeField(null=True, blank=True)
    verify_by = models.ForeignKey(Admin_detail, on_delete=models.CASCADE, null=True, related_name='veryfy_by_student_fee')
     
    
class Student_received_Fee_Cash(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    credit_debit_category = models.ForeignKey(Credit_Debit_category, on_delete=models.CASCADE, null=True)
    received_amount = models.FloatField(default=0)
    paid_date = models.DateField(null=True)
    added_by = models.ForeignKey(Clerk, on_delete=models.CASCADE, null=True, related_name='added_by_student_received_fee')
    added_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)
    updated_by = models.ForeignKey(Clerk, on_delete=models.CASCADE, null=True, related_name='updated_by_student_received_fee')
    admin_verify_status = models.IntegerField(default=0) # 0 = not verify, 1 = verify
    verify_date = models.DateTimeField(null=True, blank=True)
    verify_by = models.ForeignKey(Admin_detail, on_delete=models.CASCADE, null=True, related_name='veryfy_by_student_received_fee')
    
class Expenses(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    remark = models.CharField(max_length=500)
    type = models.CharField(max_length=100)
    added_by = models.ForeignKey(Clerk, on_delete=models.CASCADE, null=True, related_name='added_by_clerk')
    from_bank = models.ForeignKey(Bank_Account, on_delete=models.CASCADE, null=True, blank=True, related_name='from_bank')
    check_number = models.CharField(max_length=100,null=True)
    added_date = models.DateTimeField(auto_now_add=True)
    date = models.DateField(null=True)
    updated_by = models.ForeignKey(Clerk, on_delete=models.CASCADE, null=True, related_name='updated_by_clerk')
    updated_date = models.DateTimeField(null=True)
    admin_verify_status = models.IntegerField(default=0) # 0 = not verify, 1 = verify
    verify_date = models.DateTimeField(null=True, blank=True)
    
class Hostel_Fee_installment(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    installment_name = models.CharField(max_length=100)
    added_by = models.ForeignKey(Clerk, on_delete=models.CASCADE, null=True)
    added_date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=1)
    
class Student_Hostel_Fee(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    hostel_fee = models.ForeignKey(Hostel_Fee_installment, on_delete=models.CASCADE)
    added_by = models.ForeignKey(Clerk, on_delete=models.CASCADE, null=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)
    updated_by = models.ForeignKey(Clerk, on_delete=models.CASCADE, null=True, related_name='updated_by_Student_Hostel_Fee')
    
    
class Student_Received_Fee_Cash_Hostel(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    received_amount = models.FloatField(default=0)
    paid_date = models.DateField(null=True)
    added_by = models.ForeignKey(Clerk, on_delete=models.CASCADE, null=True, related_name='added_by_student_received_fee_hostel')
    added_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)
    updated_by = models.ForeignKey(Clerk, on_delete=models.CASCADE, null=True, related_name='updated_by_student_received_fee_hostel')
    admin_verify_status = models.IntegerField(default=0) # 0 = not verify, 1 = verify
    verify_date = models.DateTimeField(null=True, blank=True)
    verify_by_admin = models.ForeignKey(Admin_detail, on_delete=models.CASCADE, null=True, related_name='verify_by_admin_hostel')
    verify_by_clerk = models.ForeignKey(Clerk, on_delete=models.CASCADE, null=True, related_name='verify_by_clerk_hostel')
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, null=True, related_name='batch_student_received_fee_hostel')
    challan_number = models.CharField(max_length=100, null=True, blank=True)
    
class Student_received_Fee_Bank_hostel(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    received_amount = models.FloatField(default=0)
    paid_date = models.DateField(null=True)
    added_by = models.ForeignKey(Clerk, on_delete=models.CASCADE, null=True, related_name='added_by_student_received_fee_bank_hostel')
    added_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)
    updated_by = models.ForeignKey(Clerk, on_delete=models.CASCADE, null=True, related_name='updated_by_student_received_fee_bank_hostel')
    account = models.ForeignKey(Bank_Account, on_delete=models.CASCADE, null=True, blank=True)
    admin_verify_status = models.IntegerField(default=0)  # 0 = not verify, 1 = verify
    verify_date = models.DateTimeField(null=True, blank=True)
    verify_by_admin = models.ForeignKey(Admin_detail, on_delete=models.CASCADE, null=True,related_name='verify_by_admin_bank_hostel')
    verify_by_clerk = models.ForeignKey(Clerk, on_delete=models.CASCADE, null=True,related_name='verify_by_clerk_bank_hostel')
    verify_date_clerk = models.DateTimeField(null=True, blank=True)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, null=True,related_name='batch_student_received_fee_bank_hostel')
    utr_number = models.CharField(max_length=100, null=True, blank=True)
    
class District(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    created_by = models.ForeignKey(Clerk, on_delete=models.CASCADE, null=True, related_name='created_by_district')
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)
    updated_by = models.ForeignKey(Clerk, on_delete=models.CASCADE, null=True, related_name='updated_by_district')
    status = models.IntegerField(default=1)

class Taluka(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, null=True, related_name='district_taluka')
    created_by = models.ForeignKey(Clerk, on_delete=models.CASCADE, null=True, related_name='created_by_taluka')
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)
    updated_by = models.ForeignKey(Clerk, on_delete=models.CASCADE, null=True, related_name='updated_by_taluka')
    status = models.IntegerField(default=1)
    
class Cast_category(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    created_by = models.ForeignKey(Clerk, on_delete=models.CASCADE, null=True, related_name='created_by_cast_category')
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)
    updated_by = models.ForeignKey(Clerk, on_delete=models.CASCADE, null=True, related_name='updated_by_cast_category')
    status = models.IntegerField(default=1)