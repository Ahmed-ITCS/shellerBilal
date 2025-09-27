from rest_framework import serializers
from .models import Supplier, MunjiPurchase, RiceProduction, GlobalSettings,Expense


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'


class MunjiPurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = MunjiPurchase
        fields = '__all__'


class RiceProductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiceProduction
        fields = '__all__'


class GlobalSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlobalSettings
        fields = '__all__'
class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'
