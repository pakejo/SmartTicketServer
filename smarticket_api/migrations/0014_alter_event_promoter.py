# Generated by Django 4.0.4 on 2022-08-06 08:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smarticket_api', '0013_alter_event_imageurl_alter_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='promoter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='promoter', to='smarticket_api.user'),
        ),
    ]