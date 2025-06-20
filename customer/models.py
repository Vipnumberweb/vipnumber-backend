from django.db import models
from authentication.models import VN_User
import uuid

class Customer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(VN_User, on_delete=models.CASCADE, related_name="customer_profile")
    full_address = models.TextField()
    address_area = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

