# Generated by Django 5.0.6 on 2024-07-25 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emu', '0018_guestcustomer_order_slug_alter_item_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(blank=True, max_length=255, null=True, verbose_name='Name')),
                ('email_address', models.EmailField(blank=True, max_length=254, null=True)),
                ('message', models.TextField(blank=True, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name='item',
            name='name',
            field=models.CharField(default='Item 12', max_length=255),
        ),
    ]