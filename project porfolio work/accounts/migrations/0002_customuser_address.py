# Generated by Django 4.2.5 on 2023-10-31 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='address',
            field=models.CharField(default='na', max_length=500),
            preserve_default=False,
        ),
    ]
