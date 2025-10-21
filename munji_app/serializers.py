from rest_framework import serializers
from .models import Supplier, MunjiPurchase, RiceProduction, GlobalSettings,Expense, Category,MiscellaneousCost



class ChoiceSerializer(serializers.ModelSerializer):
    value = serializers.IntegerField(source='id')
    label = serializers.CharField(source='name')

    class Meta:
        model = Supplier  # or Category
        fields = ['value', 'label']


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'



class MunjiPurchaseSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)

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


class MiscellaneousCostSerializer(serializers.ModelSerializer):
    class Meta:
        model = MiscellaneousCost
        fields = '__all__'
