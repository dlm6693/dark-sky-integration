# Generated by Django 3.0.2 on 2020-01-16 20:45

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_data', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HourlyInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('icon', models.CharField(max_length=255)),
                ('precipType', models.CharField(max_length=100)),
                ('summary', models.CharField(max_length=255)),
                ('time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='HourlyStats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('apparentTemperature', models.FloatField()),
                ('cloudCover', models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)])),
                ('humidity', models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)])),
                ('ozone', models.FloatField()),
                ('precipAccumulation', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('precipIntensity', models.FloatField()),
                ('precipProbability', models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)])),
                ('pressure', models.FloatField()),
                ('temperature', models.FloatField()),
                ('time', models.DateTimeField()),
                ('uvIndex', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('visibility', models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('windBearing', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(360)])),
                ('windGust', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('windSpeed', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
            ],
        ),
        migrations.AlterField(
            model_name='alertregions',
            name='alert',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='regions', to='api_data.Alerts'),
        ),
        migrations.AlterUniqueTogether(
            name='alertregions',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='alerts',
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name='alertregions',
            constraint=models.UniqueConstraint(fields=('latitude', 'longitude', 'time', 'expires'), name='regions_unique_together'),
        ),
        migrations.AddConstraint(
            model_name='alerts',
            constraint=models.UniqueConstraint(fields=('latitude', 'longitude', 'time', 'expires'), name='alerts_unique_together'),
        ),
        migrations.AddField(
            model_name='hourlyinfo',
            name='stats',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='info', to='api_data.HourlyStats'),
        ),
        migrations.AddConstraint(
            model_name='hourlyinfo',
            constraint=models.UniqueConstraint(fields=('latitude', 'longitude', 'time'), name='hourly_info_unique_together'),
        ),
    ]