# Generated by Django 2.0 on 2018-01-03 02:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('swiss', '0008_auto_20171229_0107'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='family',
            field=models.ManyToManyField(blank=True, related_name='_player_family_+', to='swiss.Player'),
        ),
    ]
