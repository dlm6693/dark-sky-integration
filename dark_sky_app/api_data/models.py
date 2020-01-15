from django.db import models

# Create your models here.
class Alerts(models.Model):
    
    latitude = models.FloatField()
    longitude = models.FloatField()
    title = models.CharField(max_length=255)
    severity = models.CharField(max_length=100)
    time = models.DateTimeField()
    expires = models.DateTimeField()
    description = models.TextField()
    uri = models.URLField()
    
    class Meta:
        unique_together = ('latitude', 'longitude', 'time', 'expires')
    
    def __str__(self):
        return self.title
    
class AlertRegions(models.Model):
    
    region = models.CharField(max_length=255)
    time = models.DateTimeField()
    expires = models.DateTimeField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    alert = models.ForeignKey(Alerts, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('latitude', 'longitude', 'time', 'expires')