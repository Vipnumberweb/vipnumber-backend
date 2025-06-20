from django.db import models
import uuid
from vendors.models import Vendor

class NumberType(models.TextChoices):
    REGULAR = "REG", "Regular"
    PREMIUM_TRENDING = "PRE_TRE", "Premium & Trending"
    PREMIUM = "PREM", "Premium"
    TRENDING = "TREND", "Trending"


class Status(models.TextChoices):
    AVAILABLE = "Available", "available"
    HOLD = "Hold", "hold"
    SOLD = "Sold", "sold"
    SOLD_BY_VENDOR = "Sold by vendor", "sold by vendor"
    VENDOR_DEACTIVATED = "Vendor deactivated", "vendor deactivated"
    PENDING_APPROVAL = "Pending approval", 'pending approval'

class NumberStatus(models.TextChoices):
    RTP = "RTP", "RTP"
    NONRTP = "NONRTP", "Non-RTP"
    CODE_RTP = "CODE_RTP", "Code RTP"
    PRE_TO_POST = "PRE_TO_POST", "Prepaid to Postpaid"
    POST_TO_PRE = "POST_TO_PRE", "Postpaid to Prepaid"

class ParentOperator(models.TextChoices):
    JIO = "JIO", "jio"
    AIRTEL = "AIRTEL", "airtel"
    VI = "VI", "vi"
    BSNL = "BSNL", "bsnl"

class Pattern(models.Model):
    pattern = models.CharField(max_length=128, unique=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

    def  __str__(self):
        return self.pattern


class Number(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    pattern = models.ForeignKey(Pattern, on_delete=models.CASCADE, null=True, related_name="numbers")

    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="numbers", null=False, default=None)  # vendor id
    entry = models.CharField(max_length=10, unique=True)

    parent_operator = models.CharField(max_length=20, choices=ParentOperator.choices, null=True)
    current_operator = models.CharField(max_length=50, null=True)
    circle = models.CharField(max_length=50, null=True)

    numberStatus = models.CharField(max_length=20, choices=NumberStatus.choices, default=NumberStatus.RTP)
    dealer_name = models.CharField(max_length=100, null=True)
    dealer_contact = models.CharField(max_length=100, null=True)

    price = models.IntegerField()
    purchase_price = models.IntegerField(default=0)
    discount = models.FloatField(default=0)

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AVAILABLE)

    categories = models.CharField(
        max_length=10,
        choices=NumberType.choices,
        default=NumberType.REGULAR
    )

    uploaded_by_admin = models.BooleanField(default=False)
    is_sold = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    is_upc_transferred = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    approval_status = models.BooleanField(default=False)
    approval_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.entry} - {self.vendor}"
