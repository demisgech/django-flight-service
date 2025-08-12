from django.conf import settings
from django.db import models


# Create your models here.    

class Log(models.Model):
    message = models.TextField()
    log_date = models.DateTimeField(auto_now_add=True)
    log_type = models.CharField(max_length=20)
    severity_level = models.CharField(max_length=20)
        

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    message = models.TextField()
    sent_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10,choices=[
        ('read','Read'),
        ('unread','Unread')
    ])