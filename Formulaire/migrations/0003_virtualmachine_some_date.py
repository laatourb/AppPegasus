# Generated by Django 4.2.3 on 2023-07-23 12:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Formulaire', '0002_virtualmachine_active_virtualmachine_genre_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='virtualmachine',
            name='some_date',
            field=models.DateField(default=datetime.date(2023, 1, 1)),
        ),
    ]