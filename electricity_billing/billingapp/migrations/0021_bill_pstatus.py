# Generated by Django 4.1.1 on 2023-01-23 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billingapp', '0020_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='pstatus',
            field=models.BooleanField(default=False),
        ),
    ]
