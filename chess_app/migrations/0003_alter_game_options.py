# Generated by Django 4.0.1 on 2022-01-31 12:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chess_app', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='game',
            options={'ordering': ('completed',)},
        ),
    ]
