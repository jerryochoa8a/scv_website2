# Generated by Django 3.0.8 on 2020-12-04 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scv', '0007_appt_calnum'),
    ]

    operations = [
        migrations.AddField(
            model_name='appt',
            name='monthNum',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
