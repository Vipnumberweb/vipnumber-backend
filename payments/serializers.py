from rest_framework import serializers
from .models import RazorpayPayment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RazorpayPayment
        fields = '__all__'

