from rest_framework import serializers
from .models import CommissionByCategories, CommissionSettings, CommissionByPriceRange

class CommissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommissionByCategories
        fields = '__all__'

class CommissionSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommissionSettings
        fields = '__all__'

class CommissionPriceRange(serializers.ModelSerializer):
    class Meta:
        model = CommissionByPriceRange
        fields = "__all__"

