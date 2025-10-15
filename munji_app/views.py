from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError as DRFValidationError
from django.core.exceptions import ValidationError as DjangoValidationError
from .models import (
    Supplier, MunjiPurchase, RiceProduction, GlobalSettings,
    Expense, Category, MiscellaneousCost
)
from .serializers import (
    SupplierSerializer, MunjiPurchaseSerializer, RiceProductionSerializer,
    GlobalSettingsSerializer, ExpenseSerializer, CategorySerializer,
    MiscellaneousCostSerializer, ChoiceSerializer
)
from decimal import Decimal
from datetime import datetime, timedelta
from rest_framework.pagination import PageNumberPagination


# -------------------------------
# Global Settings
# -------------------------------
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
    queryset = GlobalSettings.objects.all()
    serializer_class = GlobalSettingsSerializer

    def get_object(self):
        obj, created = GlobalSettings.objects.get_or_create(id=1)
        return obj

    def update(self, request, *args, **kwargs):
        return self._custom_update(request)

    def partial_update(self, request, *args, **kwargs):
        return self._custom_update(request)

    def _custom_update(self, request):
        gs = self.get_object()
        data = request.data

        def to_decimal(val):
            try:
                return Decimal(str(val))
            except:
                return Decimal(0)

        if "opening_balance" in data:
            gs.opening_balance += to_decimal(data["opening_balance"])

        if "cash_in_hand" in data:
            amount = to_decimal(data["cash_in_hand"])
            if gs.opening_balance < amount:
                return Response(
                    {"error": "Not enough capital to move into cash."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            gs.cash_in_hand += amount
            gs.opening_balance -= amount

        if "sales" in data:
            gs.sales += to_decimal(data["sales"])

        if "total_munji" in data:
            gs.total_munji += to_decimal(data["total_munji"])

        gs.save()
        serializer = self.get_serializer(gs)
        return Response(serializer.data)


# -------------------------------
# Core Data ViewSets
# -------------------------------
class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all().order_by('-created_at')
    serializer_class = ChoiceSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('-created_at')
    serializer_class = ChoiceSerializer


class MunjiPurchaseViewSet(viewsets.ModelViewSet):
    queryset = MunjiPurchase.objects.all().order_by('-created_at')
    serializer_class = MunjiPurchaseSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        payment_type = self.request.query_params.get('payment_type')
        category = self.request.query_params.get('category')

        if start_date:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            queryset = queryset.filter(created_at__gte=start_date)

        if end_date:
            end_date = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
            queryset = queryset.filter(created_at__lt=end_date)

        if payment_type:
            queryset = queryset.filter(payment_type__iexact=payment_type)

        if category:
            queryset = queryset.filter(category__iexact=category)

        return queryset.order_by('-created_at')

    @action(detail=True, methods=['get'])
    def expenses(self, request, pk=None):
        purchase = self.get_object()
        expenses = purchase.expenses.all().order_by('-created_at')
        page = self.paginate_queryset(expenses)
        if page is not None:
            serializer = ExpenseSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = ExpenseSerializer(expenses, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except DjangoValidationError as e:
            return Response({'error': getattr(e, 'message_dict', str(e))}, status=400)

    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except DjangoValidationError as e:
            return Response({'error': getattr(e, 'message_dict', str(e))}, status=400)


class RiceProductionViewSet(viewsets.ModelViewSet):
    queryset = RiceProduction.objects.all().order_by('-created_at')
    serializer_class = RiceProductionSerializer

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except DjangoValidationError as e:
            return Response({'error': getattr(e, 'message_dict', str(e))}, status=400)

    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except DjangoValidationError as e:
            return Response({'error': getattr(e, 'message_dict', str(e))}, status=400)


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all().order_by('-created_at')
    serializer_class = ExpenseSerializer


class MiscellaneousCostViewSet(viewsets.ModelViewSet):
    queryset = MiscellaneousCost.objects.all().order_by('-created_at')
    serializer_class = MiscellaneousCostSerializer

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except DjangoValidationError as e:
            return Response({'error': getattr(e, 'message_dict', str(e))}, status=400)

    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except DjangoValidationError as e:
            return Response({'error': getattr(e, 'message_dict', str(e))}, status=400)


# -------------------------------
# Utility Endpoints
# -------------------------------
@api_view(['GET'])
def get_payment_choices(request):
    choices = [
        {'value': 'Cash', 'label': 'Cash'},
        {'value': 'Credit', 'label': 'Credit'},
    ]
    return Response(choices)


@api_view(['GET'])
def recent_purchases(request):
    queryset = MunjiPurchase.objects.all().order_by('-created_at')
    paginator = PageNumberPagination()
    paginator.page_size = 10
    result_page = paginator.paginate_queryset(queryset, request)
    serializer = MunjiPurchaseSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)
