'''from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SupplierViewSet, MunjiPurchaseViewSet, RiceProductionViewSet, GlobalSettingsViewSet,ExpenseViewSet, get_payment_choices, CategoryViewSet, MiscellaneousCostViewSet

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
]'''
from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView

urlpatterns += [
    path('', include(router.urls)),
    path('payment-choices/', get_payment_choices, name='payment-choices'),

    # schema + swagger
    path('api/schema/', get_schema_view(
        title="Rice Mill API",
        description="API for Rice Mill System",
        version="1.0.0"
    ), name='api-schema'),
    
    path('api/docs/', TemplateView.as_view(
        template_name='swagger.html',
        extra_context={'schema_url':'api-schema'}
    ), name='swagger-ui'),
]