# Generated by Django 5.1.3 on 2024-11-09 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctionapp', '0006_remove_adminprofile_auction_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auctionhistory',
            old_name='price_after_auction',
            new_name='current_price',
        ),
        migrations.RenameField(
            model_name='lot',
            old_name='start_price',
            new_name='current_price',
        ),
        migrations.AddField(
            model_name='adminprofile',
            name='current_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]