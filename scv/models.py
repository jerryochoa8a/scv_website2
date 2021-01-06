from calendar import month
from django.db import models
import re
from django.core.validators import RegexValidator
from django.db.models.base import Model
from datetime import datetime

# Create your models here.
class ShowManager(models.Manager):
    def login_validator(self, post_data):
        errors ={}
        
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']):    # test whether a field matches the pattern            
            errors['email'] = "Invalid email address!"
        
        if len(post_data['fname']) < 2:
            errors['fname'] = "First Name must be at least 2 characters"

        if len(post_data['lname']) < 2:
            errors['lname'] = "Last Name must be at least 2 characters"

        if len(post_data['pass']) < 5:
            errors['pass'] = "Password has to be a minimum of 5 characters"

        return errors



    def appt_validator(self, post_data):
        errors ={}

        if len(post_data['city']) < 1:
            errors['city'] = "Invalid City!"


        if len(post_data['desc']) < 4:
            errors['desc'] = "Description must be 4 Charactors or more!"
        
        EMAIL_REGEX = re.compile(r'^\+?1?\d{9,15}$')
        if not EMAIL_REGEX.match(post_data['phone']):    # test whether a field matches the pattern            
            errors['phone'] = "Invalid Phone Number!"

        return errors

    # def payment_validator(self, post_data):
    #     errors ={}
        
    #     if len(post_data['ccName']) < 1:
    #         errors['ccName'] = "Card Name is Required"

    #     if len(post_data['ccNum']) < 16:
    #         errors['ccNum'] = "Invalid Card Number" 

    #     if len(post_data['ccCode']) < 3:
    #         errors['ccCode'] = "Invalid Security Code"

    #     if len(post_data['expdate']) < 1:
    #         errors['expdate'] = "Card Date is Required"

    #     if len(post_data['fname']) < 1:
    #         errors['fname'] = "First Name is Required"

    #     if len(post_data['lname']) < 1:
    #         errors['lname'] = "Last Name is Required" 

    #     if len(post_data['addy']) < 1:
    #         errors['addy'] = "Address is Required"

    #     if len(post_data['city']) < 1:
    #         errors['city'] = "City is Required"

    #     if len(post_data['state']) < 1:
    #         errors['state'] = "State is Required"

    #     if len(post_data['zip_code']) < 5:
    #         errors['zip_code'] = "Invalid Zip!"

    #     return errors

class User(models.Model): #customers
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)
    city = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.EmailField(max_length=40)
    password = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class Appt(models.Model):
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    issus = models.CharField(max_length=255)
    desc = models.CharField(max_length=455)

    called = models.BooleanField(default=False)
    diagnosedBol = models.BooleanField(default=False)
    partsBol = models.BooleanField(default=False)
    partC = models.IntegerField(null=True, blank=True, default=0)
    finishBol = models.BooleanField(default=False)

    apptDate = models.DateField(null=True, blank=True, default=None)
    note =  models.CharField(max_length=455, null=True, blank=True)
    calNum = models.IntegerField(null=True, blank=True)
    monthNum = models.IntegerField(null=True, blank=True)

    user = models.ForeignKey(User, null=True, blank=True, related_name="appt", on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Part(models.Model):
    partName = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)
    appt = models.ForeignKey(Appt, related_name="parts",null=True, blank=True , on_delete = models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ShowManager()