# Generated by Django 5.0.3 on 2024-04-10 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Weather',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weather_date', models.DateTimeField(verbose_name='date')),
                ('temp', models.FloatField(verbose_name='temp')),
            ],
        ),
    ]