# Generated by Django 4.1.5 on 2023-01-11 08:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('billingapp', '0007_delete_alog_delete_conmodel_delete_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='alog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='admin', max_length=50)),
                ('password', models.CharField(default='admin', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='conmodel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cnumber', models.CharField(max_length=50)),
                ('ctype', models.CharField(max_length=50)),
                ('cdate', models.CharField(max_length=50)),
                ('occ', models.CharField(max_length=50)),
                ('load', models.CharField(max_length=50)),
                ('hnumber', models.CharField(max_length=50)),
                ('des', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='feedb',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cnumber', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('feed', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auth_token', models.CharField(max_length=100)),
                ('is_verified', models.BooleanField(default=False)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('cnumber', models.CharField(max_length=50)),
                ('mnumber', models.CharField(max_length=50)),
                ('gender', models.CharField(max_length=50)),
                ('add', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('pin', models.CharField(max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]