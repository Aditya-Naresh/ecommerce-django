# Generated by Django 4.2.4 on 2023-11-13 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoryoffer',
            name='offer_type',
            field=models.CharField(choices=[('PERCENT', 'Percentage Discount'), ('FIXED', 'Fixed Amount Discount')], max_length=10),
        ),
        migrations.AlterField(
            model_name='productoffer',
            name='offer_type',
            field=models.CharField(choices=[('PERCENT', 'Percentage Discount'), ('FIXED', 'Fixed Amount Discount')], max_length=10),
        ),
    ]