# Generated by Django 5.0.6 on 2024-07-14 15:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mpesa', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stkpushtransaction',
            name='balance',
        ),
    ]
