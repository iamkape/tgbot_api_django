# Generated by Django 5.1.3 on 2024-11-09 13:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctionapp', '0005_adminprofile_auction_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='adminprofile',
            name='auction_price',
        ),
    ]
