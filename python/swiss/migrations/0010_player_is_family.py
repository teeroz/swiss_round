# Generated by Django 2.0 on 2018-01-03 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('swiss', '0009_player_family'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='is_family',
            field=models.BooleanField(default=False),
        ),
    ]
