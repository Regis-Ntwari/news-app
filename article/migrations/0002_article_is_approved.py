# Generated by Django 3.1.4 on 2021-03-02 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
    ]
