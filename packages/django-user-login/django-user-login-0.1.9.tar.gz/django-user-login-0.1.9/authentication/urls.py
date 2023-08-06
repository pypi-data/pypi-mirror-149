from django.urls import path, include
from . import views

app_name = 'authentication'

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view_js),
    path('logout/', views.logout_view, name='logout'),
    path('logoutJS/', views.logout_view_js, name="logoutJS"),

    path('register/', views.register),
    path('register/cancel/', views.cancelRegistration),
    path('register/resend/', views.resendVerificationCode),
    path('register/verify/', views.verifyRegistration),

    path('recover/', views.recover),
    path('recover/cancel/', views.cancelRecovery),
    path('recover/resend/', views.resendRecoveryCode),
    path('recover/verify/', views.verifyRecovery),
    path('recover/changepassword/', views.changepassword),

    path('<str:username>/', views.account, name='account'),
    path('<str:username>/details/', views.details),
    path('<str:username>/details/edit/', views.editDetails),
    path('<str:username>/details/edit/check/', views.emailsecuritycheck),
    path('<str:username>/details/edit/check/confirm/', views.emailsecurityconfirm),
    path('<str:username>/details/edit/check/email/', views.checkemail),
    path('<str:username>/details/edit/check/email/resend/', views.reconfirmCheckemail),
    path('<str:username>/details/edit/check/email/cancel/', views.cancelCheckemail),
    path('<str:username>/details/edit/check/email/change/', views.changeEmail),
    path('<str:username>/details/edit/change/password/', views.changePassword),
]
