# Generated by Django 5.0.6 on 2024-07-15 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emu', '0017_alter_item_name_alter_order_order_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='guestcustomer',
            name='order_slug',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='name',
            field=models.CharField(default='Item 71', max_length=255),
        ),
    ]