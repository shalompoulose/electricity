from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class alog(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    img=models.FileField(upload_to='billingapp/static/assets/img/profile')
    mnumber = models.CharField(max_length=50)
    gender=models.CharField(max_length=50)
    add=models.CharField(max_length=100)
    city=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    pin=models.CharField(max_length=50)

class conmodel(models.Model):
    profile=models.ForeignKey(Profile, on_delete=models.CASCADE)
    cnumber=models.CharField(max_length=50)
    ctype = models.CharField(max_length=50)
    cdate = models.CharField(max_length=50)
    occ = models.CharField(max_length=50)
    load = models.CharField(max_length=50)
    hnumber = models.CharField(max_length=50)
    des = models.CharField(max_length=100)

class feedb(models.Model):
    conmodel=models.ForeignKey(conmodel,on_delete=models.CASCADE)
    feed=models.CharField(max_length=500)
    date=models.DateTimeField(auto_now_add=True)

class Bill(models.Model):
    connmodel=models.ForeignKey(conmodel, on_delete=models.CASCADE)
    bmonth=models.CharField(max_length=50)
    byear=models.CharField(max_length=30)
    cread=models.IntegerField()
    pread=models.IntegerField()
    tunit=models.IntegerField()
    cpu=models.IntegerField()
    amount=models.IntegerField()
    ddate=models.CharField(max_length=50)
    pstatus=models.CharField(max_length=50,default="not paid")


class Payment(models.Model):
    bill=models.ForeignKey(Bill,on_delete=models.CASCADE)
    cdnumber=models.CharField(max_length=30)
    edate=models.CharField(max_length=30)
    cvv=models.CharField(max_length=30)
    cname=models.CharField(max_length=50)


class complaint(models.Model):
    conmodel=models.ForeignKey(conmodel,on_delete=models.CASCADE)
    comp=models.CharField(max_length=500)
    date=models.DateTimeField(auto_now_add=True)







