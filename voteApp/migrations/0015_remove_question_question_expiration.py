# Generated by Django 5.0.3 on 2024-07-11 18:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('voteApp', '0014_auto_20240711_2004'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='question_expiration',
        ),
    ]