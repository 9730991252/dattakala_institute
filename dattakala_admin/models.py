from django.db import models
from office.models import Employee
# Create your models here.
class Visitor(models.Model):
    added_by = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    visitor_name = models.CharField(max_length=100)
    visitor_mobile = models.IntegerField()
    visitor_address = models.CharField(max_length=100)
    
class Appointment(models.Model):
    added_by = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE)
    visit_reason = models.CharField(max_length=100)
    book_date_time = models.DateTimeField(auto_now_add=True)
    meeting_start_time = models.DateTimeField(null=True)
    meeting_end_time = models.DateTimeField(null=True)
    order_by = models.IntegerField(null=True)
    meat_to = models.CharField(max_length=100)
    meeting_status = models.IntegerField(default=0) #0 = waiting, 1 = Running ,2 = completed, 3 = cancelled,