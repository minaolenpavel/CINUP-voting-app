# Generated by Django 5.0.3 on 2024-07-11 17:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voteApp', '0011_alter_question_question_expiration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question_expiration',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 11, 20, 2, 48, 171343, tzinfo=datetime.timezone.utc)),
        ),
    ]
