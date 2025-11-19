import pandas as pd

file_path = r'c:\Data\dev\aset\List Komputer_Laptop .xlsx'
sheet_name = 'Data Komputer'

try:
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    print(f"\nColumns in '{sheet_name}':")
    print(df.columns.tolist())
    
    print("\nSample Data (First 3 rows):")
    print(df.head(3).to_string())
    
    print("\nUnique 'Jenis' values:")
    print(df['Jenis'].unique())

except Exception as e:
    print(f"Error reading file: {e}")
