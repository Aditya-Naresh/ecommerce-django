# Generated by Django 4.2.7 on 2023-11-07 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_userprofile_pincode'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='is_blocked',
            field=models.BooleanField(default=False),
        ),
    ]