from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SupplierViewSet, MunjiPurchaseViewSet, RiceProductionViewSet, GlobalSettingsViewSet,ExpenseViewSet, get_payment_choices, get_category_choices

router = DefaultRouter()
router.register(r'suppliers', SupplierViewSet)
router.register(r'purchases', MunjiPurchaseViewSet)
router.register(r'production', RiceProductionViewSet)
router.register(r'globals', GlobalSettingsViewSet)
router.register(r'expenses', ExpenseViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('payment-choices/', get_payment_choices, name='payment-choices'),
    path('category-choices/', get_category_choices, name='category-choices'),
]
