from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SupplierViewSet, MunjiPurchaseViewSet, RiceProductionViewSet, GlobalSettingsViewSet,ExpenseViewSet, get_payment_choices, CategoryViewSet, MiscellaneousCostViewSet,recent_purchases,global_settings

router = DefaultRouter()
router.register(r'suppliers', SupplierViewSet)
router.register(r'purchases', MunjiPurchaseViewSet)
#router.register(r'production', RiceProductionViewSet)
router.register(r'globals', GlobalSettingsViewSet)
router.register(r'expenses', ExpenseViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'miscellaneous-costs', MiscellaneousCostViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('payment-choices/', get_payment_choices, name='payment-choices'),
    path('recent_purchases/', recent_purchases, name='recent_purchases'),
    #path('global/', global_settings, name='global-settings'),
]