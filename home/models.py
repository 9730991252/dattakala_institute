from django.db import models

# Create your models here.
class Self_registration_qr_count(models.Model):
    count = models.IntegerField(default=1)
    def __str__(self):
        return str(self.count)