from rest_framework import serializers
from .models import Employee, PermanentAddress, CommunicationAddress, BankAccount

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['street', 'city', 'state', 'postal_code']
        abstract = True

class PermanentAddressSerializer(AddressSerializer):
    class Meta(AddressSerializer.Meta):
        model = PermanentAddress

class CommunicationAddressSerializer(AddressSerializer):
    class Meta(AddressSerializer.Meta):
        model = CommunicationAddress

class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = [
            'account_holder_name', 'bank_name', 'account_number',
            'ifsc_code', 'branch_name', 'account_type'
        ]

class EmployeeSerializer(serializers.ModelSerializer):
    permanent_address = PermanentAddressSerializer()
    communication_address = CommunicationAddressSerializer()
    bank_account = BankAccountSerializer()
    reporting_manager_name = serializers.CharField(source='reporting_manager.full_name', read_only=True)

    class Meta:
        model = Employee
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        permanent_address_data = validated_data.pop('permanent_address')
        communication_address_data = validated_data.pop('communication_address')
        bank_account_data = validated_data.pop('bank_account')

        # Create the addresses and bank account first
        permanent_address = PermanentAddress.objects.create(**permanent_address_data)
        communication_address = CommunicationAddress.objects.create(**communication_address_data)
        bank_account = BankAccount.objects.create(**bank_account_data)

        # Create the employee with the foreign key relationships
        employee = Employee.objects.create(
            permanent_address=permanent_address,
            communication_address=communication_address,
            bank_account=bank_account,
            **validated_data
        )
        return employee

    def update(self, instance, validated_data):
        # Update nested objects if provided
        if 'permanent_address' in validated_data:
            permanent_address_data = validated_data.pop('permanent_address')
            for attr, value in permanent_address_data.items():
                setattr(instance.permanent_address, attr, value)
            instance.permanent_address.save()

        if 'communication_address' in validated_data:
            communication_address_data = validated_data.pop('communication_address')
            for attr, value in communication_address_data.items():
                setattr(instance.communication_address, attr, value)
            instance.communication_address.save()

        if 'bank_account' in validated_data:
            bank_account_data = validated_data.pop('bank_account')
            for attr, value in bank_account_data.items():
                setattr(instance.bank_account, attr, value)
            instance.bank_account.save()

        # Update the employee instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance

class EmployeeListSerializer(serializers.ModelSerializer):
    reporting_manager_name = serializers.CharField(source='reporting_manager.full_name', read_only=True)

    class Meta:
        model = Employee
        fields = ['id', 'full_name', 'personal_mobile', 'personal_email', 'designation', 'reporting_manager_name', 'joining_date']