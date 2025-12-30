# MongoDB Data Processing Scripts

A collection of Python scripts for processing MongoDB data, specifically designed for company information management and task status updates.

## 📁 Project Structure

```
mongodb-data-processor/
├── scripts/                          # Main Python scripts
│   ├── export_company_ids_by_task.py    # Export company IDs by task type
│   ├── export_company_shortnames.py      # Export company short names from DB
│   ├── map_company_shortnames.py         # Map IDs to short names via CSV
│   ├── generate_owler_profile_urls.py    # Generate Owler profile URLs
│   └── update_task_status.py             # Update task status in bulk
├── CSV_Reports/                      # Data files (gitignored)
│   ├── Input_CSV/                       # Input CSV files
│   └── Output_CSV/                      # Generated output files
├── docs/                            # Additional documentation
├── config.example.py                # Configuration template
├── requirements.txt                 # Python dependencies
├── .gitignore                       # Git ignore rules
└── README.md                        # This file
```

## 🚀 Quick Start

### 1. Setup

```bash
# Clone the repository
git clone <repository-url>
cd mongodb-data-processor

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure MongoDB connection
cp config.example.py config.py
# Edit config.py with your MongoDB credentials
```

### 2. Create Required Directories

```bash
mkdir -p CSV_Reports/Input_CSV CSV_Reports/Output_CSV
```

### 3. Run Scripts

```bash
# Export company IDs by task type
python scripts/export_company_ids_by_task.py

# Export company short names
python scripts/export_company_shortnames.py

# Map company IDs to short names
python scripts/map_company_shortnames.py

# Generate profile URLs
python scripts/generate_owler_profile_urls.py

# Update task status
python scripts/update_task_status.py
```

## 📋 Scripts Overview

### 1. export_company_ids_by_task.py
Exports company IDs from `cp_task` collection filtered by task type and status.

**Inputs:**
- Task Type (required): e.g., NAMES, DESCRIPTION, LINKS
- Limit (optional): Default 10,000

**Output:** `{TASK_TYPE}_{COUNT}.csv`

---

### 2. export_company_shortnames.py
Fetches company _id and short_name directly from MongoDB.

**Inputs:**
- Limit (optional): Default 250,000

**Output:** `company_id_short_name_unique_{LIMIT}_{timestamp}.csv`

---

### 3. map_company_shortnames.py
Maps company IDs to short names using a CSV mapping file (no DB queries).

**Input:** CSV files from `Input_CSV` directory  
**Output:** `{filename}_output_{timestamp}.csv` in `Output_CSV`

---

### 4. generate_owler_profile_urls.py
Generates Owler profile URLs from company data.

**Input:** CSV files from `Output_CSV` (pattern: `*_output_*.csv`)  
**Output:** `{filename}_with_urls_{timestamp}.csv`

**URL Format:** `https://www.owler.com/iaApp/{id}/{short-name}-company-profile`

---

### 5. update_task_status.py
Updates task status from "OPEN" to "CLEAR_QUEUE" in bulk.

**Inputs:**
- Task Type (required)
- Company ID (optional): Update specific company
- Limit (optional): Limit records to update

**Features:** Pre-update confirmation, count display, update summary

---

## 🔧 Configuration

All scripts can be configured via `config.py` (copy from `config.example.py`):

```python
MONGODB_URI = "mongodb+srv://<USERNAME>:<PASSWORD>@<HOST>/<DATABASE>"
DATABASE_NAME = "owler"
COLLECTION_COMPANY = "company"
COLLECTION_CP_TASK = "cp_task"
```

**Important:** Never commit `config.py` to version control!

## 📊 Typical Workflow

1. **Export company IDs** for a specific task type
2. **Map to short names** using the mapping script
3. **Generate profile URLs** for the enriched data
4. **Update task status** after processing is complete

## 🔒 Security

- All credentials should be stored in `config.py` (gitignored)
- Never hardcode credentials in scripts
- Use environment variables for CI/CD environments
- Review `.gitignore` to ensure sensitive files are excluded

## 📦 Requirements

- Python 3.6+
- pymongo >= 4.0.0
- certifi >= 2021.10.8

## 🤝 Contributing

1. Keep scripts modular and well-documented
2. Follow PEP 8 style guidelines
3. Update README when adding new scripts
4. Test scripts before committing

## 📝 Notes

- All scripts include error handling and progress reporting
- CSV files use UTF-8 encoding
- Timestamped filenames prevent accidental overwrites
- Scripts are interactive with clear user prompts
- Read-only operations are safe to run multiple times
- Write operations require confirmation

## 📄 License

Internal use only - Company proprietary

---

**Last Updated:** December 31, 2025
