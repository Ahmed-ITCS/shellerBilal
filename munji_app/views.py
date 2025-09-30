from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Supplier, MunjiPurchase, RiceProduction, GlobalSettings,Expense
from .serializers import SupplierSerializer, MunjiPurchaseSerializer, RiceProductionSerializer, GlobalSettingsSerializer,ExpenseSerializer

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

class MunjiPurchaseViewSet(viewsets.ModelViewSet):
    queryset = MunjiPurchase.objects.all()
    serializer_class = MunjiPurchaseSerializer

class RiceProductionViewSet(viewsets.ModelViewSet):
    queryset = RiceProduction.objects.all()
    serializer_class = RiceProductionSerializer

class GlobalSettingsViewSet(viewsets.ModelViewSet):
    queryset = GlobalSettings.objects.all()
    serializer_class = GlobalSettingsSerializer
class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

@api_view(['GET'])
def get_payment_choices(request):
    choices = [
        {'value': 'Cash', 'label': 'Cash'},
        {'value': 'Credit', 'label': 'Credit'},
    ]
    return Response(choices)
