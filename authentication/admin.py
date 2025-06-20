from django.contrib import admin
from .models import VN_User
from customer.models import Customer
from vendors.models import Vendor

@admin.register(VN_User)
class VNUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'phone', 'is_vendor', 'is_active')
    search_fields = ('username', 'email', 'phone')
    list_filter = ('is_vendor', 'is_active')
    ordering = ('id',)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'full_address', 'state', 'country')
    search_fields = ('user__username', 'user__email')

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'business_name', 'full_address', 'state', 'country')
    search_fields = ('user__username', 'business_name')
