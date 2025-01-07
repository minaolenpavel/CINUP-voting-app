# Generated by Django 5.0.3 on 2024-06-30 15:27

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voteApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='access_key',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
