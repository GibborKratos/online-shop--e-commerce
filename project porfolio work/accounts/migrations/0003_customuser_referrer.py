# Generated by Django 4.2.5 on 2023-10-31 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_customuser_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='referrer',
            field=models.CharField(default='No referrer', max_length=100),
        ),
    ]
