# Generated by Django 4.1.5 on 2023-01-30 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billingapp', '0029_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alog',
            name='password',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='alog',
            name='username',
            field=models.CharField(max_length=50),
        ),
    ]
