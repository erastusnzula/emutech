# Generated by Django 5.0.7 on 2024-08-08 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emu', '0023_remove_item_default_image_alter_item_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='name',
            field=models.CharField(default='Item 88', max_length=255),
        ),
    ]