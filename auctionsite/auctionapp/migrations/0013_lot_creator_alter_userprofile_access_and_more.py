# Generated by Django 5.1.3 on 2024-11-10 22:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctionapp', '0012_remove_lot_document_type_choice'),
    ]

    operations = [
        migrations.AddField(
            model_name='lot',
            name='creator',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='auctionapp.userprofile'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='access',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.CharField(max_length=50),
        ),
    ]
