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
def get_user_permission(e_id):
    tabs = []
    for t in Tabs.objects.all():
        tabs_permission = 0
        if Tab_permissions.objects.filter(employee=e_id,tab=t, status=1).exists():
            tabs_permission = 1
        tabs.append({
            'id':t.id,
            'name':t.name,
            'user_permission':tabs_permission
        })
    return {
            'tabs':tabs
            }


