from rest_framework import serializers
from .models import Asset, AssetType, ComputerSpec, PrinterSpec, MonitorSpec, ScannerSpec, AssetMovement

class ComputerSpecSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComputerSpec
        fields = ['ram', 'storage', 'processor', 'os']

class PrinterSpecSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrinterSpec
        fields = ['is_color']

class MonitorSpecSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitorSpec
        fields = ['size_inch']

class ScannerSpecSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScannerSpec
        fields = ['dpi', 'connection_type']

class AssetMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetMovement
        fields = ['id','asset','from_location','to_location','performed_by','performed_at','note']
        read_only_fields = ['id','performed_at']

class AssetSerializer(serializers.ModelSerializer):
    asset_type_code = serializers.CharField(source='asset_type.code', read_only=True)

    # Note: source points to related name on Asset model (e.g., 'computerspec')
    computer_spec = ComputerSpecSerializer(source='computerspec', required=False, allow_null=True)
    printer_spec = PrinterSpecSerializer(source='printerspec', required=False, allow_null=True)
    monitor_spec = MonitorSpecSerializer(source='monitorspec', required=False, allow_null=True)
    scanner_spec = ScannerSpecSerializer(source='scannerspec', required=False, allow_null=True)

    class Meta:
        model = Asset
        fields = [
            'id','asset_type','asset_type_code','name','serial_number','maker','owner','location',
            'status','condition','notes','created_at','updated_at',
            'computer_spec','printer_spec','monitor_spec','scanner_spec'
        ]
        read_only_fields = ['created_at','updated_at','asset_type_code']

    def _pop_spec_keys(self, validated_data):
        """
        Extract and remove any nested spec data from validated_data.
        Accepts both 'computer_spec' and 'computerspec' (and similar).
        Returns dict with normalized keys: computer_spec, printer_spec, monitor_spec, scanner_spec
        """
        spec_keys_map = {
            'computerspec': 'computer_spec',
            'computer_spec': 'computer_spec',
            'printerspec': 'printer_spec',
            'printer_spec': 'printer_spec',
            'monitorspec': 'monitor_spec',
            'monitor_spec': 'monitor_spec',
            'scannerspec': 'scanner_spec',
            'scanner_spec': 'scanner_spec',
        }
        specs = {}
        # iterate over a copy because we'll pop
        for key in list(validated_data.keys()):
            low = key.lower()
            if low in spec_keys_map:
                normalized = spec_keys_map[low]
                specs[normalized] = validated_data.pop(key)
        return specs

    def create(self, validated_data):
        # Extract nested spec dicts (if any) so they won't be passed to Asset.objects.create()
        specs = self._pop_spec_keys(validated_data)

        # Create the main Asset instance with remaining fields
        asset = Asset.objects.create(**validated_data)

        # Determine asset type code (lowercase) to decide which spec to create
        asset_type_code = asset.asset_type.code.lower() if asset.asset_type and asset.asset_type.code else ''

        # For each spec, create related spec row if provided
        try:
            if asset_type_code in ('laptop', 'pc'):
                cs_data = specs.get('computer_spec') or {}
                # If the serializer used source='computerspec', that data may be nested dict or validated_data form
                if cs_data:
                    ComputerSpec.objects.create(asset_id=asset.id, **cs_data)
            elif asset_type_code == 'printer':
                ps_data = specs.get('printer_spec') or {}
                if ps_data:
                    PrinterSpec.objects.create(asset_id=asset.id, **ps_data)
            elif asset_type_code == 'monitor':
                ms_data = specs.get('monitor_spec') or {}
                if ms_data:
                    MonitorSpec.objects.create(asset_id=asset.id, **ms_data)
            elif asset_type_code == 'scanner':
                ss_data = specs.get('scanner_spec') or {}
                if ss_data:
                    ScannerSpec.objects.create(asset_id=asset.id, **ss_data)
        except TypeError as e:
            # If payload shape is wrong (e.g., non-dict), raise serializer error
            raise serializers.ValidationError({'specs': f'Invalid spec data: {e}'})

        return asset

    def update(self, instance, validated_data):
        # Extract spec blocks (pop them so we only iterate model fields)
        specs = self._pop_spec_keys(validated_data)

        # Update standard Asset fields
        for attr, val in validated_data.items():
            # only set if field exists on model
            if hasattr(instance, attr):
                setattr(instance, attr, val)
        instance.save()

        # Update/create spec rows depending on asset type
        asset_type_code = instance.asset_type.code.lower() if instance.asset_type and instance.asset_type.code else ''

        # Utility: safe update helper
        def _apply_spec(model_cls, spec_dict):
            if not isinstance(spec_dict, dict):
                return
            spec_obj, created = model_cls.objects.get_or_create(asset_id=instance.id)
            for k, v in spec_dict.items():
                if hasattr(spec_obj, k):
                    setattr(spec_obj, k, v)
            spec_obj.save()

        if asset_type_code in ('laptop', 'pc'):
            cs_data = specs.get('computer_spec')
            if cs_data is not None:
                _apply_spec(ComputerSpec, cs_data)
        elif asset_type_code == 'printer':
            ps_data = specs.get('printer_spec')
            if ps_data is not None:
                _apply_spec(PrinterSpec, ps_data)
        elif asset_type_code == 'monitor':
            ms_data = specs.get('monitor_spec')
            if ms_data is not None:
                _apply_spec(MonitorSpec, ms_data)
        elif asset_type_code == 'scanner':
            ss_data = specs.get('scanner_spec')
            if ss_data is not None:
                _apply_spec(ScannerSpec, ss_data)

        return instance
