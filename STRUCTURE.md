# MongoDB Data Processor - Project Structure

```
mongodb-data-processor/
│
├── scripts/                                    # Core Python scripts
│   ├── export_company_ids_by_task.py          # Export company IDs by task type
│   ├── export_company_shortnames.py            # Export short names from MongoDB
│   ├── map_company_shortnames.py               # Map IDs to short names (CSV-based)
│   ├── generate_owler_profile_urls.py          # Generate Owler profile URLs
│   └── update_task_status.py                   # Bulk update task status
│
├── CSV_Reports/                                # Data files (gitignored)
│   ├── Input_CSV/                             # Input CSV files
│   └── Output_CSV/                            # Generated output files
│
├── docs/                                       # Documentation
│   └── USAGE.md                               # Detailed usage guide
│
├── config.example.py                          # Configuration template
├── config.py                                  # Actual config (gitignored, create from example)
├── requirements.txt                           # Python dependencies
├── .gitignore                                 # Git ignore rules
├── README.md                                  # Script documentation
└── PROJECT_README.md                          # Main project documentation
```

## File Descriptions

### Scripts Directory (`scripts/`)
All executable Python scripts for MongoDB data processing.

### CSV_Reports Directory
- **Input_CSV/**: Place input CSV files here for processing
- **Output_CSV/**: Generated output files are saved here

### Configuration Files
- **config.example.py**: Template with placeholders - safe to commit
- **config.py**: Actual credentials - must NOT be committed (in .gitignore)

### Documentation
- **PROJECT_README.md**: Main project overview and setup guide
- **README.md**: Detailed script documentation
- **docs/USAGE.md**: Usage examples and troubleshooting

### Dependencies
- **requirements.txt**: Python package dependencies
- **.gitignore**: Excludes sensitive files, data files, and Python artifacts

## Setup Steps

1. **Clone and configure:**
   ```bash
   git clone <repo-url>
   cd mongodb-data-processor
   cp config.example.py config.py
   # Edit config.py with your credentials
   ```

2. **Install dependencies:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Create data directories:**
   ```bash
   mkdir -p CSV_Reports/Input_CSV CSV_Reports/Output_CSV
   ```

4. **Run scripts:**
   ```bash
   python scripts/export_company_ids_by_task.py
   ```

## Security Notes

- `config.py` contains credentials - never commit it!
- `.gitignore` protects sensitive files
- Use environment variables in production
- Review committed files before pushing

## Maintenance

- Keep scripts in `scripts/` directory
- Document new scripts in README.md
- Update requirements.txt when adding dependencies
- Test scripts before committing changes
