# Generated by Django 4.1.5 on 2023-01-14 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billingapp', '0008_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='bill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cnumber', models.CharField(max_length=50)),
                ('bmonth', models.CharField(max_length=50)),
                ('cread', models.IntegerField()),
                ('pread', models.IntegerField()),
                ('tunit', models.IntegerField()),
                ('cpu', models.IntegerField()),
                ('amount', models.IntegerField()),
                ('ddate', models.CharField(max_length=50)),
            ],
        ),
    ]
