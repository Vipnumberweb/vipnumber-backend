from rest_framework import serializers
from .models import Cart
from number.serializers import NumberSerializers

class CartSerializer(serializers.ModelSerializer):
    number_details = NumberSerializers(source='number', read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'customer', 'number', 'number_details', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at', 'customer']

    def create(self, validated_data):
        # Get the customer from the context
        request = self.context.get('request')
        if not request or not request.user:
            raise serializers.ValidationError("Must be authenticated to create cart items")
        try:
            customer = request.user.customer_profile
        except:
            raise serializers.ValidationError("Must have a customer profile to create cart items")
            
        validated_data['customer'] = customer
        return super().create(validated_data)