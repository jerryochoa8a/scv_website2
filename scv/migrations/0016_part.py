# Generated by Django 3.0.8 on 2020-12-12 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scv', '0015_auto_20201211_1700'),
    ]

    operations = [
        migrations.CreateModel(
            name='Part',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('partName', models.CharField(max_length=255)),
                ('completed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
