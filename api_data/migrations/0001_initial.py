# Generated by Django 3.0.2 on 2020-02-11 22:01

import api_data.custom_fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AlertRegions',
            fields=[
                ('ID', models.UUIDField(db_column='id', default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('geohash', models.CharField(max_length=12, null=True)),
                ('time', models.DateTimeField()),
                ('region', models.CharField(max_length=255)),
                ('expires', models.DateTimeField()),
            ],
            options={
                'verbose_name_plural': 'AlertRegions',
            },
        ),
        migrations.CreateModel(
            name='Alerts',
            fields=[
                ('ID', models.UUIDField(db_column='id', default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('geohash', models.CharField(max_length=12, null=True)),
                ('time', models.DateTimeField()),
                ('title', models.CharField(max_length=255)),
                ('severity', models.CharField(max_length=100)),
                ('expires', models.DateTimeField()),
                ('description', models.TextField()),
                ('uri', models.URLField()),
            ],
            options={
                'verbose_name_plural': 'Alerts',
            },
        ),
        migrations.CreateModel(
            name='DailyInfo',
            fields=[
                ('ID', models.UUIDField(db_column='id', default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('geohash', models.CharField(max_length=12, null=True)),
                ('time', models.DateTimeField()),
                ('precipType', models.CharField(max_length=100)),
                ('summary', models.CharField(max_length=255)),
                ('icon', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'DailyInfo',
            },
        ),
        migrations.CreateModel(
            name='DailyStats',
            fields=[
                ('ID', models.UUIDField(db_column='id', default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('geohash', models.CharField(max_length=12, null=True)),
                ('time', models.DateTimeField()),
                ('cloudCover', models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)])),
                ('dewPoint', models.FloatField(default=0)),
                ('humidity', models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)])),
                ('ozone', models.FloatField()),
                ('precipAccumulation', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('precipIntensity', models.FloatField()),
                ('precipProbability', models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)])),
                ('pressure', models.FloatField()),
                ('uvIndex', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('visibility', models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('windBearing', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(360)])),
                ('windGust', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('windSpeed', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('apparentTemperatureHigh', models.FloatField()),
                ('apparentTemperatureHighTime', models.DateTimeField()),
                ('apparentTemperatureLow', models.FloatField()),
                ('apparentTemperatureLowTime', models.DateTimeField()),
                ('apparentTemperatureMax', models.FloatField()),
                ('apparentTemperatureMaxTime', models.DateTimeField()),
                ('apparentTemperatureMin', models.FloatField()),
                ('apparentTemperatureMinTime', models.DateTimeField()),
                ('moonPhase', models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)])),
                ('precipIntensityMax', models.FloatField()),
                ('precipIntensityMaxTime', models.DateTimeField()),
                ('sunriseTime', models.DateTimeField()),
                ('sunsetTime', models.DateTimeField()),
                ('temperatureHigh', models.FloatField()),
                ('temperatureHighTime', models.DateTimeField()),
                ('temperatureLow', models.FloatField()),
                ('temperatureLowTime', models.DateTimeField()),
                ('temperatureMax', models.FloatField()),
                ('temperatureMaxTime', models.DateTimeField()),
                ('temperatureMin', models.FloatField()),
                ('temperatureMinTime', models.DateTimeField()),
                ('windGustTime', models.DateTimeField()),
            ],
            options={
                'verbose_name_plural': 'DailyStats',
            },
        ),
        migrations.CreateModel(
            name='HourlyInfo',
            fields=[
                ('ID', models.UUIDField(db_column='id', default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('geohash', models.CharField(max_length=12, null=True)),
                ('time', models.DateTimeField()),
                ('precipType', models.CharField(max_length=100)),
                ('summary', models.CharField(max_length=255)),
                ('icon', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'HourlyInfo',
            },
        ),
        migrations.CreateModel(
            name='HourlyStats',
            fields=[
                ('ID', models.UUIDField(db_column='id', default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('geohash', models.CharField(max_length=12, null=True)),
                ('time', models.DateTimeField()),
                ('cloudCover', models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)])),
                ('dewPoint', models.FloatField(default=0)),
                ('humidity', models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)])),
                ('ozone', models.FloatField()),
                ('precipAccumulation', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('precipIntensity', models.FloatField()),
                ('precipProbability', models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)])),
                ('pressure', models.FloatField()),
                ('uvIndex', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('visibility', models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('windBearing', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(360)])),
                ('windGust', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('windSpeed', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('apparentTemperature', models.FloatField()),
                ('temperature', models.FloatField()),
            ],
            options={
                'verbose_name_plural': 'HourlyStats',
            },
        ),
        migrations.CreateModel(
            name='MappingData',
            fields=[
                ('ID', models.AutoField(db_column='id', editable=False, primary_key=True, serialize=False)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('city', models.CharField(max_length=100)),
                ('state_id', models.CharField(max_length=2)),
                ('state_name', models.CharField(max_length=100)),
                ('county_fips', models.IntegerField()),
                ('county_name', models.CharField(max_length=100)),
                ('county_fips_all', api_data.custom_fields.SeparatedValuesField()),
                ('county_name_all', api_data.custom_fields.SeparatedValuesField()),
                ('population', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('density', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('incorporated', models.BooleanField()),
                ('timezone', models.CharField(max_length=100)),
                ('ranking', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(3)])),
                ('zips', api_data.custom_fields.SeparatedValuesField()),
            ],
        ),
        migrations.AddConstraint(
            model_name='hourlystats',
            constraint=models.UniqueConstraint(fields=('geohash', 'time'), name='hourly_stats_unique_together'),
        ),
        migrations.AddConstraint(
            model_name='hourlyinfo',
            constraint=models.UniqueConstraint(fields=('geohash', 'time'), name='hourly_info_unique_together'),
        ),
        migrations.AddConstraint(
            model_name='dailystats',
            constraint=models.UniqueConstraint(fields=('geohash', 'time'), name='daily_stats_unique_together'),
        ),
        migrations.AddConstraint(
            model_name='dailyinfo',
            constraint=models.UniqueConstraint(fields=('geohash', 'time'), name='daily_info_unique_together'),
        ),
        migrations.AddConstraint(
            model_name='alerts',
            constraint=models.UniqueConstraint(fields=('geohash', 'time', 'expires'), name='alerts_unique_together'),
        ),
        migrations.AddField(
            model_name='alertregions',
            name='alertID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='regions', to='api_data.Alerts'),
        ),
        migrations.AddConstraint(
            model_name='alertregions',
            constraint=models.UniqueConstraint(fields=('geohash', 'region', 'time', 'expires'), name='regions_unique_together'),
        ),
    ]
