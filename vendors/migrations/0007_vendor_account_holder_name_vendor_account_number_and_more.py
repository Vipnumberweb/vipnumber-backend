# Generated by Django 5.1.7 on 2025-05-21 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "vendors",
            "0006_alter_vendor_aadhar_card_alter_vendor_agreement_form_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="vendor",
            name="account_holder_name",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="vendor",
            name="account_number",
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name="vendor",
            name="account_type",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name="vendor",
            name="bank_name",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="vendor",
            name="google_pay_number",
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name="vendor",
            name="ifsc_code",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name="vendor",
            name="paytm_number",
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name="vendor",
            name="phone_pay_number",
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name="vendor",
            name="upi_id",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
