from django.db import models

# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=200)
    email = models.EmailField()
    password = models.TextField()
    data = models.TextField(default="")
    
class Expert(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    domain = models.CharField(max_length=200)
    photo = models.ImageField(upload_to="expert")
    password = models.TextField()
    
class Docs(models.Model):
    id = models.AutoField(primary_key=True)
    domain = models.TextField()
    path = models.TextField()
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    datetime = models.DateTimeField(auto_now=True)
    
class Query(models.Model):
    id = models.AutoField(primary_key=True)
    domain = models.CharField(max_length=200)
    details = models.TextField()
    data = models.TextField(default="")
    datetime = models.DateTimeField(auto_now=True)




