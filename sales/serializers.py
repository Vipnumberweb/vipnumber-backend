from rest_framework import serializers
from .models import Sales
from number.models import Number
from vendors.models import Vendor

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['id', 'business_name', 'is_approved']

class NumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Number
        fields = ['id', 'entry', 'price']

class NumberSerializerTotalSales(serializers.ModelSerializer):
    class Meta:
        model = Number
        fields = ['id', 'entry', 'price', 'pattern']

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sales
        fields = ['id', 'customer_name', 'customer_email', 'customer_phone']


class SalesSerializer(serializers.ModelSerializer):
    numbers = NumberSerializer(many=True, read_only=True)
    vendors = VendorSerializer(many=True, read_only=True)  # Shows business names
    vendor_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Vendor.objects.all(), write_only=True, required=False
    )

    customer_name = serializers.SerializerMethodField()
    customer_phone = serializers.SerializerMethodField()
    customer_email = serializers.SerializerMethodField()

    class Meta:
        model = Sales
        fields = "__all__"
        extra_fields = ['customer_name', 'customer_phone', 'customer_email', 'vendor_ids']

    def update(self, instance, validated_data):
        vendor_ids = validated_data.pop('vendor_ids', None)
        if vendor_ids is not None:
            instance.vendors.set(vendor_ids)
        return super().update(instance, validated_data)

    def get_customer_name(self, obj):
        return getattr(obj.customer.user, 'get_full_name', lambda: None)()

    def get_customer_phone(self, obj):
        return getattr(obj.customer.user, 'phone', None)

    def get_customer_email(self, obj):
        return getattr(obj.customer.user, 'email', None)


class TotalSalesSerializer(serializers.ModelSerializer):
    numbers = serializers.SerializerMethodField()
    vendor = VendorSerializer(many=True, read_only=True)
    # category = serializers.SerializerMethodField()  # comment this out if not implemented
    price_range = serializers.SerializerMethodField()

    class Meta:
        model = Sales
        fields = "__all__"

    def get_numbers(self, obj):
        numbers = obj.numbers.all()
        vendor_id = self.context.get("vendor")
        min_price = self.context.get("min_price")
        max_price = self.context.get("max_price")
        pattern_id = self.context.get("pattern")
        category = self.context.get("category")

        if vendor_id:
            numbers = numbers.filter(vendor__id=vendor_id)
        if min_price:
            numbers = numbers.filter(price__gte=min_price)
        if max_price:
            numbers = numbers.filter(price__lte=max_price)
        if pattern_id:
            numbers = numbers.filter(pattern__id=pattern_id)
        if category:
            numbers = numbers.filter(categories=category)

        return NumberSerializer(numbers, many=True).data

    def get_price_range(self, obj):
        prices = obj.numbers.all().values_list("price", flat=True)
        if not prices:
            return "₹0"
        return f"₹{min(prices)} – ₹{max(prices)}"


class CustomerPurchasesSerializer(serializers.ModelSerializer):
    numbers = NumberSerializer(many=True, read_only=True)
    class Meta:
        model = Sales
        fields = "__all__"
