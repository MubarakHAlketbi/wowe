import pandas as pd
import os

def excel_to_multiple_csv(excel_file, output_folder):
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Read all sheets
    xlsx = pd.read_excel(excel_file, sheet_name=None)
    
    # Iterate through each sheet and save as CSV
    for sheet_name, df in xlsx.items():
        # Create a valid filename from the sheet name
        safe_sheet_name = "".join([c for c in sheet_name if c.isalnum() or c in (' ', '-', '_')]).rstrip()
        output_file = os.path.join(output_folder, f"{safe_sheet_name}.csv")
        
        # Save to CSV
        df.to_csv(output_file, index=False)
        print(f"Sheet '{sheet_name}' saved as {output_file}")

# Example usage with Windows paths
excel_file = r"C:\Users\Mubarak\Documents\Projects\wowe\file.xlsx"
output_folder = r"C:\Users\Mubarak\Documents\Projects\wowe\output_csvs"

excel_to_multiple_csv(excel_file, output_folder)