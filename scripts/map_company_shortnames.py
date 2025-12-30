#!/usr/bin/env python3

import csv
import time
import os
import glob
from datetime import datetime

# Configuration
INPUT_DIR = "/Users/deepan.muthusamy/Documents/CP_TASK/CSV_Reports/Input_CSV"
OUTPUT_DIR = "/Users/deepan.muthusamy/Documents/CP_TASK/CSV_Reports/Output_CSV"
MAPPING_FILE = "company_id_short_name_unique_25000000_20251230_005529.csv"  # File containing company_id to short_name mapping

def load_company_short_name_mapping(mapping_file):
    """Load company_id to short_name mapping from CSV file"""
    mapping = {}
    try:
        with open(mapping_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                company_id = row.get('company_id', '').strip()
                short_name = row.get('short_name', '').strip()
                if company_id:
                    mapping[company_id] = short_name
        print(f"✓ Loaded {len(mapping)} company_id to short_name mappings from {os.path.basename(mapping_file)}")
        return mapping
    except Exception as e:
        print(f"✗ Error reading mapping file: {e}")
        return {}

def read_company_ids_from_csv(csv_file):
    """Read company IDs from CSV file"""
    company_ids = []
    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                company_id = row.get('company_id', '').strip()
                if company_id:
                    company_ids.append(company_id)
        print(f"✓ Read {len(company_ids)} company IDs from {os.path.basename(csv_file)}")
        return company_ids
    except Exception as e:
        print(f"✗ Error reading CSV file: {e}")
        return []

def fetch_short_names_from_mapping(company_ids, mapping):
    """Fetch short names for company IDs from the mapping dictionary"""
    results = []
    for company_id in company_ids:
        short_name = mapping.get(company_id, '')
        results.append({
            "_id": company_id,
            "short_name": short_name
        })
    return results

def write_to_csv(data, filename):
    """Write results to CSV file"""
    if not data:
        print("No data to write to CSV")
        return
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write header
            writer.writerow(['_id', 'short_name'])
            
            # Write data
            for doc in data:
                writer.writerow([doc.get('_id', ''), doc.get('short_name', '')])
        
        print(f"✓ Data exported to {filename}")
        print(f"  Total records: {len(data)}")
        
    except Exception as e:
        print(f"✗ Error writing to CSV: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("Company ID and Short Name Mapper")
    print("=" * 60)
    
    # Check if input directory exists
    if not os.path.exists(INPUT_DIR):
        print(f"\n✗ Input directory not found: {INPUT_DIR}")
        exit(1)
    
    # Check if mapping file exists
    mapping_file_path = os.path.join(INPUT_DIR, MAPPING_FILE)
    if not os.path.exists(mapping_file_path):
        print(f"\n✗ Mapping file not found: {mapping_file_path}")
        exit(1)
    
    # Get all CSV files from input directory (excluding the mapping file)
    csv_files = [f for f in glob.glob(os.path.join(INPUT_DIR, "*.csv")) 
                 if os.path.basename(f) != MAPPING_FILE]
    
    if not csv_files:
        print(f"\n✗ No CSV files found in {INPUT_DIR} (excluding mapping file)")
        exit(1)
    
    print(f"\nFound {len(csv_files)} CSV file(s) in input directory:")
    for i, csv_file in enumerate(csv_files, 1):
        print(f"  {i}. {os.path.basename(csv_file)}")
    
    # Let user select which file to process
    print("\nSelect a file to process (enter number):")
    try:
        choice = int(input("> "))
        if choice < 1 or choice > len(csv_files):
            print("\n✗ Invalid selection")
            exit(1)
        selected_file = csv_files[choice - 1]
    except (ValueError, KeyboardInterrupt):
        print("\n✗ Invalid input or cancelled")
        exit(1)
    
    print(f"\nSelected: {os.path.basename(selected_file)}")
    
    # Create output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    try:
        # Load mapping from CSV
        print(f"\nStep 1: Loading company_id to short_name mapping...")
        start_time = time.time()
        mapping = load_company_short_name_mapping(mapping_file_path)
        
        if not mapping:
            print("\n✗ Failed to load mapping. Exiting.")
            exit(1)
        
        load_time = time.time() - start_time
        print(f"  Loaded in {load_time:.2f} seconds")
        
        # Read company IDs from CSV
        print(f"\nStep 2: Reading company IDs from selected CSV...")
        company_ids = read_company_ids_from_csv(selected_file)
        
        if not company_ids:
            print("\n⚠️  No company IDs found in CSV file")
            exit(1)
        
        # Fetch short names from mapping
        print(f"\nStep 3: Mapping company IDs to short names...")
        start_time = time.time()
        all_results = fetch_short_names_from_mapping(company_ids, mapping)
        elapsed_time = time.time() - start_time
        
        print(f"✓ Mapping completed in {elapsed_time:.2f} seconds")
        print(f"✓ Processed {len(all_results)} company IDs")
        
        if all_results:
            # Generate output filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            input_basename = os.path.splitext(os.path.basename(selected_file))[0]
            output_filename = os.path.join(OUTPUT_DIR, f"{input_basename}_output_{timestamp}.csv")
            
            # Export to CSV
            print(f"\nStep 4: Writing results to CSV...")
            write_to_csv(all_results, output_filename)
            
            # Count records with short_name
            records_with_short_name = sum(1 for r in all_results if r.get('short_name'))
            records_without_short_name = len(all_results) - records_with_short_name
            
            print(f"\nSummary:")
            print(f"  Records with short_name: {records_with_short_name}")
            print(f"  Records without short_name: {records_without_short_name}")
            print(f"  Output file: {output_filename}")
            
            print(f"\n{'=' * 60}")
            print("✓ SUCCESS!")
            print(f"{'=' * 60}")
        else:
            print("\n⚠️  No results found")
    
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
