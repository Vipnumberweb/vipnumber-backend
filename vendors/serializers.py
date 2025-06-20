from rest_framework import serializers
from .models import Vendor
from django.contrib.auth import get_user_model

User = get_user_model()

class AdminCreateVendorSerializer(serializers.ModelSerializer):
    # User fields
    username = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False, allow_blank=True)
    phone = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = Vendor
        fields = [
            # User info
            'username', 
            'first_name', 'last_name', 'email', 'phone', 'password',

            # Vendor basic info
            'business_name', 'full_address', 'address_area', 'state', 'country', 'gst_number',

            # Bank/UPI fields
            'account_holder_name', 'account_number', 'bank_name', 'account_type',
            'ifsc_code', 'upi_id', 'google_pay_number', 'phone_pay_number', 'paytm_number',

            # Documents
            'aadhar_card', 'pan_card', 'agreement_form',
        ]
        extra_kwargs = {
            'aadhar_card': {'required': False},
            'pan_card': {'required': False},
            'agreement_form': {'required': False},
            'gst_number': {'required': False},
            'full_address': {'required': False},
            'address_area': {'required': False},
            'state': {'required': False},
            'country': {'required': False},
        }

    def validate(self, data):
        phone = data.get("phone")
        email = data.get("email")

        if User.objects.filter(phone=phone).exists():
            raise serializers.ValidationError({"phone": "User with this phone already exists."})
        if email and User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "User with this email already exists."})
        return data

    def create(self, validated_data):
        # Extract user fields
        user_data = {
            'username': validated_data.pop('username'),
            'first_name': validated_data.pop('first_name'),
            'last_name': validated_data.pop('last_name', ''),
            'email': validated_data.pop('email', ''),
            'phone': validated_data.pop('phone'),
            'password': validated_data.pop('password'),
            'is_vendor': True
        }

        user = User.objects.create_user(**user_data)
        user.phone_verified = False
        user.save()

        # Auto-approve vendor by admin
        vendor = Vendor.objects.create(user=user, is_approved=True, **validated_data)
        return vendor
    
class AdminUpdateVendorSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False, allow_blank=True)
    phone = serializers.CharField(required=False)

    class Meta:
        model = Vendor
        fields = [
            # User info
            'username', 'first_name', 'last_name', 'email', 'phone',

            # Vendor info
            'business_name', 'full_address', 'address_area', 'state', 'country', 'gst_number',

            # Bank/UPI
            'account_holder_name', 'account_number', 'bank_name', 'account_type',
            'ifsc_code', 'upi_id', 'google_pay_number', 'phone_pay_number', 'paytm_number',

            # Documents
            'aadhar_card', 'pan_card', 'agreement_form',
        ]

    def update(self, instance, validated_data):
        # Update user fields
        user = instance.user
        user.username = validated_data.get('username', user.username)
        user.first_name = validated_data.get('first_name', user.first_name)
        user.last_name = validated_data.get('last_name', user.last_name)
        user.email = validated_data.get('email', user.email)
        user.phone = validated_data.get('phone', user.phone)
        user.save()

        # Update vendor fields
        for attr, value in validated_data.items():
            if hasattr(instance, attr):
                setattr(instance, attr, value)

        instance.save()
        return instance


class VendorSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField(source="user.id", read_only=True)  # Fetch UUID of the user

    class Meta:
        model = Vendor
        fields = [
            "user_id", "id", "business_name", "full_address", "address_area",
            "state", "country", "aadhar_card", "pan_card", "agreement_form", "created_at"
        ]
        extra_kwargs = {
            "agreement_form": {"required": False},
            "address_area": {"required": False},
            "state": {"required": False},
            "country": {"required": False},
            "full_address": {"required": False},
            "business_name": {"required": False},
        }

    def create(self, validated_data):
        """Ensure a vendor profile is created only once per user"""
        user = self.context["request"].user
        if Vendor.objects.filter(user=user).exists():
            raise serializers.ValidationError("Vendor profile already exists for this user.")
        return Vendor.objects.create(user=user, **validated_data)


class AllVendorSerializers(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    contact = serializers.CharField(source='user.phone')
    total_numbers = serializers.SerializerMethodField()
    class Meta:
        fields = ['id', 'username', 'contact', 'business_name', 'is_approved', 'total_numbers']
        model = Vendor

    def get_total_numbers(self, obj):
        return obj.numbers.count()

class AdminVendorListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.EmailField(source="user.email")
    phone = serializers.CharField(source="user.phone")
    is_active = serializers.BooleanField(source="user.is_active")

    class Meta:
        model = Vendor
        fields = [
            # User info
            'id', 'username', 'first_name', 'last_name', 'email', 'phone', 'is_active',

            # Vendor info
            'business_name', 'full_address', 'address_area', 'state', 'country', 'gst_number',
            'is_approved',

            # Bank/UPI
            'account_holder_name', 'account_number', 'bank_name', 'account_type',
            'ifsc_code', 'upi_id', 'google_pay_number', 'phone_pay_number', 'paytm_number',

            # Documents
            'aadhar_card', 'pan_card', 'agreement_form',

            # Metadata
            'created_at'
        ]
