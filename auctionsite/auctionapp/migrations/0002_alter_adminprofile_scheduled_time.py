# Generated by Django 5.1.3 on 2024-11-05 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctionapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adminprofile',
            name='scheduled_time',
            field=models.DateTimeField(blank=True),
        ),
    ]
