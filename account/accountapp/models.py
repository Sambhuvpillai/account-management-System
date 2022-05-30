from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
# Create your models here.
class Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_address = models.CharField(max_length=255)
    user_gender = models.CharField(max_length=150)
    user_mobile= models.CharField(max_length=255)
    user_photo=models.ImageField(upload_to='image/',null=True,blank=True)
    DOB =models.DateField()
    
    

    
class Leave(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    startdate = models.DateField()
    enddate = models.DateField()
    reason = models.CharField(max_length=255)
    status = models.BooleanField(default=False)
    
	