# Generated by Django 5.1.3 on 2024-11-09 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctionapp', '0003_adminprofile_rules_adminprofile_step_bid_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='lot',
            name='user_name_bid',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]