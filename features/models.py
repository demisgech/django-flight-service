from django.conf import settings
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class RelatedObjectMixin(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        abstract = True
  

class Log(RelatedObjectMixin):
    message = models.TextField()
    log_date = models.DateTimeField(auto_now_add=True)
    log_type = models.CharField(max_length=20)
    severity_level = models.CharField(max_length=20)
        

class Notification(RelatedObjectMixin):
    NOTIFICATION_STATUS = [
        ('read','Read'),
        ('unread','Unread')
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    message = models.TextField()
    sent_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10,choices=NOTIFICATION_STATUS,default='unread')
