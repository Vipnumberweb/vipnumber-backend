from django.db import models
import uuid
from number.models import Pattern
# Create your models here.

class CommissionByCategories(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.OneToOneField(Pattern, on_delete=models.CASCADE, related_name="category")
    commission = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

class CommissionSettings(models.Model):
    is_add_on_new_number = models.BooleanField(default=False)
    is_add_on_exist_number = models.BooleanField(default=False)
    exist_updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    new_updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)


class CommissionByPriceRange(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    min_price = models.FloatField()
    max_price = models.FloatField()
    commission = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    updated_at = models.DateTimeField(auto_now_add=True, auto_now=False)
