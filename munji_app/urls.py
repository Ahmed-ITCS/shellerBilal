from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SupplierViewSet, MunjiPurchaseViewSet, RiceProductionViewSet, GlobalSettingsViewSet,ExpenseViewSet

router = DefaultRouter()
router.register(r'suppliers', SupplierViewSet)
router.register(r'purchases', MunjiPurchaseViewSet)
router.register(r'production', RiceProductionViewSet)
router.register(r'globals', GlobalSettingsViewSet)
router.register(r'expenses', ExpenseViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
