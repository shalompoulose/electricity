# Generated by Django 4.1.5 on 2023-02-12 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billingapp', '0040_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='byear',
            field=models.CharField(default=2022, max_length=30),
            preserve_default=False,
        ),
    ]
