# Generated by Django 2.2.7 on 2020-04-12 01:47

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('eduline', '0005_message_time'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='checkout',
            options={'ordering': ['student']},
        ),
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['time']},
        ),
        migrations.RenameField(
            model_name='checkout',
            old_name='returned_date',
            new_name='closed_date',
        ),
    ]
