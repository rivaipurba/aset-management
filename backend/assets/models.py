from django.db import models

class AssetType(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField()

    class Meta:
        db_table = "asset_types"
        managed = False  # sudah dibuat oleh SQL seed; set True kalau mau Django mengelola

class Asset(models.Model):
    id = models.AutoField(primary_key=True)
    asset_type = models.ForeignKey(AssetType, db_column='asset_type_id', on_delete=models.RESTRICT)
    name = models.CharField(max_length=255)
    serial_number = models.CharField(max_length=255, unique=True, null=True, blank=True, db_index=True)
    maker = models.CharField(max_length=255, null=True, blank=True)
    owner = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=50, default='available')
    condition = models.CharField(max_length=50, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "assets"
        managed = False

class ComputerSpec(models.Model):
    id = models.AutoField(primary_key=True)
    asset = models.OneToOneField(Asset, db_column='asset_id', on_delete=models.CASCADE)
    ram = models.CharField(max_length=50, null=True, blank=True)
    storage = models.CharField(max_length=100, null=True, blank=True)
    processor = models.CharField(max_length=255, null=True, blank=True)
    os = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = "computer_specs"
        managed = False

class PrinterSpec(models.Model):
    id = models.AutoField(primary_key=True)
    asset = models.OneToOneField(Asset, db_column='asset_id', on_delete=models.CASCADE)
    is_color = models.BooleanField(default=False)

    class Meta:
        db_table = "printer_specs"
        managed = False

class MonitorSpec(models.Model):
    id = models.AutoField(primary_key=True)
    asset = models.OneToOneField(Asset, db_column='asset_id', on_delete=models.CASCADE)
    size_inch = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)

    class Meta:
        db_table = "monitor_specs"
        managed = False

class ScannerSpec(models.Model):
    id = models.AutoField(primary_key=True)
    asset = models.OneToOneField(Asset, db_column='asset_id', on_delete=models.CASCADE)
    dpi = models.IntegerField(null=True, blank=True)
    connection_type = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = "scanner_specs"
        managed = False

class AssetMovement(models.Model):
    id = models.AutoField(primary_key=True)
    asset = models.ForeignKey(Asset, db_column='asset_id', on_delete=models.CASCADE)
    from_location = models.CharField(max_length=255, null=True, blank=True)
    to_location = models.CharField(max_length=255)
    performed_by = models.CharField(max_length=255, null=True, blank=True)
    performed_at = models.DateTimeField()
    note = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "asset_movements"
        managed = False
