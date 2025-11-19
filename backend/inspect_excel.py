import pandas as pd

file_path = r'c:\Data\dev\aset\List Komputer_Laptop .xlsx'
try:
    df = pd.read_excel(file_path)
    print("All Columns:")
    print(df.columns.tolist())
    
    print("\nSample Data (First 3 rows):")
    cols_to_show = ['Jenis', 'Merk', 'Type', 'Posisi Barang Di Meja/Dibawa Oleh', 'Bidang', 'Kondisi']
    # Add serial number column if found
    for col in df.columns:
        if 'serial' in col.lower() or 'sn' in col.lower() or 's/n' in col.lower():
            cols_to_show.append(col)
            print(f"Found potential Serial Number column: {col}")
            
    print(df[cols_to_show].head(3).to_string())
except Exception as e:
    print(f"Error reading file: {e}")
