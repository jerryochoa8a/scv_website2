# Generated by Django 3.0.8 on 2020-12-04 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scv', '0008_appt_monthnum'),
    ]

    operations = [
        migrations.CreateModel(
            name='Calendar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('yearNum', models.IntegerField(blank=True, null=True)),
                ('monthNum', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
