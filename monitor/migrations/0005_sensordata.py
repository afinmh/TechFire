# Generated by Django 5.1.1 on 2024-12-27 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0004_delete_esp32data'),
    ]

    operations = [
        migrations.CreateModel(
            name='SensorData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pompa', models.CharField(max_length=10)),
                ('strobo', models.CharField(max_length=10)),
                ('speaker', models.CharField(max_length=10)),
                ('fire', models.CharField(max_length=10)),
                ('batre', models.PositiveIntegerField()),
                ('distance', models.FloatField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
