from django.contrib import admin
from api_data import models
# Register your models here.

admin.site.register(models.Alerts)
admin.site.register(models.AlertRegions)
admin.site.register(models.HourlyInfo)
admin.site.register(models.DailyInfo)
admin.site.register(models.HourlyStats)
admin.site.register(models.DailyStats)