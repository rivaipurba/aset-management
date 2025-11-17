from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import filters
from .models import Asset, AssetType, AssetMovement
from .serializers import AssetSerializer, AssetMovementSerializer

class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all().select_related('asset_type')
    serializer_class = AssetSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name','serial_number','maker','owner','location']
    ordering_fields = ['name','created_at','updated_at','status']
    # filtering by query params manually for type/status/location
    def get_queryset(self):
        qs = super().get_queryset()
        asset_type = self.request.query_params.get('type')  # expects code like 'laptop'
        status = self.request.query_params.get('status')
        location = self.request.query_params.get('location')
        owner = self.request.query_params.get('owner')
        if asset_type:
            qs = qs.filter(asset_type__code__iexact=asset_type)
        if status:
            qs = qs.filter(status__iexact=status)
        if location:
            qs = qs.filter(location__icontains=location)
        if owner:
            qs = qs.filter(owner__icontains=owner)
        return qs

    @action(detail=True, methods=['post'])
    def move(self, request, pk=None):
        """
        POST /api/assets/{id}/move
        payload: { "to_location": "...", "performed_by": "...", "note": "..." }
        """
        asset = self.get_object()
        to_location = request.data.get('to_location')
        performed_by = request.data.get('performed_by')
        note = request.data.get('note', '')
        if not to_location:
            return Response({"detail":"to_location is required"}, status=status.HTTP_400_BAD_REQUEST)
        # save movement
        movement = AssetMovement.objects.create(
            asset_id=asset.id,
            from_location=asset.location,
            to_location=to_location,
            performed_by=performed_by,
            # performed_at will be set by DB default; for managed=False we set manually:
            performed_at = None
        )
        # If performed_at is nullable in model; but DB has default now(). For safety:
        # Use raw SQL fallback if needed; else, update using now() here
        from django.utils import timezone
        movement.performed_at = timezone.now()
        movement.save()
        # update asset location
        asset.location = to_location
        asset.save()
        return Response({"detail":"moved","movement_id": movement.id})

class AssetMovementViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AssetMovement.objects.all().order_by('-performed_at')
    serializer_class = AssetMovementSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['performed_by','from_location','to_location','note']
    ordering_fields = ['performed_at']
