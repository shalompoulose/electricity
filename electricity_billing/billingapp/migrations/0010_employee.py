# Generated by Django 4.1.5 on 2023-01-18 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billingapp', '0009_bill'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.IntegerField(default='1', primary_key=True, serialize=False)),
                ('name', models.CharField(default='hello', max_length=255)),
                ('email', models.EmailField(default='s@gmail.com', max_length=254)),
                ('position', models.CharField(default='qwerty', max_length=255)),
            ],
        ),
    ]
