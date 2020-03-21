# Generated by Django 3.0.1 on 2020-03-21 11:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestionApp', '0005_auto_20200321_1222'),
    ]

    operations = [
        migrations.RenameField(
            model_name='liga',
            old_name='usuarios',
            new_name='usuario',
        ),
        migrations.CreateModel(
            name='plantilla',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seleccion', models.CharField(choices=[('SELECCIONADO', 'Seleccionado'), ('NO_SELECCIONADO', 'No seleccionado')], max_length=30)),
                ('jugador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestionApp.jugador')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestionApp.usuario')),
            ],
        ),
    ]
