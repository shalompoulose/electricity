# Generated by Django 4.1.1 on 2023-01-23 19:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('billingapp', '0018_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='alog',
        ),
        migrations.RemoveField(
            model_name='bill',
            name='profile',
        ),
        migrations.RemoveField(
            model_name='conmodel',
            name='profile',
        ),
        migrations.DeleteModel(
            name='feedb',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='user',
        ),
        migrations.DeleteModel(
            name='Bill',
        ),
        migrations.DeleteModel(
            name='conmodel',
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
