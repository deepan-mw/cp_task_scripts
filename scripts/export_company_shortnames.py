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
COLLECTION_NAME = "company"
DEFAULT_LIMIT = 250000  # Default number of documents to fetch
DEFAULT_BATCH_SIZE = 10000  # Default number of documents to fetch per batch

def connect_mongodb(uri, db_name):
    """Establish connection to MongoDB"""
    try:
        client = MongoClient(
            uri, 
            serverSelectionTimeoutMS=30000,
            connectTimeoutMS=30000,
            socketTimeoutMS=120000,
            tlsCAFile=certifi.where(),
            maxPoolSize=50,
            retryWrites=True
        )
        client.admin.command('ping')
        db = client[db_name]
        print(f"✓ Connected to {db_name}")
        return client, db
    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        print(f"✗ Error: Cannot connect to MongoDB - {e}")
        return None, None

def write_to_csv(data, filename):
    """Write results to CSV file"""
    if not data:
        print("No data to write to CSV")
        return
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write header
            writer.writerow(['company_id', 'short_name'])
            
            # Write data (only documents with valid short_name)
            for doc in data:
                company_id = str(doc.get('_id', ''))
                short_name = doc.get('short_name', '')
                
                # Skip if short_name is empty
                if short_name:
                    writer.writerow([company_id, short_name])
        
        print(f"✓ Data exported to {filename}")
        print(f"  Total records: {len(data)}")
        
    except Exception as e:
        print(f"✗ Error writing to CSV: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("MongoDB Company ID and Short Name Fetcher")
    print("=" * 60)
    
    # Get input parameters
    print("\nEnter parameters (press Enter to use defaults):")
    
    try:
        limit_input = input(f"Limit (default: {DEFAULT_LIMIT}): ").strip()
        LIMIT = int(limit_input) if limit_input else DEFAULT_LIMIT
        
        # batch_input = input(f"Batch Size (default: {DEFAULT_BATCH_SIZE}): ").strip()
        # BATCH_SIZE = int(batch_input) if batch_input else DEFAULT_BATCH_SIZE
        
        print(f"\nUsing LIMIT: {LIMIT}")
        # print(f"\nUsing LIMIT: {LIMIT}, BATCH_SIZE: {BATCH_SIZE}")
    except ValueError:
        print("\n✗ Invalid input. Using default values.")
        LIMIT = DEFAULT_LIMIT
        BATCH_SIZE = DEFAULT_BATCH_SIZE
    except KeyboardInterrupt:
        print("\n✗ Cancelled by user.")
        exit(1)
    
    # Connect to MongoDB
    print(f"\nStep 1: Connecting to MongoDB...")
    client, db = connect_mongodb(MONGODB_URI, DATABASE_NAME)
    if db is None:
        print("\n✗ Failed to connect to MongoDB. Exiting.")
        exit(1)
    
    try:
        collection = db[COLLECTION_NAME]
        
        # Execute query to get all _id and short_name pairs
        print(f"\nStep 2: Fetching documents from '{COLLECTION_NAME}' collection...")
        print(f"Getting all company IDs with their short_names (limit: {LIMIT})")
        # print(f"Getting all company IDs with their short_names (limit: {LIMIT}, batch size: {BATCH_SIZE})")
        
        start_time = time.time()
        
        # Simple find query to get all documents with _id and short_name
        cursor = collection.find(
            {
                "short_name": {"$exists": True, "$ne": "", "$ne": None}
            },
            {"_id": 1, "short_name": 1}
        ).limit(LIMIT)
        # ).batch_size(BATCH_SIZE).limit(LIMIT)
        
        results = list(cursor)
        elapsed_time = time.time() - start_time
        
        print(f"\n✓ Query completed in {elapsed_time:.2f} seconds")
        print(f"✓ Retrieved {len(results)} documents with short_names")
        
        if results:
            # Export to CSV
            print(f"\nStep 3: Writing results to CSV...")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"company_id_short_name_unique_{LIMIT}_{timestamp}.csv"
            write_to_csv(results, filename)
            
            print(f"\n{'=' * 60}")
            print("✓ SUCCESS!")
            print(f"{'=' * 60}")
        else:
            print("\n⚠️  No results found")
    
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        if client:
            client.close()
            print("\n✓ Connection closed")
