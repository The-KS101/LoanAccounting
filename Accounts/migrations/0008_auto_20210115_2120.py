# Generated by Django 3.1.4 on 2021-01-15 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0007_auto_20210112_2238'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clearedclients',
            name='clearedRed',
        ),
        migrations.AddField(
            model_name='client',
            name='redPay',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='amountadded',
            name='date_paid',
            field=models.DateField(auto_now_add=True),
        ),
    ]
