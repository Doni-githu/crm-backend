# Generated by Django 4.1.9 on 2023-07-20 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_payment_month'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='month',
            field=models.DateField(max_length=50, null=True),
        ),
    ]
