# Generated by Django 3.0.8 on 2020-12-14 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scv', '0019_auto_20201213_1849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appt',
            name='partC',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
