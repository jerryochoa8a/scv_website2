# Generated by Django 3.0.8 on 2020-12-14 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scv', '0017_part_appt'),
    ]

    operations = [
        migrations.AddField(
            model_name='appt',
            name='partC',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
