import uuid
import time
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse
from .forms import *
from .models import *
from electricity_billing.settings import EMAIL_HOST_USER
# from signal import signal,SIGPIPE,SIG_DFL
# signal(SIGPIPE,SIG_DFL)




def adindex(request):
    a = Profile.objects.all()
    return render(request, 'adminindex.html', {'a': a})


def cuindex(request,id):
    c=Profile.objects.filter(id=id).first()
    return render(request,'custindex.html',{'c':c})


# Create your views here.

def index(request):
    logout(request)
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
                return redirect(alogin)
        else:
            return redirect(alogin)
    else:
        return render(request, 'authenticate/adlogin.html')


def clogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        cnumber = request.POST.get('cnumber')
        if not (User.objects.filter(username=username)):
            messages.success(request, "incorrect username")
            return redirect(clogin)
        user = User.objects.get(username=username)
        if not (conmodel.objects.filter(cnumber=cnumber)):
            messages.success(request, "incorrect username/cnumber")
            return redirect(clogin)

        cm = conmodel.objects.get(profile__user=user, cnumber=cnumber)
        fn = cm.profile.user.first_name
        em = username
        token = str(uuid.uuid4())
        cm.profile.auth_token = token
        if cm.profile.is_verified:
            messages.success(request, "this account is already created kindly login")
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
        c = profile_obj
        print(c)
        login(request, user)
        return render(request, 'custindex.html',{'c': c})
    return render(request, 'authenticate/logincust.html')


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
        un=a.user.username
        em=a.user.email
        cmodel.save()
        sendconmail(cnumber,un,em)
        return redirect(conviews)
    return render(request, 'pycon.html', {'a': a})


def sendconmail(cn,un,em):
    subject="your connection is ready"
    message=f'HELLO user            ' \
            f'your username is {un}             ' \
            f'your consumer number is {cn}             '
    email_from=EMAIL_HOST_USER
    recipient=[em]
    send_mail(subject,message,email_from,recipient)


def conviews(request):
    a = conmodel.objects.all()
    return render(request, 'viewcon.html', {'a': a})



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
        byear=request.POST['byear']
        cread = request.POST['cread']
        tunit = request.POST['tunit']
        pread = request.POST['pread']
        cpu = request.POST['cpu']
        amount = request.POST['amount']
        ddate = request.POST['ddate']

        if Bill.objects.filter(bmonth=bmonth).first():
            if Bill.objects.filter(byear=byear).first():
                messages.success(request, 'bill already entered')
                return redirect(adb)
        bills = Bill(connmodel=a, bmonth=bmonth,byear=byear,cread=cread, pread=pread, tunit=tunit, cpu=cpu, amount=amount,
                     ddate=ddate)
        bills.save()
        return redirect(billv)
    return render(request, 'adbill.html', {'a': a})


def billv(request):
    a = Bill.objects.all()

    return render(request, 'viewbill.html', {'a': a})


@login_required(login_url="/billingapp/custlogin/")
def custindex(request):
    a = request.user
    c=Profile.objects.filter(id=id).first()
    print(a)
    return render(request, 'custindex.html',{'a': a, 'c': c})


@login_required(login_url="/billingapp/custlogin/")
def qpay(request, id):
    a = Bill.objects.filter(connmodel__profile__id=id).first()
    if request.method == "POST":
        acc = request.POST.get('cdnumber')
        ed = request.POST.get('edate')
        cvv = request.POST.get('cvv')
        cn = request.POST.get('cname')
        print(1)
        c=Profile.objects.filter(id=id).first()

        a.pstatus = "paid"
        a.save()
        print(2)
        obj = Payment(bill=a, cdnumber=acc, edate=ed, cvv=cvv, cname=cn)
        obj.save()
        url = reverse('cbillv', kwargs={'id': id})
        return redirect(url)
    return render(request, 'pay.html', {'a': a})


@login_required(login_url="/billingapp/custlogin/")
def cbillv(request, id):
    a = Bill.objects.filter(pstatus='not 45paid', connmodel__profile__id=id).first()
    print(a)
    c=Profile.objects.filter(id=id).first()
    if a is None:
        print('aqwertyujy')
        messages.success(request, "nothing to show")
        return render(request, 'cbillview.html', {'c': c})
    else:

        print(a)
        action = "pay now"
        return render(request, 'cbillview.html', {'a': a, 'c': c, 'action': action})


@login_required(login_url="/billingapp/custlogin/")
def billpay(request, id):
    a = Bill.objects.filter(pstatus='not paid', connmodel__profile__id=id).first()
    b = Bill.objects.filter(connmodel__profile__id=id).first()
    c = Profile.objects.filter(id=id).first()
    print(a)
    if a is None:

        messages.success(request, "nothing to show")
        a = b

        return render(request, 'cbillview.html', {'a': a, 'c': c})
    else:

        print(a)
        action = "pay now"
        return render(request, 'cbillview.html', {'a': a, 'c': c, 'action': action})


@login_required(login_url="/billingapp/custlogin/")
def payment(request, id):
    if request.method == "POST":
        acc = request.POST.get('cdnumber')
        ed = request.POST.get('edate')
        cvv = request.POST.get('cvv')
        cn = request.POST.get('cname')
        print(1)

        a = Bill.objects.filter(connmodel__profile__id=id).first()
        a.pstatus = "paid"
        a.save()
        print(2)
        obj = Payment(bill=a, cdnumber=acc, edate=ed, cvv=cvv, cname=cn)
        obj.save()
        url = reverse('cbillv', kwargs={'id': id})
        return redirect(url)


@login_required(login_url="/billingapp/custlogin/")
def hbill(request, id):
    # id=request.user.id
    # print(3)
    a = Bill.objects.filter(pstatus='paid', connmodel__profile__id=id).first()
    b = Bill.objects.filter(connmodel__profile__id=id).first()
    c=Profile.objects.filter(id=id).first()
    if a is None:
        messages.success(request, "nothing to show")
        a = b
        return render(request, 'hbill.html', {'a': a, 'c': c})
    else:
        action = "pay now"
        return render(request, 'hbill.html', {'a': a, 'c': c, 'action': action})


@login_required(login_url="/billingapp/custlogin/")
def profile(request, id):
    a = conmodel.objects.filter(profile__id=id).first()
    c=Profile.objects.filter(id=id).first()

    li=[]
    path=a.profile.img
    print(path)
    l=(str(path).split("/")[-1])
    list=l
    print(l)
    return render(request, 'profile.html', {'a': a,'list':list, 'c': c})

@login_required(login_url="/billingapp/custlogin/")
def comp(request, id):
    a = conmodel.objects.filter(profile__id=id).first()
    c=Profile.objects.filter(id=id).first()
    b=complaint.objects.filter(conmodel__profile__id=id)
    if request.method == "POST":
        comp = request.POST.get('comp')
        obj = complaint(conmodel=a, comp=comp)
        obj.save()
        messages.success(request, 'complaint registered successfully')
        url=reverse('vcomp', kwargs={'id': id})
        return redirect(url)
    else:
        return render(request, 'addcomp.html', {'a': a, 'c': c})

@login_required(login_url="/billingapp/custlogin/")
def vcomp(request,id):
    c=Profile.objects.filter(id=id).first()
    # a=[]
    # for i in complaint:
    b=complaint.objects.filter(conmodel__profile__id=id)
    print(b)
    return render(request,'vpcomp.html',{'b':b,'c':c})


@login_required(login_url="/billingapp/custlogin/")
def cfeed(request,id):
    a = conmodel.objects.filter(profile__id=id).first()
    c=Profile.objects.filter(id=id).first()
    b=feedb.objects.filter(conmodel__profile__id=id)
    if request.method == "POST":
        feed = request.POST.get('feed')
        obj = feedb(conmodel=a, feed=feed)
        obj.save()
        messages.success(request, 'feedback registered successfully')
        url=reverse('vfeed', kwargs={'id': id})
        return redirect(url)
    else:
        return render(request, 'addfeed.html', {'a': a, 'c': c})

@login_required(login_url="/billingapp/custlogin/")
def vfeed(request,id):
    c=Profile.objects.filter(id=id).first()
    # a=[]
    # for i in complaint:
    b=feedb.objects.filter(conmodel__profile__id=id)
    if b:

        print(b)
        return render(request,'vpfeed.html',{'b':b,'c':c})
    else:
        return render(request, 'vpfeed.html', {'b': b, 'c': c})

def adfeed(request):
    a=feedb.objects.all()
    return render(request,'adfeed.html',{'a':a})

def adcomp(request):
    a=complaint.objects.all()
    return render(request,'adcomp.html',{'a':a})

@login_required(login_url="/billingapp/custlogin/")
def edphoto(request,id):
    a=conmodel.objects.filter(profile__id=id).first()
    c=User.objects.filter(id=id).first()
    if request.method=="POST":
        b=prof(request.POST,request.FILES)
        if b.is_valid():
            im=b.cleaned_data['img']
            a.profile.img=im
            a.profile.save()
            print(a.profile.img)
            messages.success(request,"profile picture edited successfully")
            url = reverse('profile', kwargs={'id': id})
            return redirect(url)
    return render(request,'editphoto.html',{'a':a,'c':c})



@login_required(login_url="/billingapp/custlogin/")
def edpes(request, id):
    a = Profile.objects.filter(id=id).first()
    print(a)
    c=Profile.objects.filter(id=id).first()
    print(c)
    profile_obj = Profile.objects.filter(id=id).first()
    print(profile_obj)
    # print(user.id)
    if request.method == "POST":
        profile_obj.user.first_name = request.POST.get('fname')
        profile_obj.user.last_name = request.POST.get('lname')
        profile_obj.user.email = request.POST.get('email')
        profile_obj.user.username = request.POST.get('username')
        profile_obj.add = request.POST.get('add')
        profile_obj.gender = request.POST.get('gender')
        profile_obj.mnumber = request.POST.get('mnumber')
        profile_obj.city = request.POST.get('city')
        profile_obj.state = request.POST.get('state')
        profile_obj.pin = request.POST.get('pin')
        profile_obj.user.save()
        profile_obj.save()
        url = reverse('profile', kwargs={'id': id})
        return redirect(url)
    else:
        return render(request, 'edpes.html', {'a': a})


def regdel(request,id):
    un=Profile.objects.get(id=id)
    print(id)
    e=un.user.username
    print(e)
    u=User.objects.get(username=e)
    print(un.user.username)
    u.delete()
    return redirect(cviews)


def condel(request,id):
    un=conmodel.objects.get(id=id)
    print(un)
    un.delete()
    return redirect(conviews)



