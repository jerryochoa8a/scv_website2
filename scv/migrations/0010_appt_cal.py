# Generated by Django 3.0.8 on 2020-12-04 22:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scv', '0009_calendar'),
    ]

    operations = [
        migrations.AddField(
            model_name='appt',
            name='cal',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='appt', to='scv.Calendar'),
        ),
    ]
