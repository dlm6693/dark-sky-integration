from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Base(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    geohash = models.CharField(max_length=12, primary_key=True)
    
    class Meta:
        abtract = True

class AlertsHourlyBase(Base):
    time = models.DateTimeField()
    
    class Meta:
        abtract = True

class StatsBase(Base):
    


class Alerts(AlertsHourlyBase):
    
    title = models.CharField(max_length=255)
    severity = models.CharField(max_length=100)
    expires = models.DateTimeField()
    description = models.TextField()
    uri = models.URLField()
    
    class Meta:
       constraints = [
            models.UniqueConstraint(fields=['latitude', 'longitude', 'time', 'expires'], name='alerts_unique_together')
        ]
    
    def __str__(self):
        return self.title
    
class AlertRegions(AlertsHourlyBase):
    
    region = models.CharField(max_length=255)
    expires = models.DateTimeField()
    alert = models.ForeignKey('Alerts', related_name = 'regions', on_delete=models.CASCADE)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['latitude', 'longitude', 'time', 'expires'], name='regions_unique_together')
        ]
    
    def __str__(self):
        return self.region

class InfoBase(Base):
    
    precipType = models.CharField(max_length=100)
    summary= models.CharField(max_length=255)
    icon = models.CharField(max_length=255)
    
    class Meta:
        abtract = True

class HourlyInfo(AlertsHourlyBase, InfoBase):
    
    stats = models.ForeignKey('HourlyStats', related_name = 'info', on_delete=models.CASCADE)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['latitude', 'longitude', 'time'], name='hourly_info_unique_together')
            ]
    
    def __str__(self):
        return f"{self.latitude}, {self.longitude}, {self.time}"
    

class BaseStats(models.Model):
    

class HourlyStats(models.Model):
    
    apparentTemperature = models.FloatField()
    cloudCover = models.FloatField(
        validators=[MinValueValidator(0), 
                    MaxValueValidator(1)]
    )
    humidity = models.FloatField(
        validators=[MinValueValidator(0), 
                    MaxValueValidator(1)])
    ozone = models.FloatField()
    precipAccumulation = models.FloatField(
        validators=[MinValueValidator(0)]
    )
    precipIntensity = models.FloatField()
    precipProbability = models.FloatField(
        validators=[MinValueValidator(0), 
                    MaxValueValidator(1)]
    )
    precipAccumulation = models.FloatField(
        validators = [MinValueValidator(0)]
    )
    precipIntensity = models.FloatField()
    precipProbability = models.FloatField(
        validators=[MinValueValidator(0), 
                    MaxValueValidator(1)])
    pressure = models.FloatField()
    temperature = models.FloatField()
    time = models.DateTimeField()
    uvIndex = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), 
                    MaxValueValidator(10)]
    )
    visibility = models.FloatField(
        validators=[MinValueValidator(0), 
                    MaxValueValidator(10)]
    )
    windBearing = models.PositiveIntegerField(
        validators = [MaxValueValidator(360)]
    )
    windGust = models.FloatField(
        validators = [MinValueValidator(0)]
    )
    windSpeed = models.FloatField(
        validators = [MinValueValidator(0)]
    )