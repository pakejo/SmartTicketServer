# Generated by Django 4.0.4 on 2022-07-23 19:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smarticket_api', '0005_delete_sale'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customerId', models.CharField(max_length=32)),
                ('price', models.DecimalField(decimal_places=5, max_digits=7)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event', to='smarticket_api.event')),
            ],
        ),
    ]
