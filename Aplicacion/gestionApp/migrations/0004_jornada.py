# Generated by Django 3.0.5 on 2020-07-14 15:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestionApp', '0003_auto_20200711_1008'),
    ]

    operations = [
        migrations.CreateModel(
            name='Jornada',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_jornada', models.IntegerField()),
                ('puntos', models.IntegerField()),
                ('jugador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestionApp.Jugador')),
            ],
        ),
    ]
