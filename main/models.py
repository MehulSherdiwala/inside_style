from django.contrib.auth.models import User
from djongo import models
from django import forms


# Create your models here.
class State(models.Model):
    state_name = models.CharField(max_length=50)

    def __str__(self):
        return self.state_name


class City(models.Model):
    city_name = models.CharField(max_length=50)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return self.city_name


class Designer(models.Model):
    designer_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=12)
    password = forms.CharField(widget=forms.PasswordInput)
    description = models.TextField()
    join_date = models.DateField()
    status = models.BooleanField(default=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.designer_name

