# Generated by Django 3.1.4 on 2021-01-26 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0013_delete_users'),
    ]

    operations = [
        migrations.CreateModel(
            name='BalanceSheet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bankbalance', models.IntegerField()),
                ('cashbalance', models.IntegerField()),
                ('totaldebt', models.IntegerField()),
                ('totalowed', models.IntegerField()),
                ('capitalinvested', models.IntegerField()),
                ('companyworth', models.IntegerField()),
                ('percentgrowth', models.IntegerField()),
            ],
        ),
    ]
