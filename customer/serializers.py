from rest_framework import serializers
from .models import Customer
from authentication.models import VN_User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = VN_User
        fields = ['username', 'email', 'phone']

class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = Customer
        fields = "__all__"

class CustomerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['full_address', 'address_area', 'state', 'country']
        
    def update(self, instance, validated_data):
        instance.full_address = validated_data.get('full_address', instance.full_address)
        instance.address_area = validated_data.get('address_area', instance.address_area)
        instance.state = validated_data.get('state', instance.state)
        instance.country = validated_data.get('country', instance.country)
        instance.save()
        return instance