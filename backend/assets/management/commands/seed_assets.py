import pandas as pd
from django.core.management.base import BaseCommand
from assets.models import Asset, AssetType, ComputerSpec, PrinterSpec, MonitorSpec, ScannerSpec
from django.db import transaction
import re

from django.utils import timezone

class Command(BaseCommand):
    help = 'Seeds the database with assets from an Excel or CSV file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the Excel/CSV file')
        parser.add_argument('--sheet', type=str, help='Sheet name to read (optional)', default=None)

    def handle(self, *args, **options):
        file_path = options['file_path']
        sheet_name = options['sheet']
        self.stdout.write(f"Reading file: {file_path}")
        if sheet_name:
            self.stdout.write(f"Sheet: {sheet_name}")

        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            else:
                # Read specific sheet if provided, else read first sheet
                if sheet_name:
                    df = pd.read_excel(file_path, sheet_name=sheet_name)
                else:
                    df = pd.read_excel(file_path)
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error reading file: {e}"))
            return

        # Fill NaN with empty strings
        df = df.fillna('')

        success_count = 0
        error_count = 0

        with transaction.atomic():
            for index, row in df.iterrows():
                try:
                    # Normalize keys to handle potential whitespace issues
                    row = {k.strip(): v for k, v in row.items()}
                    
                    # 1. Determine Asset Type
                    # Check for 'Jenis' (specific file) or 'type' (generic)
                    raw_type = str(row.get('Jenis', row.get('type', 'laptop'))).lower().strip()
                    
                    # Map Indonesian terms if necessary
                    type_mapping = {
                        'laptop': 'laptop',
                        'pc': 'pc',
                        'komputer': 'pc',
                        'all in one': 'pc', # Map All In One to PC
                        'printer': 'printer',
                        'monitor': 'monitor',
                        'scanner': 'scanner',
                        'server': 'server'
                    }
                    type_code = type_mapping.get(raw_type, 'other')

                    asset_type, _ = AssetType.objects.get_or_create(
                        code=type_code,
                        defaults={
                            'name': type_code.capitalize(),
                            'created_at': timezone.now()
                        }
                    )

                    # 2. Construct Asset Data
                    # Handle 'Nama Asset' from Printer sheet which combines Merk and Type
                    nama_asset = str(row.get('Nama Asset', '')).strip()
                    
                    if nama_asset:
                        # Simple heuristic: first word is maker, rest is model
                        parts = nama_asset.split(' ', 1)
                        merk = parts[0]
                        model_type = parts[1] if len(parts) > 1 else ''
                        name = nama_asset
                    else:
                        merk = str(row.get('Merk', row.get('maker', ''))).strip()
                        model_type = str(row.get('Type', row.get('name', ''))).strip()
                        name = f"{merk} {model_type}".strip()
                    
                    if not name:
                        name = "Unknown Asset"

                    # Construct or Get Serial Number
                    # Priority: 'Serial Number' -> 'SN' -> Generated
                    serial = str(row.get('Serial Number', row.get('SN', row.get('serial_number', '')))).strip()
                    
                    if not serial:
                        # Generate a placeholder serial if missing
                        # Format: TYPE-MERK-NO or TYPE-MERK-INDEX
                        no_val = row.get('No', index + 1)
                        try:
                            no_int = int(no_val)
                        except:
                            no_int = index + 1
                        
                        prefix_type = type_code[:3].upper()
                        prefix_merk = merk[:3].upper() if merk else "UNK"
                        serial = f"{prefix_type}-{prefix_merk}-{no_int:04d}"
                        self.stdout.write(self.style.WARNING(f"Row {index}: Missing serial, generated: {serial}"))

                    # Owner & Location Mapping
                    # 'Posisi Barang...' -> Owner
                    # 'Bidang' -> Location
                    owner = str(row.get('Posisi Barang Di Meja/Dibawa Oleh', row.get('owner', ''))).strip()
                    location = str(row.get('Bidang', row.get('location', ''))).strip()
                    
                    condition_raw = str(row.get('Kondisi', row.get('condition', 'good'))).lower()
                    condition = 'good'
                    if 'rusak' in condition_raw:
                        condition = 'broken'
                    elif 'baik' in condition_raw:
                        condition = 'good'

                    asset_data = {
                        'asset_type': asset_type,
                        'name': name,
                        'maker': merk,
                        'owner': owner,
                        'location': location,
                        'status': 'available' if not owner else 'in_use', # Assume in_use if owner exists
                        'condition': condition,
                        'notes': str(row.get('Indikasi Awal', row.get('notes', ''))).strip(),
                    }

                    asset, created = Asset.objects.update_or_create(
                        serial_number=serial,
                        defaults=asset_data
                    )

                    # 3. Handle Specs
                    if type_code in ['laptop', 'pc']:
                        ComputerSpec.objects.update_or_create(
                            asset=asset,
                            defaults={
                                'ram': str(row.get('RAM', row.get('ram', ''))).strip(),
                                'storage': str(row.get('Penyimpanan', row.get('storage', ''))).strip(),
                                'processor': str(row.get('Processor', row.get('processor', ''))).strip(),
                                'os': str(row.get('os', '')).strip(), # Not in specific file, but keep for generic
                            }
                        )
                    elif type_code == 'printer':
                         PrinterSpec.objects.update_or_create(
                            asset=asset,
                            defaults={'is_color': False} # Default to False as not in sheet
                        )
                    elif type_code == 'scanner':
                        ScannerSpec.objects.update_or_create(
                            asset=asset,
                            defaults={'dpi': 0, 'connection_type': 'USB'} # Defaults
                        )

                    action = "Created" if created else "Updated"
                    # self.stdout.write(self.style.SUCCESS(f"{action}: {asset.name} ({serial})"))
                    success_count += 1

                except Exception as e:
                    self.stderr.write(self.style.ERROR(f"Error processing row {index}: {e}"))
                    error_count += 1

        self.stdout.write(self.style.SUCCESS(f"Seeding complete. Success: {success_count}, Errors: {error_count}"))
