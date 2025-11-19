import pandas as pd

data = [
    {
        'type': 'laptop',
        'name': 'ThinkPad X1 Carbon',
        'serial_number': 'SN-LAPTOP-001',
        'maker': 'Lenovo',
        'owner': 'John Doe',
        'location': 'IT Dept',
        'status': 'available',
        'condition': 'good',
        'notes': 'Primary dev machine',
        'ram': '16GB',
        'storage': '512GB SSD',
        'processor': 'Intel i7',
        'os': 'Windows 11 Pro'
    },
    {
        'type': 'monitor',
        'name': 'Dell UltraSharp',
        'serial_number': 'SN-MONITOR-001',
        'maker': 'Dell',
        'owner': 'Jane Smith',
        'location': 'Design Dept',
        'status': 'in_use',
        'condition': 'good',
        'notes': 'Color accurate',
        'size_inch': 27.0
    },
    {
        'type': 'printer',
        'name': 'HP LaserJet Pro',
        'serial_number': 'SN-PRINTER-001',
        'maker': 'HP',
        'owner': 'Office Admin',
        'location': 'Reception',
        'status': 'maintenance',
        'condition': 'fair',
        'notes': 'Needs toner',
        'is_color': 'True'
    }
]

df = pd.DataFrame(data)
df.to_excel('assets_sample.xlsx', index=False)
print("Sample Excel file created: assets_sample.xlsx")
