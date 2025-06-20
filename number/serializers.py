from rest_framework import serializers
from .models import *

class NumberSerializers(serializers.ModelSerializer):
    vendor_name = serializers.CharField(source='vendor.business_name', read_only=True)
    pattern_text = serializers.CharField(source='pattern.pattern', read_only=True)
    class Meta:
        model = Number
        fields = [
            'id',
            'entry',
            'parent_operator',
            'current_operator',
            'circle',
            'numberStatus',
            'dealer_name',
            'dealer_contact',
            'price',
            'purchase_price',
            'discount',
            'status',
            'categories',
            'uploaded_by_admin',
            'is_sold',
            'is_upc_transferred',
            'approval_status',
            'approval_date',
            'is_rejected',
            'created_at',
            'vendor',           
            'vendor_name',      
            'pattern',          
            'pattern_text',     
        ]
        read_only_fields = ["created_at", "vendor", "uploaded_by_admin"]

class PatternSerializers(serializers.ModelSerializer):
    class Meta: 
        model = Pattern
        fields = "__all__"

class UnsoldNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Number
        fields = [
            'id',
            'entry',
            'vendor',
            'price',
            'discount',
            'status',
            'categories',
            'is_sold',
            'numberStatus',
            'parent_operator',
            'current_operator',
            'circle',
            'created_at',
        ]