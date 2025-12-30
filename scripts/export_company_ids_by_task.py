#!/usr/bin/env python3

import csv
import ssl
import certifi
import time
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from bson import ObjectId

# Configuration
# Replace with your MongoDB connection string:
# MONGODB_URI = "mongodb+srv://<USERNAME>:<PASSWORD>@<HOST>/<DATABASE>?retryWrites=true&w=majority&authSource=admin"
MONGODB_URI = ""
DATABASE_NAME = "owler"
COLLECTION_NAME = "cp_task"
DEFAULT_LIMIT = 10000  # Default number of documents to fetch


def convert_to_serializable(obj):
    """Convert MongoDB objects to CSV-serializable format"""
    if isinstance(obj, ObjectId):
        return str(obj)
    elif isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, dict):
        return {k: convert_to_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_serializable(item) for item in obj]
    return obj

def write_to_csv(data, collection_name, task_type):
    """Write results to CSV file"""
    if not data:
        print("No data to write to CSV")
        return
    
    # Convert all objects to serializable format
    serializable_data = [convert_to_serializable(doc) for doc in data]
    
    # Generate filename with actual document count
    filename = f"{task_type}_{len(serializable_data)}.csv"
    
    try:
        # Get all unique keys from all documents
        all_keys = set()
        for doc in serializable_data:
            all_keys.update(doc.keys())
        
        fieldnames = sorted(all_keys)
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for doc in serializable_data:
                # Flatten nested objects for CSV
                flat_doc = {}
                for key, value in doc.items():
                    if isinstance(value, (dict, list)):
                        flat_doc[key] = str(value)
                    else:
                        flat_doc[key] = value
                writer.writerow(flat_doc)
        
        print(f"✓ Data exported to {filename}")
        print(f"  Total records: {len(serializable_data)}")
        print(f"  Fields: {len(fieldnames)}")
        
    except Exception as e:
        print(f"✗ Error writing to CSV: {e}")

def connect_mongodb(uri, db_name):
    """Establish connection to MongoDB"""
    try:
        # Use certifi for SSL certificate verification on macOS
        client = MongoClient(
            uri, 
            serverSelectionTimeoutMS=5000,
            tlsCAFile=certifi.where()
        )
        client.admin.command('ping')
        db = client[db_name]
        print(f"✓ Connected to {db_name}")
        return client, db
    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        print(f"✗ Error: Cannot connect to MongoDB - {e}")
        return None, None

if __name__ == "__main__":
    script_start_time = time.time()
    
    print("=" * 60)
    print("Export Company IDs by Task Type and Status")
    print("=" * 60)
    
    # Get input parameters
    print("\nEnter parameters:")
    
    try:
        # Mandatory task_type
        TASK_TYPE = input("Task Type (required): ").strip().upper()
        if not TASK_TYPE:
            print("\n✗ Task Type is required. Exiting.")
            exit(1)
        
        # Optional limit
        limit_input = input(f"Limit (press Enter for default: {DEFAULT_LIMIT}): ").strip()
        LIMIT = int(limit_input) if limit_input else DEFAULT_LIMIT
        
        print("\n" + "=" * 60)
        print("Configuration:")
        print(f"  Task Type: {TASK_TYPE}")
        print(f"  Limit: {LIMIT}")
        print(f"  Status Filter: OPEN")
        print("=" * 60)
        
    except ValueError:
        print("\n✗ Invalid input for limit. Must be a number.")
        exit(1)
    except KeyboardInterrupt:
        print("\n✗ Cancelled by user.")
        exit(1)
    
    # Connect to MongoDB
    client, db = connect_mongodb(MONGODB_URI, DATABASE_NAME)
    if db is None:
        exit(1)
    
    try:
        collection = db[COLLECTION_NAME]
        
        # Execute query
        filter_query = {
          "status": "OPEN",
          "task_type": TASK_TYPE
        }
        projection = {
          "company_id": 1,
          "_id": 0
        }
        sort_order = {}
        
        cursor = collection.find(filter_query, projection).limit(LIMIT)
        
        results = list(cursor)
        print(f"Found {len(results)} documents\n")
        
        # Export to CSV
        if results:
            write_to_csv(results, COLLECTION_NAME, TASK_TYPE)
        else:
            print("No results to export")
    
    except Exception as e:
        print(f"✗ Error: {e}")
    
    finally:
        if client:
            client.close()
            print("✓ Connection closed")
        
        # Display total execution time
        total_time = time.time() - script_start_time
        print(f"\n{'=' * 60}")
        print(f"Total execution time: {total_time:.2f} seconds")
        print(f"{'=' * 60}")
