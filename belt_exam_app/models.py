from django.db import models
import re
from datetime import date, datetime

class UserManager(models.Manager):
    def basic_validator(self, requestPOST):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[A-Za-z0-9]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(requestPOST['name']) < 3:
            errors['name'] = "Name is too short"
        users_with_name = User.objects.filter(name=requestPOST['name'])
        if len(users_with_name) > 0:
            errors['duplicate'] = "Name already taken"
        if len(requestPOST['password']) < 8:
            errors['password'] = "Password is too short"
        if requestPOST['password'] != requestPOST['password_conf']:
            errors['no_match'] = "Password and Password Confirmation must match"
        if not EMAIL_REGEX.match(requestPOST['email']):
            errors["email_regex"] = "Email must be valid email"
        return errors
    def edit_validator(self, requestPOST):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[A-Za-z0-9]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(requestPOST['name']) < 3:
            errors['name'] = "Name is too short"
        if not EMAIL_REGEX.match(requestPOST['email']):
            errors["email_regex"] = "Email must be valid email"
        return errors


class QuoteManager(models.Manager):
    def quote_validator(self, requestPOST):
        errors = {}
        if len(requestPOST['author']) < 4:
            errors['author_name'] = "Author Name is too short"
        if len(requestPOST['quote']) < 11:
            errors['quote_name'] = "Quote is too short"
        return errors

class User(models.Model):
    name = models.CharField(max_length=60)
    password = models.TextField()
    email = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Quote(models.Model):
    author = models.CharField(max_length=30)
    quote = models.CharField(max_length=255)
    users_who_like_quote = models.ManyToManyField(User, related_name="quotes_liked")
    user = models.ForeignKey(User, related_name="quotes", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()


# Create your models here.

# from django.db import models

# class UserManager(models.Manager):
#     def basic_validator(self, requestPOST):
#         errors = {}
#         if len(requestPOST['name']) < 3:
#             errors['name'] = "Name is too short"
#         users_with_name = User.objects.filter(name=requestPOST['name'])
#         if len(users_with_name) > 0:
#             errors['duplicate'] = "Name already taken"
#         if len(requestPOST['password']) < 8:
#             errors['password'] = "Password is too short"
#         if requestPOST['password'] != requestPOST['password_conf']:
#             errors['no_match'] = "Password and Password Confirmation must match"
#         return errors

# class User(models.Model):
#     name = models.TextField()
#     password = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     objects = UserManager()

# class CatManager(models.Manager):
#     def cat_validator(self, requestPOST):
#         errors = {}
#         if len(requestPOST['name']) <= 2:
#             errors['name'] = "Name is too short"
#         cats_with_name = Cat.objects.filter(name=requestPOST['name'])
#         if len(cats_with_name) > 0:
#             errors['duplicate'] = "Name already taken. Enter number next to cat name"
#         return errors

# class Cat(models.Model):
#     name = models.CharField(max_length=30)
#     users_who_voted_for = models.ManyToManyField(User, related_name="cats_voted_for")
#     user = models.ForeignKey(User, related_name="cats", on_delete = models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     objects = CatManager()

#I would like a Cat to have a name, owner/user (use related_name "cats"), users_who_voted_for (use related_name "cats_voted_for"), and created_at + updated_at
#A Cat can only have one User who owns it

# class User(models.Model):
#     name = models.TextField()
#     friendships = models.ManyToManyField("self")
        #still has same functions(add, remove) that a regular ManyToManyField has.
        #This is a self join.
