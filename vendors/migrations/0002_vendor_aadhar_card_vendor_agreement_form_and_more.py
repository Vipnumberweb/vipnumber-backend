# Generated by Django 5.1.7 on 2025-04-02 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='aadhar_card',
            field=models.FileField(default=None, upload_to=None),
        ),
        migrations.AddField(
            model_name='vendor',
            name='agreement_form',
            field=models.FileField(default=None, upload_to=None),
        ),
        migrations.AddField(
            model_name='vendor',
            name='pan_card',
            field=models.FileField(default=None, upload_to=None),
        ),
    ]
