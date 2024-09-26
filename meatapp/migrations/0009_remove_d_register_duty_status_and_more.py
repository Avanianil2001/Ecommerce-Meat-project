# Generated by Django 5.0.6 on 2024-08-14 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meatapp', '0008_d_register_duty_status_d_register_is_available_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='d_register',
            name='duty_status',
        ),
        migrations.RemoveField(
            model_name='d_register',
            name='is_available',
        ),
        migrations.AddField(
            model_name='d_register',
            name='d_status',
            field=models.CharField(choices=[('available', 'Available'), ('in-duty', 'In Duty'), ('off-duty', 'Off Duty')], default='off-duty', max_length=20),
        ),
    ]
