from django.urls import path
from .views import *
#
urlpatterns=[
    path('index/',index),
    path('alogin/',alogin),
    # path('cregis/',cregis),
    path('sendmail/',sendmail),
    path('verify/<token>',verify),
    # path('error/',error),
    path('clogin/',clogin),
    path('adlogin/',adindex),
    path('custlogin/',custlogin),
    path('addmcus/',admcus),
    path('cviews/',cviews),
    path('adcon/',adconn),
    path('adb/',adb),
    path('addbill/<int:obj2>/',addbill,name='addbill'),
    path('cfeed/',cfeed),
    path('conviews/',conviews),
    path('billv/',billv),
    path('cust/',custindex),
    path('qpay/',qpay),
    path('passw/<id>',passw),
    path('cbillv',cbillv),
    path('billpay/<id>',billpay),
    path('qpay/<id>',qpay),
    path('payment/<id>', payment),
    path('hbill/<id>', hbill),
    path('addconnect/<int:obj2>/',addconnect, name='addconnect'),
    path('cbillv/<int:id>/',cbillv, name='cbillv'),




]