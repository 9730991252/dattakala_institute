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
    
class Department(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='departments')
    name = models.CharField(max_length=100, unique=True)
    status = models.IntegerField(default=1)
    added_by = models.ForeignKey(Clerk, on_delete=models.CASCADE, related_name='added_departments')
    
GENDER_CHOICES = (
    ('MALE', "MALE"),
    ('FEMALE', "FEMALE"),
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
    edit_status = models.IntegerField(default=1)
    tocken = models.CharField(max_length=1000, null=True, blank=True)
    date_of_birth = models.DateField(null=True)
    
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