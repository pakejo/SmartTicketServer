# Generated by Django 4.0.4 on 2022-08-20 13:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smarticket_api', '0026_alter_category_options_alter_coordinates_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='event',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='smarticket_api.event'),
        ),
    ]
