# Generated by Django 2.2.5 on 2019-12-18 21:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20191218_1743'),
    ]

    operations = [
        migrations.CreateModel(
            name='MedalType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Medal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mtype', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app.MedalType')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Player')),
                ('tournament', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app.Tournament')),
            ],
            options={
                'unique_together': {('tournament', 'player', 'mtype')},
            },
        ),
    ]
