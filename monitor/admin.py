from django.contrib import admin
from .models import SensorData, Userakun, FireImage

admin.site.register(SensorData)
admin.site.register(FireImage)
admin.site.register(Userakun)
