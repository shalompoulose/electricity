# Generated by Django 4.1.5 on 2023-01-29 07:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('billingapp', '0027_complaint'),
    ]

    operations = [
        migrations.DeleteModel(
            name='alog',
        ),
        migrations.RemoveField(
            model_name='bill',
            name='connmodel',
        ),
        migrations.RemoveField(
            model_name='complaint',
            name='conmodel',
        ),
        migrations.RemoveField(
            model_name='conmodel',
            name='profile',
        ),
        migrations.DeleteModel(
            name='feedb',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='bill',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='user',
        ),
        migrations.DeleteModel(
            name='Bill',
        ),
        migrations.DeleteModel(
            name='complaint',
        ),
        migrations.DeleteModel(
            name='conmodel',
        ),
        migrations.DeleteModel(
            name='Payment',
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]