from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError as DRFValidationError
from django.core.exceptions import ValidationError as DjangoValidationError
from .models import Supplier, MunjiPurchase, RiceProduction, GlobalSettings, Expense, Category, MiscellaneousCost
from .serializers import SupplierSerializer, MunjiPurchaseSerializer, RiceProductionSerializer, GlobalSettingsSerializer, ExpenseSerializer, CategorySerializer, MiscellaneousCostSerializer,ChoiceSerializer

@api_view(['GET', 'POST'])
def global_settings(request):
    gs = GlobalSettings.get_instance()

    if request.method == 'POST':
        serializer = GlobalSettingsSerializer(gs, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    serializer = GlobalSettingsSerializer(gs)
    return Response(serializer.data)
class GlobalSettingsViewSet(viewsets.ModelViewSet):
    serializer_class = GlobalSettingsSerializer
    queryset = GlobalSettings.objects.all()

    def get_object(self):
        # Always return the singleton instance (id=1 or first record)
        obj, created = GlobalSettings.objects.get_or_create(id=1)
        return obj

    def list(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(obj)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        # Block creation of new rows
        return Response(
            {"detail": "Creation not allowed. Use PUT/PATCH to update existing settings."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def destroy(self, request, *args, **kwargs):
        # Block delete too
        return Response(
            {"detail": "Deletion not allowed for global settings."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )
class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = ChoiceSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = ChoiceSerializer

class MunjiPurchaseViewSet(viewsets.ModelViewSet):
    queryset = MunjiPurchase.objects.all()
    serializer_class = MunjiPurchaseSerializer
    
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except DjangoValidationError as e:
            if hasattr(e, 'message_dict'):
                return Response({'error': e.message_dict}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except DjangoValidationError as e:
            if hasattr(e, 'message_dict'):
                return Response({'error': e.message_dict}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class RiceProductionViewSet(viewsets.ModelViewSet):
    queryset = RiceProduction.objects.all()
    serializer_class = RiceProductionSerializer
    
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except DjangoValidationError as e:
            if hasattr(e, 'message_dict'):
                return Response({'error': e.message_dict}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except DjangoValidationError as e:
            if hasattr(e, 'message_dict'):
                return Response({'error': e.message_dict}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class GlobalSettingsViewSet(viewsets.ModelViewSet):
    queryset = GlobalSettings.objects.all()
    serializer_class = GlobalSettingsSerializer

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

class MiscellaneousCostViewSet(viewsets.ModelViewSet):
    queryset = MiscellaneousCost.objects.all()
    serializer_class = MiscellaneousCostSerializer
    
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except DjangoValidationError as e:
            if hasattr(e, 'message_dict'):
                return Response({'error': e.message_dict}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except DjangoValidationError as e:
            if hasattr(e, 'message_dict'):
                return Response({'error': e.message_dict}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_payment_choices(request):
    choices = [
        {'value': 'Cash', 'label': 'Cash'},
        {'value': 'Credit', 'label': 'Credit'},
    ]
    return Response(choices)

@api_view(['GET'])
def recent_purchases(request):
    purchases = MunjiPurchase.objects.order_by('-created_at')[:10]  # latest 10
    serializer = MunjiPurchaseSerializer(purchases, many=True)
    return Response(serializer.data)