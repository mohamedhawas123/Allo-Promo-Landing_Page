from django.db import models
from django.contrib.auth.models import AbstractUser


class Post(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    image = models.ImageField(upload_to='images', blank=True, null=True)
    dateTime= models.DateTimeField()
    user = models.CharField(max_length=100, blank=True, null=True)
    catelog = models.CharField(max_length=100,blank=True, null=True)


    def __str__(self):
        return self.title
    

class Service(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return self.name

class Testimonial(models.Model):
    client_name = models.CharField(max_length=200)
    statement = models.TextField()
    client_profile = models.ImageField(upload_to='images', blank=True, null=True)
    role = models.CharField(max_length=150, blank=True, null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='testimonials', blank=True, null=True)

    def __str__(self):
        return f"Testimonial by {self.client_name}"

class Form(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name
    


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    body = models.TextField()

    def __str__(self):
        return self.name