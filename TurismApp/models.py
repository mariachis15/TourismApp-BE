from django.db import models

# Create your models here.

class User(models.Model):
    id = models.AutoField(primary_key=True)
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    email =  models.CharField(max_length=70)
    password = models.CharField(max_length=70)
    role = models.CharField(max_length=30)

class Destination(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)  
    location = models.CharField(max_length=100)
    price = models.FloatField()  
    numberOfGuests = models.IntegerField()

