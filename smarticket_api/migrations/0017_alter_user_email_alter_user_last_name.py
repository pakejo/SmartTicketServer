# Generated by Django 4.0.4 on 2022-08-10 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smarticket_api', '0016_alter_location_address1_alter_location_address2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
