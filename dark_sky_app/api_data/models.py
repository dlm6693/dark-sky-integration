from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Base(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    geohash = models.CharField(max_length=12)
    time = models.DateTimeField()
    
    class Meta:
        abtract = True
    
class Alerts(Base):
    
    title = models.CharField(max_length=255)
    severity = models.CharField(max_length=100)
    expires = models.DateTimeField()
    description = models.TextField()
    uri = models.URLField()
    
    class Meta:
       constraints = [
            models.UniqueConstraint(fields=['geohash', 'time', 'expires'], name='alerts_unique_together')
        ]
    
    def __str__(self):
        return self.title
    
class AlertRegions(Base):
    
    region = models.CharField(max_length=255)
    expires = models.DateTimeField()
    alert = models.ForeignKey('Alerts', related_name = 'regions', on_delete=models.CASCADE)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['geohash', 'time', 'expires'], name='regions_unique_together')
        ]
    
    def __str__(self):
        return self.region

class InfoBase(Base):
    
    precipType = models.CharField(max_length=100)
    summary= models.CharField(max_length=255)
    icon = models.CharField(max_length=255)
    
    class Meta:
        abtract = True
        
    def __str__(self):
        return f"{self.geohash}, {self.time}"

class HourlyInfo(InfoBase):
    
    stats = models.ForeignKey('HourlyStats', related_name = 'info', on_delete=models.CASCADE)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['geohash', 'time'], name='hourly_info_unique_together')
            ]

class DailyInfo(InfoBase):
    
    stats = models.ForeignKey('DailyStats', related_name = 'info', on_delete=models.CASCADE)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['geohash', 'time'], name='daily_info_unique_together')
            ]
    

class StatsBase(Base):
    
    cloudCover = models.FloatField(
        validators=[MinValueValidator(0), 
                    MaxValueValidator(1)]
    )
    dewPoint = models.FloatField()
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
    pressure = models.FloatField()
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
    
    class Meta:
        abtract = True
        
    def __str__(self):
        return f"{self.geohash}, {self.time}"
        
class HourlyStats(StatsBase):
    
    apparentTemperature = models.FloatField()
    temperature = models.FloatField()
    info = models.ForeignKey('HourlyInfo', related_name = 'stats', on_delete=models.CASCADE)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['geohash', 'time'], name='hourly_stats_unique_together')
            ]
    
class DailyStats(StatsBase)    

    apparentTemperatureHigh = models.FloatField()
    apparentTemperatureHighTime = models.DateTimeField()
    apparentTemperatureLow = models.FloatField()
    apparentTemperatureLowTime = models.DateTimeField()
    apparentTemperatureMax = models.FloatField()
    apparentTemperatureMaxTime = models.DateTimeField()
    apparentTemperatureMin = models.FloatField()
    apparentTemperatureMinTime = models.DateTimeField()
    moonPhase = models.FloatField(
        validators = [MinValueValidator(0), MaxValueValidator(1)]
    )
    precipIntensityMax = models.FloatField()
    precipIntensityMaxTime = models.DateTimeField()
    sunriseTime = models.DateTimeField()
    sunsetTime = models.DateTimeField()
    temperatureHigh = models.FloatField()
    temperatureHighTime = models.FloatField()
    temperatureLow = models.FloatField()
    temperatureLowTime = models.DateTimeField()
    temperatureMax = models.FloatField()
    temperatureMaxTime = models.DateTimeField()
    temperatureMin = models.FloatField()
    temperatureMinTime = models.DateTimeField()
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['geohash', 'time'], name='daily_stats_unique_together')
            ]
    