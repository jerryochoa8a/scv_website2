from django.contrib import admin
from django.db import models
from scv.models import User, Appt, Part
from django.shortcuts import render, redirect
from django.urls import path
from datetime import datetime
from datetime import date

# Register your models here.
class CustListModel(models.Model):

    class Meta:
        verbose_name_plural = 'Customer List'
        app_label = 'scv'

def my_custom_view(request):
    if not request.user.has_perm('poll.change_poll'):
        return redirect('/')
    else:
        appt_check = Appt.objects.filter(called = True)
        month = datetime.now().month
        year = datetime.now().year
        day = datetime.now().day
        
        if appt_check.exists():
            for  appt in appt_check:
                # if appt.monthNum
                if appt.calNum < day or appt.monthNum < datetime.now().month:
                    print("Appt have been moved up!")
                    appt.apptDate = datetime.now()
                    appt.calNum = day
                    appt.save()
        else:
            print("-------")
            print("QuerySet is Empty")
            print("-------")
            

        context = {
            "apptList": Appt.objects.filter(called=False),
            "diagnos": Appt.objects.filter(diagnosedBol=True),
            "parts": Appt.objects.filter(partsBol=True),
            "finish": Appt.objects.filter(finishBol=True),
        }
    return render(request, 'admin/admin-list.html', context)

class CustListModelAdmin(admin.ModelAdmin):
    model = CustListModel

    def get_urls(self):
        view_name = '{}_{}_changelist'.format(
            self.model._meta.app_label, self.model._meta.model_name)
        return [
            path('my_admin_path/', my_custom_view, name=view_name),
        ]
admin.site.register(CustListModel, CustListModelAdmin)


class TVModel(models.Model):

    class Meta:
        verbose_name_plural = 'TV'
        app_label = 'scv'

def tv(request):
    today = date.today().strftime('%A %B %d %Y')
    time = datetime.now().time().strftime("%I:%M %p")
    context ={
        'appts': Appt.objects.filter(apptDate = datetime.now())[:4],
        'today': today,
        'time': time
    }
    return render(request, 'admin/admin-TV.html', context)

class TVModelAdmin(admin.ModelAdmin):
    model = TVModel

    def get_urls(self):
        view_name = '{}_{}_changelist'.format(
            self.model._meta.app_label, self.model._meta.model_name)
        return [
            path('my_admin_path/TV', tv, name=view_name),
        ]
admin.site.register(TVModel, TVModelAdmin)

