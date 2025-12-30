#!/usr/bin/env python3

import csv
import time
import os
import glob
from datetime import datetime

# Configuration
INPUT_DIR = "/Users/deepan.muthusamy/Documents/CP_TASK/CSV_Reports/Output_CSV"
OUTPUT_DIR = "/Users/deepan.muthusamy/Documents/CP_TASK/CSV_Reports/Output_CSV"
BASE_URL = "https://www.owler.com/iaApp"

def read_company_data_from_csv(csv_file):
    """Read company IDs and short names from CSV file"""
    company_data = []
    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                company_id = row.get('_id', '').strip()
                short_name = row.get('short_name', '').strip()
                if company_id:  # Only require company_id, short_name can be empty
                    company_data.append({
                        '_id': company_id,
                        'short_name': short_name
                    })
        print(f"✓ Read {len(company_data)} records from {os.path.basename(csv_file)}")
        return company_data
    except Exception as e:
        print(f"✗ Error reading CSV file: {e}")
        return []

def generate_profile_url(company_id, short_name):
    """Generate Owler profile URL from company_id and short_name"""
    # Replace spaces with hyphens in short_name
    formatted_name = short_name.replace(' ', '-')
    # Generate URL
    url = f"{BASE_URL}/{company_id}/{formatted_name}-company-profile"
    return url

def generate_urls_from_data(company_data):
    """Generate profile URLs for all company data"""
    results = []
    for data in company_data:
        company_id = data.get('_id', '')
        short_name = data.get('short_name', '')
        if company_id:  # Only require company_id
            # Generate URL only if short_name exists
            url = generate_profile_url(company_id, short_name) if short_name else ''
            results.append({
                '_id': company_id,
                'short_name': short_name,
                'profile_url': url
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
            writer.writerow(['_id', 'short_name', 'profile_url'])
            
            # Write data
            for doc in data:
                writer.writerow([doc.get('_id', ''), doc.get('short_name', ''), doc.get('profile_url', '')])
        
        print(f"✓ Data exported to {filename}")
        print(f"  Total records: {len(data)}")
        
    except Exception as e:
        print(f"✗ Error writing to CSV: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("Company Profile URL Generator")
    print("=" * 60)
    
    # Check if input directory exists
    if not os.path.exists(INPUT_DIR):
        print(f"\n✗ Input directory not found: {INPUT_DIR}")
        exit(1)
    
    # Get all CSV files from Output_CSV directory
    csv_files = glob.glob(os.path.join(INPUT_DIR, "*_output_*.csv"))
    
    if not csv_files:
        print(f"\n✗ No output CSV files found in {INPUT_DIR}")
        print("Looking for files matching pattern: *_output_*.csv")
        exit(1)
    
    print(f"\nFound {len(csv_files)} CSV file(s) in output directory:")
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
        # Read company data from CSV
        print(f"\nStep 1: Reading company data from CSV...")
        company_data = read_company_data_from_csv(selected_file)
        
        if not company_data:
            print("\n✗ No company data found in CSV file")
            exit(1)
        
        # Generate profile URLs
        print(f"\nStep 2: Generating profile URLs...")
        start_time = time.time()
        all_results = generate_urls_from_data(company_data)
        elapsed_time = time.time() - start_time
        
        print(f"✓ URL generation completed in {elapsed_time:.2f} seconds")
        print(f"✓ Generated {len(all_results)} profile URLs")
        
        if all_results:
            # Generate output filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            input_basename = os.path.splitext(os.path.basename(selected_file))[0]
            output_filename = os.path.join(OUTPUT_DIR, f"{input_basename}_with_urls_{timestamp}.csv")
            
            # Export to CSV
            print(f"\nStep 3: Writing results to CSV...")
            write_to_csv(all_results, output_filename)
            
            print(f"\nSummary:")
            print(f"  Total records processed: {len(all_results)}")
            print(f"  Output file: {output_filename}")
            
            print(f"\n{'=' * 60}")
            print("✓ SUCCESS!")
            print(f"{'=' * 60}")
        else:
            print("\n⚠️  No results generated")
    
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
