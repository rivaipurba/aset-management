import pandas as pd

file_path = r'c:\Data\dev\aset\List Komputer_Laptop .xlsx'
sheet_name = 'Printer & Scanner'

try:
    # Check available sheets first
    xl = pd.ExcelFile(file_path)
    print("Available sheets:", xl.sheet_names)
    
    if sheet_name in xl.sheet_names:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        print(f"\nColumns in '{sheet_name}':")
        print(df.columns.tolist())
        
        print("\nSample Data (First 3 rows):")
        print(df.head(3).to_string())
    else:
        print(f"Sheet '{sheet_name}' not found.")

except Exception as e:
    print(f"Error reading file: {e}")
