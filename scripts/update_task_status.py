#!/usr/bin/env python3

import csv
import ssl
import certifi
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from bson import ObjectId

# Configuration
MONGODB_URI = "mongodb+srv://<USERNAME>:<PASSWORD>@<HOST>/<DATABASE>?retryWrites=true&w=majority&authSource=admin"
DATABASE_NAME = "owler"
COLLECTION_NAME = "cp_task"
NEW_STATUS = "CLEAR_QUEUE"  # Status to update to
OLD_STATUS = "OPEN"  # Status to update from


def connect_mongodb(uri, db_name):
    """Establish connection to MongoDB"""
    try:
        # Use certifi for SSL certificate verification on macOS
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

if __name__ == "__main__":
    print("=" * 60)
    print("MongoDB Status Update Script")
    print(f"Update status from '{OLD_STATUS}' to '{NEW_STATUS}'")
    print("=" * 60)
    
    # Get optional input parameters
    print("\nEnter parameters (press Enter to skip):")
    
    try:
        # Optional company_id filter
        company_id_input = input("Company ID (optional, leave empty for all): ").strip()
        company_id = company_id_input if company_id_input else None
        
        # Mandatory task_type filter
        task_type = input("Task Type (required): ").strip()
        if not task_type:
            print("\n✗ Task Type is required. Exiting.")
            exit(1)
        
        # Optional limit
        limit_input = input("Limit (optional, leave empty for no limit): ").strip()
        limit = int(limit_input) if limit_input else None
        
        print("\n" + "=" * 60)
        print("Configuration:")
        print(f"  Company ID filter: {company_id if company_id else 'None (all records)'}")
        print(f"  Task Type filter: {task_type}")
        print(f"  Limit: {limit if limit else 'None (no limit)'}")
        print(f"  Status change: {OLD_STATUS} -> {NEW_STATUS}")
        print("=" * 60)
        
        # Confirm before proceeding
        confirm = input("\nProceed with update? (yes/no): ").strip().lower()
        if confirm not in ['yes', 'y']:
            print("\n✗ Update cancelled by user.")
            exit(0)
            
    except ValueError:
        print("\n✗ Invalid input for limit. Must be a number.")
        exit(1)
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
        
        # Build filter query
        filter_query = {"status": OLD_STATUS, "task_type": task_type}
        
        # Add company_id filter if provided
        if company_id:
            try:
                # Try to convert to integer first (most common case)
                if company_id.isdigit():
                    filter_query["company_id"] = int(company_id)
                # Try ObjectId if it looks like one (24 character hex string)
                elif len(company_id) == 24:
                    filter_query["company_id"] = ObjectId(company_id)
                else:
                    # Use as string
                    filter_query["company_id"] = company_id
            except Exception:
                # If conversion fails, use as string
                filter_query["company_id"] = company_id
        
        print(f"\nFilter query: {filter_query}")
        
        # Count matching documents before update
        print(f"\nStep 2: Counting documents to update...")
        count_query = filter_query.copy()
        if limit:
            # For counting with limit, we need to find the IDs first
            matching_docs = list(collection.find(count_query, {"_id": 1}).limit(limit))
            total_to_update = len(matching_docs)
        else:
            total_to_update = collection.count_documents(count_query)
        
        print(f"✓ Found {total_to_update} document(s) matching criteria")
        
        if total_to_update == 0:
            print("\n⚠️  No documents found to update. Exiting.")
            exit(0)
        
        # Perform update
        print(f"\nStep 3: Updating status to '{NEW_STATUS}'...")
        update_operation = {"$set": {"status": NEW_STATUS}}
        
        if limit:
            # Update with limit requires updating specific _ids
            ids_to_update = [doc["_id"] for doc in matching_docs]
            filter_query = {"_id": {"$in": ids_to_update}}
            result = collection.update_many(filter_query, update_operation)
        else:
            # Update all matching documents
            result = collection.update_many(filter_query, update_operation)
        
        print(f"\n{'=' * 60}")
        print("Update Results:")
        print(f"  Matched: {result.matched_count}")
        print(f"  Modified: {result.modified_count}")
        print(f"{'=' * 60}")
        
        if result.modified_count > 0:
            print("\n✓ SUCCESS!")
        else:
            print("\n⚠️  No documents were modified (they may already have the target status)")
    
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        if client:
            client.close()
            print("\n✓ Connection closed")
