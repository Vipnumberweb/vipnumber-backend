from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Sales

@receiver(pre_save, sender=Sales)
def generate_sales_id(sender, instance, **kwargs):
    if not instance.sales_id:
        last = Sales.objects.filter(sales_id__startswith='VWID').order_by('-created_at').first()
        if last and last.sales_id:
            try:
                last_number = int(last.sales_id.replace('VWID', ''))
            except ValueError:
                last_number = 0
        else:
            last_number = 0
        new_number = last_number + 1
        instance.sales_id = f'VWID{new_number:06d}'
