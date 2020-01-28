from django.db import models
from django.contrib import messages
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+$')


class UserManager(models.Manager):
    def validator(self, data):
        errors = {}
        if len(data['fname']) < 2:
            errors['fname'] = "Name is too short"
        if len(data['lname']) < 2:
            errors['lname'] = "Name is too short"
        if not EMAIL_REGEX.match(data['email']):
            errors['email'] = "Email is invalid"
        if len(data['password']) < 8:
            errors['password'] = "Password needs to be 8 characters or longer"
        if data['password'] != data['cpassword']:
            errors['password'] = "Passwords do not match"
        return errors


class UpdateManager(models.Manager):
    def validator(self, data):
        errors = {}
        if len(data['fname']) < 2:
            errors['fname'] = "Name is too short"
        if len(data['lname']) < 2:
            errors['lname'] = "Name is too short"
        if not EMAIL_REGEX.match(data['email']):
            errors['email'] = "Email is invalid"
        return errors


class QuoteManager(models.Manager):
    def validator(self, data):
        errors = {}
        if len(data['author']) < 3:
            errors['author'] = "Need to be more than 3 characters"
        if len(data['quote']) < 10:
            errors['quote'] = "Need to be more than 10 characters"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.CharField(max_length=60)
    password = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like = models.ManyToManyField('Quote', related_name="liked_quote")
    objects = UserManager()
    objects2 = UpdateManager()


class Quote(models.Model):
    author = models.CharField(max_length=60)
    quote = models.TextField()
    user_related = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name="quoted")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()
