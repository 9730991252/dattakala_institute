from django import template
register = template.Library()
from django.db.models import Avg, Sum, Min, Max
from math import *
import math
import datetime
from datetime import datetime, date, time

from sunil.models import *
from office.models import * 
from num2words import num2words


@register.simple_tag()
def check_student_approval(student):
    student_approval = Student_approval.objects.filter(student=student).first()
    print(student_approval)
    if student_approval:
        if student_approval.office_approval_status == 1 or student_approval.account_approval_status == 1 or student_approval.store_approval_status == 1:
            return False
    return True