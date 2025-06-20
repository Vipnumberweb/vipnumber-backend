from django.db import models
import uuid
from number.models import Number
from customer.models import Customer

class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='cart_items')
    number = models.ForeignKey(Number, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['customer', 'number']  # Prevent duplicate numbers in cart
        ordering = ['-created_at']  # Order by most recently added

    def __str__(self):
        return f"{self.customer.user.username}'s cart - {self.number.entry}"
