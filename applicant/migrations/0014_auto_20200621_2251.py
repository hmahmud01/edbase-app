# Generated by Django 3.0 on 2020-06-21 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applicant', '0013_batch_session_studentsessionbatchtracker'),
    ]

    operations = [
        migrations.AddField(
            model_name='personalinfo',
            name='unique_id',
            field=models.CharField(blank=True, max_length=26, null=True),
        ),
        migrations.AddField(
            model_name='subject',
            name='code',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
