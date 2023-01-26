import uuid
import time
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse
from .forms import *
from .models import *
from electricity_billing.settings import EMAIL_HOST_USER


def adindex(request):
    a = Profile.objects.all()
    return render(request, 'adminindex.html', {'a': a})


def cuindex(request):
    return render(request, 'custindex.html')


# Create your views here.

def index(request):
    return render(request, 'index.html')


def alogin(request):
    if request.method == "POST":
        a = alogform(request.POST)
        if a.is_valid():
            un = a.cleaned_data['username']
            ps = a.cleaned_data['password']
            b = alog.objects.all()
            for i in b:
                if un == i.username and ps == i.password:
                    messages.success(request, 'login success')
                    a = Profile.objects.all()
                    return render(request, 'adminindex.html', {'a': a})
                else:
                    messages.success(request, 'incorrect username or password')
                    return redirect(alogin)
        else:
            # return HttpResponse('incorrect credentials')
            return redirect(alogin)
    else:
        return render(request, 'adlogin.html')


# def cregis(request):
#     if request.method=="POST":
#         fn = request.POST.get('fname')
#         ln = request.POST.get('lname')
#         un=request.POST.get('username')
#         cn=request.POST.get('cnumber')
#         em=request.POST.get('email')
#         mn=request.POST.get('mnumber')
#         ps=request.POST.get('password')
#         cp=request.POST.get('cpassword')
#         if ps==cp:
#             if User.objects.filter(username=un).first():
#                 messages.success(request,'username already exist')
#                 return redirect(cregis)
#             if User.objects.filter(email=em).first():
#                 messages.success(request,"email already exist")
#                 return redirect(cregis)
#             user_obj=User(username=un,email=em,first_name=fn,last_name=ln)
#             user_obj.set_password(ps)
#             user_obj.save()
#             auth_token=str(uuid.uuid4())
#             profile_obj=Profile.objects.create(user=user_obj,cnumber=cn,mnumber=mn,auth_token=auth_token)
#             profile_obj.save()
#             messages.success(request,'check ur email')
#             sendmail(fn,em,auth_token)
#         else:
#             messages.success(request,"password doesnt match")
#             return redirect(cregis)
#     return render(request,'creg.html')

# def sendmail(fn,em,token):
#     subject="your account has been verified"
#     message=f'HELLO {fn}' \
#             f'paste the link to verify the account http://127.0.0.1:8000/billingapp/verify/{token}'
#     email_from=EMAIL_HOST_USER
#     recipient=[em]
#     send_mail(subject,message,email_from,recipient)

# def verify(request,auth_token):
#     profile_obj=Profile.objects.filter(auth_token=auth_token).first()
#     if profile_obj:
#         if profile_obj.is_verified:
#             messages.success(request,'ur account is already verified')
#             return redirect(clogin)
#         profile_obj.is_verified=True
#         profile_obj.save()
#         messages.success(request,'your account is verified')
#         return redirect(clogin)
#     else:
#         return redirect(error)


# def error(request):
#     return render(request,'error.html')


def clogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        cnumber = request.POST.get('cnumber')
        if not (User.objects.filter(username=username)):
            messages.success(request, "incorrect username")
            return redirect(clogin)
        user=User.objects.get(username=username)
        if not (conmodel.objects.filter(cnumber=cnumber)):
            messages.success(request, "incorrect username/cnumber")
            return redirect(clogin)

        cm = conmodel.objects.get(profile__user=user, cnumber=cnumber)
        fn = cm.profile.user.first_name
        em = username
        token = str(uuid.uuid4())
        cm.profile.auth_token = token
        if cm.profile.is_verified:
            messages.success(request,"this account is already created kindly login")
            return redirect(clogin)
        else:
            cm.profile.save()
            sendmail(fn, em, token)
            messages.success(request, 'check your inbox for email verification')
            return redirect(clogin)
    else:
        return render(request, 'cuslogin.html')


def sendmail(fn, em, token):
    subject = "your account has been verified"
    message = f'HELLO {fn}' \
              f'paste the link to verify the account http://127.0.0.1:8000/billingapp/verify/{token}'
    email_from = EMAIL_HOST_USER
    recipient = [em]
    send_mail(subject, message, email_from, recipient)


def verify(request, token):
    profile_obj = Profile.objects.filter(auth_token=token).first()
    if profile_obj:
        if profile_obj.is_verified:
            messages.success(request, 'ur account is already verified')
            return redirect(custlogin)
        profile_obj.is_verified = True
        profile_obj.save()
        id = profile_obj.id
        messages.success(request, 'your account is verified,')
        return render(request, 'redirection.html', {'id': id})
        url = reverse('passw', kwargs={'id': id})
        return redirect(url)
    else:
        return HttpResponse("errrrrorrrrrr")

@login_required
def custlogin(request):
    if request.method == "POST":
        un = request.POST.get('username')
        ps = request.POST.get('password')
        user_obj = User.objects.filter(username=un).first()
        if user_obj is None:
            messages.success(request, 'user not found')
            return redirect(custlogin)
        profile_obj = Profile.objects.filter(user=user_obj).first()
        if not profile_obj.is_verified:
            messages.success(request, 'profile not verified check ur email')
            return redirect(custlogin)
        user = authenticate(username=un, password=ps)
        print(user)
        if user is None:
            messages.success(request, "wrong password or username")
            return redirect(custlogin)
        a=user
        print(a)
        return render(request, 'custindex.html', {'a': a})
    return render(request, 'logincust.html')


def passw(request, id):
    if request.method == "POST":
        ps = request.POST.get('password')
        cp = request.POST.get('cpassword')
        if ps == cp:
            profile_obj = Profile.objects.filter(id=id).first()
            profile_obj.user.set_password(ps)
            profile_obj.user.save()
            return redirect(custlogin)
        else:
            messages.success(request, "password doesnt match")

    return render(request, 'cpass.html')


def admcus(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        mnumber = request.POST.get('mnumber')
        gender = request.POST.get('gender')
        email = request.POST.get('email')
        address = request.POST.get('add')
        cit = request.POST.get('city')
        state = request.POST.get('state')
        pin = request.POST.get('pin')
        if User.objects.filter(email=email).first():
            messages.error(request, 'email already exist with another account')
            return redirect(admcus)
        username = email
        userobj = User(first_name=fname, last_name=lname, email=email, username=username)
        userobj.save()
        profileobj = Profile.objects.create(user=userobj, mnumber=mnumber, gender=gender, add=address, city=cit,
                                            state=state, pin=pin)
        profileobj.save()
        messages.success(request, 'registration success')
        return redirect(cviews)
    return render(request, 'add customer.html')


def cviews(request):
    a = Profile.objects.all()
    return render(request, 'cview.html', {'a': a})


def adconn(request):
    if request.method == "POST":
        email = request.POST.get('email')
        obj1 = Profile.objects.get(user__email=email)
        obj2 = obj1.id
        print(obj2)
        url = reverse('addconnect', kwargs={'obj2': obj2})
        return redirect(url)
    else:
        a = Profile.objects.all()
        return render(request, 'adcon.html', {'a': a})


def addconnect(request, obj2):
    obj1 = obj2
    a = Profile.objects.get(id=obj1)
    if request.method == "POST":
        cnumber = request.POST['cnumber']
        ctype = request.POST['ctype']
        cdate = request.POST['cdate']
        occ = request.POST['occ']
        load = request.POST['load']
        hnumber = request.POST['hnumber']
        des = request.POST['des']

        if conmodel.objects.filter(id=a.id).first():
            messages.success(request, 'user already have a connection')
            return redirect(adconn)
        cmodel = conmodel(profile=a, cnumber=cnumber, ctype=ctype, cdate=cdate, occ=occ, load=load, hnumber=hnumber,
                          des=des)
        cmodel.save()
        return redirect(conviews)
    return render(request, 'pycon.html', {'a': a})


def conviews(request):
    a = conmodel.objects.all()
    return render(request, 'viewcon.html', {'a': a})

    # if request.method=="POST":

    # quantity = request.POST['quantity']
    # total_price = request.POST['total_price']
    # bill = Bill(product=product, quantity=quantity, total_price=total_price)
    # bill.save()
    # return redirect('bill_list')

    #     return HttpResponse("success")
    # else:


# def createbill(request):
#     if request.method == 'POST':
#         object = Profile.objects.get(user__email=request.POST['email'])
#         print(object)
#         quantity = request.POST['quantity']
#         total_price = request.POST['total_price']
#         bill = Bill(profile=object, quantity=quantity, total_price=total_price)
#         bill.save()
#         return HttpResponse('success')
#     else:
#         a = Profile.objects.all()
#         return render(request,'work1.html',{'a':a})


def cfeed(request):
    if request.method == "POST":
        cnumber = request.POST.get('cnumber')
        email = request.POST.get('email')
        feed = request.POST.get('feed')
        cfeed_obj = feedb(cnumber=cnumber, email=email, feed=feed)
        cfeed_obj.save()
    return render(request, 'feedback.html')

def adb(request):
    if request.method == "POST":
        cnumber = request.POST.get('cnumber')

        if conmodel.objects.filter(cnumber=cnumber).first():
            obj1 = conmodel.objects.get(cnumber=cnumber)
            obj2 = obj1.id
            print(obj2)
            url = reverse('addbill', kwargs={'obj2': obj2})
            return redirect(url)
        else:
            messages.error(request, 'customer/connnection not found')
            return redirect(adb)
    else:
        a = conmodel.objects.all()
        return render(request, 'adb.html', {'a': a})

def addbill(request, obj2):
    obj1 = obj2
    a = conmodel.objects.get(id=obj1)
    if request.method == "POST":
        bmonth = request.POST['bmonth']
        cread = request.POST['cread']
        tunit = request.POST['tunit']
        pread = request.POST['pread']
        cpu = request.POST['cpu']
        amount = request.POST['amount']
        ddate = request.POST['ddate']

        if Bill.objects.filter(connmodel__cnumber=a.cnumber).first():
            messages.success(request, 'bill already entered')
            return redirect(adb)
        bills = Bill(connmodel=a, bmonth=bmonth, cread=cread, pread=pread, tunit=tunit, cpu=cpu, amount=amount,
                     ddate=ddate)
        bills.save()
        return redirect(billv)
    return render(request, 'adbill.html', {'a': a})


def billv(request):
    a = Bill.objects.all()

    return render(request, 'viewbill.html', {'a': a})



def custindex(request):
    a = request.user
    print(a)
    return render(request, 'custindex.html', {'a': a})


def qpay(request,id):
    a = Bill.objects.filter(connmodel__profile__user__id=id).first()
    if request.method=="POST":
        acc=request.POST.get('cdnumber')
        ed = request.POST.get('edate')
        cvv=request.POST.get('cvv')
        cn=request.POST.get('cname')
        print(1)


        a.pstatus = "paid"
        a.save()
        print(2)
        obj = Payment(bill=a, cdnumber=acc, edate=ed, cvv=cvv, cname=cn)
        obj.save()
        url = reverse('cbillv', kwargs={'id': id})
        return redirect(url)
    return render(request,'pay.html',{'a':a})


def cbillv(request,id):
    a = Bill.objects.filter(pstatus='not paid',connmodel__profile__user__id=id).first()
    print(a)
    if a is None:
        print('aqwertyujy')
        messages.success(request, "nothing to show")
        return render(request, 'cbillview.html')
    else:

        print(a)
        action="pay now"
        return render(request,'cbillview.html',{'a':a,'action':action})


def billpay(request,id):

    a = Bill.objects.filter(pstatus='not paid',connmodel__profile__user__id=id).first()
    b=Bill.objects.filter(connmodel__profile__user__id=id).first()
    print(a)
    if a is None:

        messages.success(request, "nothing to show")
        a=b

        return render(request, 'cbillview.html',{'a':a})
    else:

        print(a)
        action="pay now"
        return render(request,'cbillview.html',{'a':a,'action':action})


def payment(request,id):
    if request.method=="POST":
        acc=request.POST.get('cdnumber')
        ed = request.POST.get('edate')
        cvv=request.POST.get('cvv')
        cn=request.POST.get('cname')
        print(1)

        a = Bill.objects.filter(connmodel__profile__user__id=id).first()
        a.pstatus="paid"
        a.save()
        print(2)
        obj=Payment(bill=a,cdnumber=acc,edate=ed,cvv=cvv,cname=cn)
        obj.save()
        url = reverse('cbillv', kwargs={'id': id})
        return redirect(url)



def hbill(request,id):
    # id=request.user.id
    # print(3)
    a = Bill.objects.filter(pstatus='paid',connmodel__profile__user__id=id).first()
    b=Bill.objects.filter(connmodel__profile__user__id=id).first()
    if a is None:
        messages.success(request,"nothing to show")
        a=b
        return render(request, 'hbill.html',{'a':a})
    else:
        action="pay now"
        return render(request,'hbill.html',{'a':a,'action':action})



