# Generated by Django 4.0.4 on 2022-07-22 18:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smarticket_api', '0002_alter_event_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='coordinates',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smarticket_api.coordinates'),
        ),
    ]
