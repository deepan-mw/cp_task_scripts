# cp_task_scripts

# MongoDB Data Processing Scripts

This repository contains Python scripts for processing MongoDB data, specifically for company information management and task status updates.

## Scripts Overview

### 1. export_company_ids_by_task.py
**Purpose**: Exports company IDs from the `cp_task` collection based on task type and status filters.

**Key Features**:
- Connects to MongoDB `owler` database
- Queries `cp_task` collection
- Filters by `status: "OPEN"` and `task_type` (configurable)
- Exports company_id list to CSV file
- Uses configurable LIMIT for result set size

**Output**: CSV file with format: `{TASK_TYPE}_{LIMIT}.csv` containing company IDs

**Use Case**: Extract company IDs for specific open tasks (e.g., DESCRIPTION, LINKS, CEO, etc.)

---

### 2. export_company_shortnames.py
**Purpose**: Fetches company _id and short_name directly from MongoDB `company` collection and exports to CSV.

**Key Features**:
- Connects to MongoDB `owler` database
- Queries `company` collection
- Filters out documents with empty/null short_name
- User input for LIMIT (optional, defaults to 250,000)
- Batch processing support with configurable batch size
- Exports to timestamped CSV file

**Output**: CSV file with format: `company_id_short_name_unique_{LIMIT}_{timestamp}.csv`

**Use Case**: Create a master mapping file of company IDs to short names from the database

---

### 3. map_company_shortnames.py
**Purpose**: Maps company IDs from input CSV files to their corresponding short_names using a pre-existing mapping file.

**Key Features**:
- Reads company IDs from CSV files in `Input_CSV` directory
- Uses mapping file: `company_id_short_name_90000_20251229_195508.csv`
- Performs fast in-memory dictionary lookups (no database queries)
- Interactive file selection from available input files
- Exports results to `Output_CSV` directory

**Input Directory**: `/Users/deepan.muthusamy/Documents/CP_TASK/CSV_Reports/Input_CSV`

**Output Directory**: `/Users/deepan.muthusamy/Documents/CP_TASK/CSV_Reports/Output_CSV`

**Output Format**: `{input_filename}_output_{timestamp}.csv` with columns: `_id`, `short_name`

**Use Case**: Enrich company ID lists with short names without hitting the database

---

### 4. generate_owler_profile_urls.py
**Purpose**: Generates Owler profile URLs from company data (company_id and short_name).

**Key Features**:
- Reads from Output_CSV directory (files matching `*_output_*.csv` pattern)
- Generates Owler profile URLs in format: `https://www.owler.com/iaApp/{id}/{short-name}-company-profile`
- Handles empty short_names (includes record with blank URL)
- Replaces spaces with hyphens in company names
- Interactive file selection

**Input Directory**: `/Users/deepan.muthusamy/Documents/CP_TASK/CSV_Reports/Output_CSV`

**Output Format**: `{input_filename}_with_urls_{timestamp}.csv` with columns: `_id`, `short_name`, `profile_url`

**Use Case**: Create clickable Owler profile URLs for company lists

---

### 5. update_task_status.py
**Purpose**: Updates the status field in `cp_task` collection from "OPEN" to "CLEAR_QUEUE".

**Key Features**:
- Bulk update operation with MongoDB `update_many()`
- Interactive input for filters:
  - **task_type** (required): Task type to update
  - **company_id** (optional): Update specific company only
  - **limit** (optional): Limit number of records to update
- Automatic data type detection for company_id (integer, ObjectId, or string)
- Pre-update count and confirmation prompt
- Shows filter query for debugging
- Reports matched and modified counts after update

**Safety Features**:
- Confirmation prompt before executing update
- Shows exact filter criteria before proceeding
- Displays count of documents to be updated
- Reports update results (matched vs modified)

**Use Case**: Change task status in bulk for queue management, optionally filtered by task type and/or company

---

## Workflow Example

### Typical Data Processing Flow:

1. **Export Company IDs by Task**
   ```bash
   python export_company_ids_by_task.py
   ```
   Exports company IDs for specific task type from cp_task collection

2. **Map to Short Names**
   ```bash
   python map_company_shortnames.py
   ```
   Select the exported file to enrich with short names

3. **Generate Profile URLs**
   ```bash
   python generate_owler_profile_urls.py
   ```
   Create Owler profile URLs for the enriched data

4. **Update Task Status** (when ready to clear processed tasks)
   ```bash
   python update_task_status.py
   ```
   Mark tasks as CLEAR_QUEUE after processing

---

## Configuration

### MongoDB Connection
All scripts use the same MongoDB Atlas connection:
- **URI**: `mongodb+srv://dqmetrics:...@owler.afztv.mongodb.net/owler`
- **Database**: `owler`
- **Collections**: `company`, `cp_task`
- **SSL/TLS**: Uses `certifi` for certificate verification

### Directory Structure
```
CP_TASK/
├── CSV_Reports/
│   ├── Input_CSV/          # Input files for processing
│   └── Output_CSV/         # Generated output files
├── export_company_ids_by_task.py
├── export_company_shortnames.py
├── map_company_shortnames.py
├── generate_owler_profile_urls.py
├── update_task_status.py
└── README.md
```

---

## Requirements

### Python Packages
```bash
pip install pymongo certifi
```

### Python Version
- Python 3.6+

---

## Notes

- All scripts include error handling and progress reporting
- CSV files use UTF-8 encoding
- Timestamped filenames prevent accidental overwrites
- Scripts are interactive and provide clear feedback
- Read-only scripts (export/map/generate) are safe to run multiple times
- Write script (update_task_status.py) requires confirmation before execution

---

## Author
Created for MongoDB data processing and company information management.

**Last Updated**: December 30, 2025
