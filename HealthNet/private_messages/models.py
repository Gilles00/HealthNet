from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Message(models.Model):
    title = models.CharField(max_length=30)
    message = models.CharField(max_length=400)
    time = models.DateTimeField('time')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    is_opened = models.BooleanField()