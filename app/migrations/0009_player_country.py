# Generated by Django 2.2.5 on 2019-12-27 19:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_player_disabled'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='country',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app.Country'),
        ),
    ]