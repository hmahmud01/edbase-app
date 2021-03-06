# Generated by Django 3.0 on 2020-05-30 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applicant', '0003_auto_20200526_0923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='email',
            field=models.EmailField(blank=True, max_length=128, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='guardian_mobile',
            field=models.CharField(blank=True, max_length=11, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='mobile',
            field=models.CharField(blank=True, max_length=11, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='name',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='qualification',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='school',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='status',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='user_type',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
