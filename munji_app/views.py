from rest_framework import viewsets
from .models import Supplier, MunjiPurchase, RiceProduction, GlobalSettings
from .serializers import SupplierSerializer, MunjiPurchaseSerializer, RiceProductionSerializer, GlobalSettingsSerializer

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
