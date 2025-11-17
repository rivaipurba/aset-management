from django.urls import path, include
from rest_framework.routers import DefaultRouter
from assets.views import AssetViewSet, AssetMovementViewSet

router = DefaultRouter()
router.register(r'assets', AssetViewSet, basename='asset')
router.register(r'movements', AssetMovementViewSet, basename='movement')

urlpatterns = [
    path('api/', include(router.urls)),
    # path('api/auth/', include('rest_framework.urls')),  # optional browsable login
]
