from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, int_list_validator
import uuid

# Create your models here.
class Base(models.Model):
    ID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_column='id')
    latitude = models.FloatField()
    longitude = models.FloatField()
    geohash = models.CharField(max_length=12, null=True)
    time = models.DateTimeField()
    
    class Meta:
        abstract = True
    
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
       verbose_name_plural = 'Alerts'
    
    def __str__(self):
        return self.title
    
class AlertRegions(Base):
    alertID = models.ForeignKey('Alerts', related_name='regions', on_delete=models.CASCADE)
    region = models.CharField(max_length=255)
    expires = models.DateTimeField()
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['geohash', 'region', 'time', 'expires'], name='regions_unique_together')
        ]
        verbose_name_plural = 'AlertRegions'
    
    def __str__(self):
        return self.region
    
    @property
    def alert(self):
        return Alerts.objects.get(forecastID = self.forecastID)

class InfoBase(Base):
    
    precipType = models.CharField(max_length=100)
    summary= models.CharField(max_length=255)
    icon = models.CharField(max_length=255)
    
    class Meta:
        abstract = True
        
    def __str__(self):
        return f"{self.geohash}, {self.time}"

class HourlyInfo(InfoBase):
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['geohash', 'time'], name='hourly_info_unique_together')
            ]
        verbose_name_plural = 'HourlyInfo'
    
    @property
    def stats(self):
        return HourlyStats.objects.get(forecastID = self.forecastID)

class DailyInfo(InfoBase):
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['geohash', 'time'], name='daily_info_unique_together')
            ]
        verbose_name_plural = 'DailyInfo'
    
    @property
    def stats(self):
        return DailyStats.objects.get(forecastID = self.forecastID)
    

class StatsBase(Base):
    
    cloudCover = models.FloatField(
        validators=[MinValueValidator(0), 
                    MaxValueValidator(1)]
    )
    dewPoint = models.FloatField(default=0)
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
        abstract = True
        
    def __str__(self):
        return f"{self.geohash}, {self.time}"
        
class HourlyStats(StatsBase):
    
    apparentTemperature = models.FloatField()
    temperature = models.FloatField()
    # info = models.ForeignKey('HourlyInfo', related_name = 'stats', on_delete=models.CASCADE)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['geohash', 'time'], name='hourly_stats_unique_together')
            ]
        verbose_name_plural = 'HourlyStats'
        
    @property
    def info(self):
        return HourlyInfo.objects.get(forecastID=self.forecastID)
    
class DailyStats(StatsBase):    

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
    temperatureHighTime = models.DateTimeField()
    temperatureLow = models.FloatField()
    temperatureLowTime = models.DateTimeField()
    temperatureMax = models.FloatField()
    temperatureMaxTime = models.DateTimeField()
    temperatureMin = models.FloatField()
    temperatureMinTime = models.DateTimeField()
    windGustTime = models.DateTimeField()
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['geohash', 'time'], name='daily_stats_unique_together')
            ]
        verbose_name_plural = 'DailyStats'
    
    @property
    def info(self):
        return DailyInfo.objects.get(forecastID=self.forecastID)

class MappingData(models.Model):
    ID = models.AutoField(primary_key=True, editable=False, db_column='id')
    latitude = models.FloatField()
    longitude = models.FloatField()
    city = models.CharField()
    state_id = models.CharField(max_length=2)
    state_name = models.CharField(max_length=100)
    county_flips = models.IntegerField()
    county_name = models.CharField(max_length=100)
    county_flips_all = models.CharField()
    county_name_all = models.CharField()
    population = models.IntegerField(
        validators = [MinValueValidator(0)]
    )
    density = models.IntegerField(
        validators = [MinValueValidator(0)]
    )
    incorporated = models.BooleanField()
    timezone = models.CharField(max_length=100)
    ranking = models.PositiveSmallIntegerField(
        validators = [MinValueValidator(1), MaxValueValidator(3)]
    )
    zips = models.CharField(
        validators = [int_list_validator]
    )
    
    
    
    