# Generated by Django 3.2.20 on 2024-09-04 00:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EnergyNew',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('square_footage', models.FloatField(default=0)),
                ('gas_usage', models.FloatField(default=0)),
                ('electricity_usage', models.FloatField(default=0)),
                ('miles_driven', models.FloatField(default=0)),
                ('net_co2', models.FloatField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Energy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('square_footage', models.FloatField(default=0)),
                ('gas_usage', models.FloatField(default=0)),
                ('electricity_usage', models.FloatField(default=0)),
                ('miles_driven', models.FloatField(default=0)),
                ('net_co2', models.FloatField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
