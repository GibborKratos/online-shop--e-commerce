# Generated by Django 4.2.5 on 2023-10-31 03:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_message_recipient'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ('timestamp',)},
        ),
        migrations.DeleteModel(
            name='Room',
        ),
    ]
