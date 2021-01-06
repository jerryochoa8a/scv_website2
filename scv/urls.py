from scv.views import appt
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('appt', views.appt),
    path('about', views.about),
    path('login', views.login),
    path('register', views.register),
    path('contactUs', views.contactUs),
    path('loginAction', views.loginAction),
    path('reg', views.reg),
    path('logout', views.logout),
    path('account/<custId>', views.account),
    path('makeAppt', views.makeAppt),
    path('sendEmail',views.sendEmail),

    #admin
    path('admin/customer/<custId>', views.customerInfo),
    path('admin/cancelJob/<custId>', views.cancelJob),
    path('admin/addCalendar/<custId>/<keyWord>', views.addCalendar),
    path('admin/addCalendarNext/<custId>/<keyword>', views.addCalendarNext),
    path('admin/assign/<custId>/<dayNum>/<monthNum>/<keyWord>', views.assignAppt),
    path('admin/note/<custId>', views.note),
    path('admin/calender', views.calendarPage),
    path('admin/nextCalender', views.nextCalenderPage),
    path('admin/today/list', views.todayList),
    path('admin/cal/info/<day>', views.dateInfo),
    path('admin/addpart/<custId>', views.addPart),
    path('admin/complete/true/<partId>/<custId>', views.partTrue),
    path('admin/complete/false/<partId>/<custId>', views.partFalse),
    
]