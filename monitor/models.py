from django.db import models


class SensorData(models.Model):
    pompa = models.CharField(max_length=10)
    strobo = models.CharField(max_length=10)  
    speaker = models.CharField(max_length=10)  
    fire = models.CharField(max_length=10)  
    batre = models.PositiveIntegerField()  
    distance = models.FloatField()  
    timestamp = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"SensorData at {self.timestamp}"

class Userakun(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class FireImage(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    fire_image = models.ImageField(upload_to='fire_images/')

    def __str__(self):
        return f"Fire image at {self.timestamp}"