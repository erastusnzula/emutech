# Generated by Django 5.0.6 on 2024-07-06 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emu', '0007_remove_guestcustomer_user_alter_item_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='guestcustomer',
            name='password1',
            field=models.CharField(blank=True, default='PASSword@1', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='guestcustomer',
            name='password2',
            field=models.CharField(blank=True, default='PASSword@1', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='name',
            field=models.CharField(default='Item 9', max_length=255),
        ),
    ]
