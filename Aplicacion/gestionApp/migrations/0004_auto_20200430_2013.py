# Generated by Django 3.0.5 on 2020-04-30 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionApp', '0003_auto_20200430_1933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mercado',
            name='liga_mercado',
            field=models.CharField(max_length=40),
        ),
    ]
