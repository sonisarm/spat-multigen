# Title: Python code to create STRand format
# Author: Sonia Sarmiento
# Date: February 2025

# input: xlsx with one column per allele, and metadata (Ind, Pop, X, Y)
# output: xlsx with STRand formatting

import os
import pandas as pd

# Define paths
script_dir = os.path.dirname(os.path.abspath(__file__))  # Path of the script
raw_data_path = os.path.join(script_dir, "../Data/RawData/")  # Input files
output_path = os.path.join(script_dir, "../Data/STRand/")  # Output files
txt_file_path = os.path.join(script_dir, "../Data/RawData/STRand-input-files.txt")  # List of files

# Ensure output directory exists
os.makedirs(output_path, exist_ok=True)

# Function to process each Excel file
def process_excel(file_path, sheet_name, output_name, ploidy):
    try:
        # Read the specified sheet from the Excel file
        df_pop = pd.read_excel(file_path, sheet_name=sheet_name)
        
        # Copy the initial columns that do not change (keeping 'Ind' and 'Pop')
        df_new = df_pop.iloc[:, :2].copy()  # Keeping 'Ind' and 'Pop', excluding 'X' and 'Y'

        # Identify the loci columns (starting from the 5th column)
        loci_columns = df_pop.columns[4:]  # Excluding 'Ind', 'Pop', 'X', 'Y'

        # Process each group of 'ploidy' columns
        for i in range(0, len(loci_columns), ploidy):
            locus_name = loci_columns[i]  # Name of the locus (use the first column name in the group)
            
            # Select the relevant group of columns based on the ploidy
            locus_values = df_pop.iloc[:, i + 4: i + 4 + ploidy].astype("Int64")  # Ensure integers with no decimals
            
            # Define a function to format locus values
            def format_locus(row):
                values = row.dropna().astype(str)  # Convert non-null values to string
                values = values[values != "0"]  # Remove zeros
                if values.empty:
                    return "0"
                formatted = "/".join(values)
                return formatted if len(values) < 3 else formatted + "*"  # Append '*' if more than 2 alleles
        
            # Apply the formatting function to the locus values
            df_new[locus_name] = locus_values.apply(format_locus, axis=1)

        # Save the result to a CSV file with a semicolon separator
        csv_output = os.path.join(output_path, f"{output_name}.csv")
        df_new.to_csv(csv_output, sep=",", index=False)

        # Save the result to an Excel file
        excel_output = os.path.join(output_path, f"{output_name}.xlsx")
        df_new.to_excel(excel_output, index=False)

        # Return the paths of the generated files
        return csv_output, excel_output
        
    except Exception as e:
        print(f"Error processing {file_path} - {e}")
        return None, None


# Process the input txt file
def process_input_txt(txt_file_path):
    with open(txt_file_path, 'r') as file:
        lines = file.readlines()
    
    for line in lines:
        # Assuming the format in the txt file is: file_path, sheet_name, output_name, ploidy
        file_path, sheet_name, output_name, ploidy = line.strip().split(",")
        ploidy = int(ploidy)  # Convert ploidy to integer
        
        # Combine raw_data_path with the excel_name to get the full file path
        file_path = os.path.join(raw_data_path, file_path)
        
        if os.path.exists(file_path):
            csv_file, excel_file = process_excel(file_path, sheet_name, output_name, ploidy)
            if csv_file and excel_file:
                print(f"Processed: {csv_file}, {excel_file}")
            else:
                print(f"Failed to process {file_path}")
        else:
            print(f"File not found: {file_path}")


# Process input txt file
process_input_txt(txt_file_path)
