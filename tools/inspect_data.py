import pandas as pd
import os

def inspect_orbit(file_path):
    try:
        df = pd.read_excel(file_path)
        print("Columns:", df.columns.tolist())
        print("First 5 rows:")
        print(df.head())
        print("Shape:", df.shape)
    except Exception as e:
        print(f"Error reading excel: {e}")

def inspect_file_size(file_path):
    try:
        size = os.path.getsize(file_path)
        print(f"File: {os.path.basename(file_path)}, Size: {size} bytes")
    except Exception as e:
        print(f"Error checking size: {e}")

if __name__ == "__main__":
    import sys
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    
    inspect_orbit(os.path.join(data_dir, "input", "orbit.xlsx"))
    inspect_file_size(os.path.join(data_dir, "input", "Proj.dat"))
    inspect_file_size(os.path.join(data_dir, "reference", "OSEMReconed.dat"))
    inspect_file_size(os.path.join(data_dir, "reference", "Filtered.dat"))
