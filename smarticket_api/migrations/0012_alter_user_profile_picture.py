# Generated by Django 4.0.4 on 2022-08-01 20:42

from django.db import migrations, models
import smarticket_api.models


class Migration(migrations.Migration):

    dependencies = [
        ('smarticket_api', '0011_alter_user_profile_picture_alter_user_wallet_hash'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to=smarticket_api.models.upload_to),
        ),
    ]
