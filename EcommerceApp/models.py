from django.db import models
import re, bcrypt
from datetime import datetime, timedelta

# Create your models here.
class UserManager(models.Manager):
    def registerVal(self, postData):
        errors= {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['firstName']) < 1:
            errors['firstName'] = "Enter First Name"
        if len(postData['lastName']) < 1:
            errors['lastName'] = "Enter Last Name"
        if not EMAIL_REGEX.match(postData['email']): 
            errors['emailpattern'] = "Invalid Email Address" 
        user = User.objects.filter(email=postData['email'])
        if user:
            register_user = user[0]
            errors['existid'] ="Eamil Address is already exists"
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters"
        if postData['confirm'] != postData['password']:
            errors['confirm'] = "Password and confirm PW must match"
        return errors

    def loginVal(self, postData):
        errors= {}
        user = User.objects.filter(email=postData['email'])
        if user:
            logged_user = user[0]
            if bcrypt.checkpw(postData['password'].encode(), logged_user.password.encode()):
                pass
            else:
                errors['wrongpw'] ="Password does not match"
        else:
            errors['unregistered'] = "User not registered. Try agian"
        return errors

class User(models.Model):
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Item(models.Model):
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    price = models.IntegerField(blank=True, null=True)
    inStock = models.IntegerField(blank=True, null=True)
    isSold = models.IntegerField(blank=True, null=True)
    image = models.ImageField(upload_to="forums", default=None, blank=True, null=True)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Option(models.Model):
    choice = models.CharField(max_length=255)
    image = models.ImageField(upload_to="forums", default=None, blank=True, null=True)
    item = models.ForeignKey(Item, related_name="options", on_delete=models.CASCADE, default=None)
    extra = models.IntegerField(blank=True, null=True, default=None)
    
class List(models.Model):
    currentuser = models.ForeignKey(User, related_name="cart", on_delete=models.CASCADE)
    obj = models.ForeignKey(Item, related_name="iteminCart", on_delete=models.CASCADE)
    selected = models.ForeignKey(Option, related_name="chosen", on_delete=models.CASCADE, default=None)
    total = models.IntegerField(blank=True, null=True)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Transaction(models.Model):
    currentuser = models.ForeignKey(User, related_name="cart", on_delete=models.CASCADE)
    items = models.ForeignKey(List, related_name="purchased", on_delete=models.CASCADE)
    history = models.ForeignKey(History, related_name="made", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class History(models.Model):
    currentuser = models.ForeignKey(User, related_name="history", on_delete=models.CASCADE)
    order = models.ForeignKey(Transaction, related_name="purchased", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
