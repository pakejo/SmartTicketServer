# Generated by Django 4.0.4 on 2022-07-31 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smarticket_api', '0008_alter_event_imageurl'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='uid',
            field=models.CharField(default='', max_length=40),
        ),
    ]