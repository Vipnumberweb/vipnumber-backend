from django.db import models
from number.models import Number
from vendors.models import Vendor
from customer.models import Customer
import uuid

# class Sales(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     sales_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
#     numbers = models.ManyToManyField(Number, related_name="number_sales")
#     vendors = models.ManyToManyField(Vendor, related_name="sales")
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="purchases")
#     final_price = models.FloatField()
#     status = models.CharField(max_length=20, choices=[("pending", "Pending"), ("completed", "Completed"), ("canceled", "Canceled")], default="pending")
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.numbers} sold to {self.customer.user.username} by VIPNUMBERWEB"

class Sales(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sales_id = models.CharField(max_length=20, unique=True, blank=True, null=True) # VWID000001, VWID000002
    numbers = models.ManyToManyField(Number, related_name="number_sales")
    vendors = models.ManyToManyField(Vendor, related_name="sales") # To store multiple vendors for multiple numbers if needed
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="purchases")

    # New fields for client requirements
    order_rate = models.FloatField(default=0.0) # Base price of the VIP number (sum of numbers.price)
    total_excl_gst = models.FloatField(default=0.0) # Calculated total excluding GST
    total_incl_gst = models.FloatField(default=0.0) # Calculated total including GST
    vendor_rate = models.FloatField(default=0.0) # Sum of prices at which vendors supplied the numbers

    # Client-specific status fields
    payment_status = models.CharField(
        max_length=20,
        choices=[("paid", "Paid"), ("pending", "Pending"), ("refunded", "Refunded")],
        default="pending"
    )
    # Re-evaluate or expand your existing `status` field to match client's "Order Status"
    # You might rename 'status' to 'order_status' for clarity if it fully replaces it.
    order_status = models.CharField(
        max_length=20,
        choices=[
            ("new", "New"),
            ("closed_won", "Closed-Won"),
            ("duplicate", "Duplicate"),
            ("cancelled", "Cancelled"),
            ("wrong_data", "Wrong Data"),
            ("pending", "Pending"), # Keep existing if still relevant
            ("completed", "Completed"), # Keep existing if still relevant
            # Add other statuses as needed
        ],
        default="new" # Or whatever makes sense as an initial state
    )

    agent_name = models.CharField(max_length=50, blank=True, null=True)
    agent_order_type = models.CharField(max_length=50, blank=True, null=True)

    # Existing fields
    final_price = models.FloatField() # Consider if this is 'total_incl_gst' or something else
    created_at = models.DateTimeField(auto_now_add=True)

    # For UPC Code (assuming it's a field related to the sale/order)
    upc_code = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"Sale {self.sales_id or self.id} to {self.customer.user.email}" # Assuming Customer has a 'name' attribute

    # You might want to override save() to auto-calculate totals and assign sales_id
    def save(self, *args, **kwargs):
        if not self.sales_id and self.pk: # Assign sales_id only if new object
            # This is a placeholder; you'd need logic to generate a unique VWIDXXXXXX
            # based on the last sales_id or a counter.
            # For simplicity, let's just use the 'id' for now for demonstration.
            # In a real app, you'd query the last sales_id and increment.
            # Example (simplified):
            # last_sale = Sales.objects.order_by('-created_at').first()
            # last_id_num = int(last_sale.sales_id[4:]) if last_sale and last_sale.sales_id else 0
            # self.sales_id = f"VWID{last_id_num + 1:06d}"
            pass # Keep it blank for now, let Django handle unique or populate it via signal/separate logic

        # Auto-calculate totals (these should be based on `numbers` and `vendors` related objects)
        # You'll need to fetch related objects here or ensure they are present before saving
        # if self.numbers.exists():
        #     self.order_rate = sum(num.price for num in self.numbers.all())
        #     # Add logic for GST calculation here
        #     # self.total_excl_gst = self.order_rate
        #     # self.total_incl_gst = self.order_rate * 1.18 # Example for 18% GST
        # if self.vendors.exists():
        #     self.vendor_rate = sum(vendor_num_rate for vendor_num_rate in self.vendors.all()) # This logic needs refinement based on your vendor-number relationship

        super().save(*args, **kwargs)