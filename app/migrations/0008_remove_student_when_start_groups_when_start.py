# Generated by Django 4.1.9 on 2023-07-18 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_student_when_start'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='when_start',
        ),
        migrations.AddField(
            model_name='groups',
            name='when_start',
            field=models.TimeField(null=True),
        ),
    ]
