# Generated by Django 4.2.7 on 2023-11-06 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='pincode',
            field=models.CharField(blank=True, max_length=15),
        ),
    ]
