# cd..
# jerryEnv\Scripts\activate
# cd scv_website
# manage.py runserver
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from scv.models import User, Appt, Part
from django.contrib import messages
import bcrypt
import datetime, calendar
from datetime import datetime
import json

#not a robot
from django.conf import settings
import urllib

import urllib.request as urllib2
import json



####PAGES####
def home(request):
    if "userid" not in request.session:
        request.session['userid'] = None
    if request.session['userid'] == None:
        return render(request, 'home.html')
    else:
        context = {
            "user": User.objects.get(id=request.session['userid']),
        }

        return render(request, 'home.html', context)


def login(request):
    if request.session['userid'] == None:
        return render(request, 'login.html')
    else:
        context = {
            "user": User.objects.get(id=request.session['userid']),
        }
        return render(request, 'login.html', context)


def register(request):
    if request.session['userid'] == None:
        return render(request, 'register.html')
    else:
        context = {
            "user": User.objects.get(id=request.session['userid']),
        }
        return render(request, 'register.html', context)


def account(request, custId):
    user = User.objects.get(id=custId)
    num = user.phone

    appt = Appt.objects.filter(user=user).last()

    year = datetime.now().year #current year
    month = datetime.now().month #current month
    
    date1 = None
    date2 = None

    if appt == None or appt.apptDate == None:
        print("Processing")
    else:
        weekday = appt.apptDate.weekday()
        month = appt.monthNum 
    
        end_day_month = calendar.monthrange(year, month)[1]

        monday = appt.calNum
        friday = appt.calNum - 2
        prev_month = False
        next_month = False
        for i in range(6):
            if i < weekday: 
                monday = monday - 1
                if monday < 0:
                    if month == 1:
                        monday = calendar.monthrange(year, 12)[1]
                        prev_month = True
                    else:
                        monday = calendar.monthrange(year, month-1)[1]
                        prev_month = True
            else:
                friday = friday + 1
                if friday > end_day_month:
                    friday = 1
                    next_month = True
        if prev_month == True:
            if month == 1:
                date1 = datetime(year, 12, monday).date
            else:
                date1 = datetime(year, month - 1, monday).date
        else:
            date1 = datetime(year, month, monday).date

        if next_month == True:
            if month == 12:
                date2 = datetime(year+1, 1, friday).date
            else:
                date2 = datetime(year, month + 1, friday).date
        else:
            date2 = datetime(year, month, friday).date

    phoneNumber = format(int(num[:-1]), ",").replace(",", "-") + num[-1]
    context = {
        'user': user,
        'phone': phoneNumber,
        'appt': Appt.objects.filter(user=user).last(),
        'date1': date1,
        'date2': date2,
    }
    return render(request, 'account.html', context)


def contactUs(request):
    if request.session['userid'] == None:
        return render(request, 'contactUs.html')
    else:
        context = {
            "user": User.objects.get(id=request.session['userid']),
        }
        return render(request, 'contactUs.html', context)


def appt(request):
    if request.session['userid'] == None:
        return render(request, 'appt.html')
    else:
        context = {
            "user": User.objects.get(id=request.session['userid']),
        }
        return render(request, 'appt.html', context)


def about(request):
    if request.session['userid'] == None: 
        return render(request, 'about.html')
    else:
        context = {
            "user": User.objects.get(id=request.session['userid']),
        }
        return render(request, 'about.html', context)


### Functions ###

def loginAction(request):
    user = User.objects.filter(email=request.POST['email'])
    if user:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['pass'].encode(), logged_user.password.encode()):
            request.session['userid'] = logged_user.id
            return redirect("/")
        else:
            messages.error(request, "Incorrect email or password.")
            return redirect('/login')
    else:
        messages.error(request, "Incorrect email or password.")
    return redirect('/login')


def reg(request):
    errors = Part.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
            return redirect('/register')
    else:
        if request.POST['conPass'] != request.POST['pass']:
            messages.error(request, "Please confirm your password.")
            return redirect('/register')
        else:
            password = request.POST['pass']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            User.objects.create(
                    fname=request.POST['fname'],
                    lname=request.POST['lname'],
                    city=request.POST['city'],
                    phone=request.POST['phone'],
                    email=request.POST['email'],
                    password=pw_hash
                )
            return redirect('/login')


def logout(request):
    request.session['userid'] = None
    return redirect('/')


def makeAppt(request):
    errors = Part.objects.appt_validator(request.POST)
    
    recaptcha_response = request.POST.get('g-recaptcha-response')
    url = 'https://www.google.com/recaptcha/api/siteverify'
    values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
    data = urllib.parse.urlencode(values).encode()
    req =  urllib.request.Request(url, data=data)
    response = urllib.request.urlopen(req)
    result = json.loads(response.read().decode())

    print("-------")
    print(response)
    print("-------")


    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
            return redirect('/appt')
    elif result['success'] == False:
        messages.error(request, "Sorry no Robots! Please click the Checkbox")
        return redirect('/appt')
    else:
        if request.session['userid'] == None:
            n = request.POST['phone']
            phoneNumber = format(int(n[:-1]), ",").replace(",", "-") + n[-1]
            Appt.objects.create(
                fname=request.POST['fname'],
                lname=request.POST['lname'],
                phone= phoneNumber,
                city=request.POST['city'],
                type=request.POST['type'],
                issus=request.POST['issus'],
                desc=request.POST['desc'],
            )
            return redirect('/')
        else:
            n = request.POST['phone']
            phoneNumber = format(int(n[:-1]), ",").replace(",", "-") + n[-1]
            Appt.objects.create(
                fname=request.POST['fname'],
                lname=request.POST['lname'],
                phone= phoneNumber,
                city=request.POST['city'],
                type=request.POST['type'],
                issus=request.POST['issus'],
                desc=request.POST['desc'],
                user=User.objects.get(id=request.session['userid'])
            )
            return redirect('/')  # change to login account

def sendEmail(request):
    name = request.GET["name"]
    message = request.GET["message"]
    from_email = request.GET["email"]

    recaptcha_response = request.POST.get('g-recaptcha-response')
    url = 'https://www.google.com/recaptcha/api/siteverify'
    values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
    data = urllib.parse.urlencode(values).encode()
    req =  urllib.request.Request(url, data=data)
    response = urllib.request.urlopen(req)
    result = json.loads(response.read().decode())

    if result['success'] == False:
        messages.error(request, "Sorry no Robots! Please click the Checkbox")
        return redirect('/contactUs')
    else:
        send_mail(
            request.GET["subject"],
            f'Hello my name is {name} and my Email is {from_email}, {message}',
            'scrv8@yahoo.com',
            ['scrv8@yahoo.com'], #person that gets the email
            fail_silently=False,
        )
        return redirect("/")




# admin ///////////////////////////////////////////////

def customerInfo(request, custId):
    if not request.user.has_perm('poll.change_poll'):
        return redirect('/')
    else:
        context = {
            "cust": Appt.objects.get(id=custId),
            "parts": Part.objects.filter(appt=custId)
        }
        return render(request, 'admin/apptInfo.html', context)


def cancelJob(request, custId):
    if not request.user.has_perm('poll.change_poll'):
        return redirect('/')
    else:
        appt = Appt.objects.get(id=custId)
        appt.delete()
        return redirect('/admin/scv/custlistmodel/my_admin_path/')


def addCalendar(request, custId, keyWord):
    if not request.user.has_perm('poll.change_poll'):
        return redirect('/')
    else:
        year = datetime.now().year #current year
        month = datetime.now().month  #current month
        num_days = calendar.monthrange(year, month)[1]

        test = Appt.objects.filter(monthNum=month)
        work = []
        workName = []

        for one in test:
            work.append(one.calNum)
            workName.append(f"-{one.issus} in {one.city}")
        
        context = {
            'endMonth': num_days, #days in the month
            'monthNum': month,  # month number
            'month': calendar.month_name[month],  #month name
            'weekDay': calendar.monthrange(year, month)[0] + 1,
            'day': datetime.now().day,  #days number
            'cust': Appt.objects.get(id=custId), #Appt ID
            'keyWord': keyWord,  #keyword of Bol
            'appt': Appt.objects.filter(monthNum=month), # appts assigned to the month already
            'work': work,  #Numbers for bullet points
            'workName': json.dumps(workName),  #bullet point for cal box
        }
        return render(request, 'admin/addCalendar.html', context)


def addCalendarNext(request, custId, keyword):
    if not request.user.has_perm('poll.change_poll'):
        return redirect('/')
    else:
        year = datetime.now().year #current year
        month = datetime.now().month + 1 #current month
        if month == 13:
            month = 1
            year = datetime.now().year + 1
        num_days = calendar.monthrange(year, month)[1]

        test = Appt.objects.filter(monthNum=month)
        work = []
        workName = []

        for one in test:
            work.append(one.calNum)
            workName.append(f"-{one.issus} in {one.city}")
        
        context = {
            'endMonth': num_days,
            'monthNum': month,
            'month': calendar.month_name[month],
            'weekDay': calendar.monthrange(year, month)[0] +1,
            'day': datetime.now().day,
            'cust': Appt.objects.get(id=custId),
            'keyWord': keyword,
            'appt': Appt.objects.filter(monthNum=month),
            'work': work,
            'workName': json.dumps(workName),
        }
        return render(request, 'admin/addCalendar.html', context)


def assignAppt(request, custId, dayNum, monthNum, keyWord):
    if not request.user.has_perm('poll.change_poll'):
        return redirect('/')
    else:
        cust_appt = Appt.objects.get(id=custId)

        day = int(dayNum)
        month = int(monthNum)
        year = datetime.now().year

        if keyWord == 'diagnostic':
            cust_appt.diagnosedBol = True
            cust_appt.finishBol = False
            cust_appt.partsBol = False
            cust_appt.monthNum = monthNum
            cust_appt.apptDate = datetime(year,month, day)
            cust_appt.calNum = dayNum
            cust_appt.called = True
            cust_appt.save()
        if keyWord == 'complete':
            # if cust_appt.partC == partsLen:
            cust_appt.diagnosedBol = False
            cust_appt.finishBol = True
            cust_appt.partsBol = False
            cust_appt.monthNum = monthNum
            cust_appt.apptDate = datetime(year,month, day)
            cust_appt.calNum = dayNum
            cust_appt.called = True
            cust_appt.save()
        return redirect('/admin/scv/custlistmodel/my_admin_path/')


def calendarPage(request):
    if not request.user.has_perm('poll.change_poll'):
        return redirect('/')
    else:
        #add none page when cal has not been created
        year = datetime.now().year #current year
        month = datetime.now().month #current month
        num_days = calendar.monthrange(year, month)[1]
        monthNum = datetime.now().month
        test = Appt.objects.filter(monthNum=monthNum)
        work = []
        workName = []

        for one in test:
            work.append(one.calNum)
            workName.append(f"-{one.issus} in {one.city}")
        
        context = {
            'endMonth': num_days,
            'month': calendar.month_name[monthNum],
            'weekDay': calendar.monthrange(year, month)[0] +1,
            'day': datetime.now().day,
            'appt': Appt.objects.filter(monthNum=monthNum),
            'work': work,
            'workName': json.dumps(workName),
        }
        return render(request, 'admin/calender.html', context)


def nextCalenderPage(request):
    if not request.user.has_perm('poll.change_poll'):
        return redirect('/')
    else:
        #add none page when cal has not been created
        year = datetime.now().year #current year
        month = datetime.now().month + 1 #current month
        if month == 13:
            month = 1
            year = datetime.now().year + 1
        num_days = calendar.monthrange(year, month)[1]
        test = Appt.objects.filter(monthNum=month)
        work = []
        workName = []

        for one in test:
            work.append(one.calNum)
            workName.append(f"-{one.issus} in {one.city}")
        
        context = {
            'endMonth': num_days,
            'month': calendar.month_name[month],
            'weekDay': calendar.monthrange(year, month)[0] +1,
            'day': datetime.now().day,
            'appt': Appt.objects.filter(monthNum=month),
            'work': work,
            'workName': json.dumps(workName),
        }
        return render(request, 'admin/nextCalender.html', context)


def dateInfo(request, day):
    if not request.user.has_perm('poll.change_poll'):
        return redirect('/')
    else:
        monthNum = datetime.now().month
        context = {
            'jobs': Appt.objects.filter(calNum= day),
            'month': calendar.month_name[monthNum],
            'day': day
        }
        return render(request, 'admin/dateInfo.html', context)


def note(request, custId):
    if not request.user.has_perm('poll.change_poll'):
        return redirect('/')
    else:
        cust = Appt.objects.get(id=custId)
        cust.note = request.POST['note']
        cust.save()
        return redirect(f'/admin/customer/{custId}')


def addPart(request, custId):
    if not request.user.has_perm('poll.change_poll'):
        return redirect('/')
    else:
        cust = Appt.objects.get(id=custId) 
        Part.objects.create(
            partName = request.POST['partName'],
            appt = cust
        )
        cust.partsBol = True
        cust.diagnosedBol = False
        cust.finishBol = False
        cust.apptDate = None
        cust.save()
        return redirect(f'/admin/customer/{custId}')

def partTrue(request, partId, custId):
    if not request.user.has_perm('poll.change_poll'):
        return redirect('/')
    else:
        part = Part.objects.get(id=partId)
        part.completed = True
        part.save()

        cust = Appt.objects.get(id=custId)
        if cust.partC == None:
            cust.partC = 1
            cust.save()
        else:
            num = cust.partC
            cust.partC = num + 1
            cust.save()
        return redirect(f'/admin/customer/{custId}')

def partFalse(request, partId, custId):
    if not request.user.has_perm('poll.change_poll'):
        return redirect('/')
    else:
        part = Part.objects.get(id=partId)
        part.completed = False
        part.save()

        cust = Appt.objects.get(id=custId)
        if cust.partC == None:
            cust.partC = 1
            cust.save()
        else:
            num = cust.partC
            cust.partC = num - 1
            cust.save()
        return redirect(f'/admin/customer/{custId}')

def todayList(request):
    if not request.user.has_perm('poll.change_poll'):
        return redirect('/')
    else:
        context = {
            'todayAppt': Appt.objects.filter(apptDate = datetime.now())
        }
        return render(request, 'admin/today-list.html', context)


