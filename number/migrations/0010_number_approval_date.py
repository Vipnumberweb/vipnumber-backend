# Generated by Django 5.2 on 2025-04-27 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('number', '0009_number_is_rejected'),
    ]

    operations = [
        migrations.AddField(
            model_name='number',
            name='approval_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
