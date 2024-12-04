from django.db import models

class ESP32Data(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    mqtt_status = models.CharField(max_length=50)
    gas = models.CharField(max_length=10)
    direction = models.CharField(max_length=10)
    steer = models.CharField(max_length=10)
    distance = models.FloatField()

    def __str__(self):
        return f"Data at {self.timestamp}"

class Userakun(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username
