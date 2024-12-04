# Generated by Django 5.1.1 on 2024-12-04 03:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
    ]
