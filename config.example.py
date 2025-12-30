"""
Configuration template for MongoDB Data Processing Scripts

Copy this file to config.py and fill in your actual values.
DO NOT commit config.py to version control.
"""

# MongoDB Configuration
MONGODB_URI = "mongodb+srv://<USERNAME>:<PASSWORD>@<HOST>/<DATABASE>?retryWrites=true&w=majority&authSource=admin"
DATABASE_NAME = "owler"

# Collection Names
COLLECTION_COMPANY = "company"
COLLECTION_CP_TASK = "cp_task"

# Directory Paths (relative to project root)
INPUT_CSV_DIR = "CSV_Reports/Input_CSV"
OUTPUT_CSV_DIR = "CSV_Reports/Output_CSV"

# Default Settings
DEFAULT_EXPORT_LIMIT = 10000
DEFAULT_SHORTNAME_LIMIT = 250000
DEFAULT_BATCH_SIZE = 10000

# Status Values
STATUS_OPEN = "OPEN"
STATUS_CLEAR_QUEUE = "CLEAR_QUEUE"

# Mapping File (update with your actual mapping file)
MAPPING_FILE = "company_id_short_name_90000_20251229_195508.csv"
