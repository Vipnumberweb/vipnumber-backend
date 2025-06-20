from django.db import models

# Create your models here
import uuid
from sales.models import Sales

class PaymentStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    COMPLETED = 'completed', 'Completed'
    FAILED = 'failed', 'Failed'
    REFUNDED = 'refunded', 'Refunded'

class RazorpayPayment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sale = models.OneToOneField(
        Sales,
        on_delete=models.CASCADE,
        related_name='razorpay_payment'
    )
    razorpay_order_id = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Razorpay order ID for the payment"
    )
    razorpay_payment_id = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Razorpay payment ID"
    )
    razorpay_signature = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Razorpay payment signature for verification"
    )
    amount = models.FloatField(
        help_text="Payment amount in INR"
    )
    status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    payment_method = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="Payment method used (e.g., card, upi, netbanking)"
    )
    failure_reason = models.TextField(
        null=True,
        blank=True,
        help_text="Reason for payment failure, if applicable"
    )

    def __str__(self):
        return f"Payment {self.id} for Sale {self.sale.id} - {self.status}"

    class Meta:
        ordering = ['-created_at']