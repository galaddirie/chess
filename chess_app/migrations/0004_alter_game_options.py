# Generated by Django 4.0.1 on 2022-01-31 12:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chess_app', '0003_alter_game_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='game',
            options={'ordering': ('-completed',)},
        ),
    ]