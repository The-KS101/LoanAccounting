# Generated by Django 3.1.4 on 2020-12-24 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0004_clearedclients_cleareddate'),
    ]

    operations = [
        migrations.AddField(
            model_name='clearedclients',
            name='clearedRed',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]