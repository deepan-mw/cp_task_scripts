# Script Usage Guide

## Common Scenarios

### Scenario 1: Export company IDs for a new task

```bash
python scripts/export_company_ids_by_task.py
# Enter: Task Type = NAMES
# Enter: Limit = 5000
# Output: NAMES_3176.csv (if 3176 records found)
```

### Scenario 2: Create a mapping file from database

```bash
python scripts/export_company_shortnames.py
# Enter: Limit = 100000
# Output: company_id_short_name_unique_100000_20251231_120000.csv
```

### Scenario 3: Enrich company IDs with short names

```bash
python scripts/map_company_shortnames.py
# Select file: 1. NAMES_3176.csv
# Output: NAMES_3176_output_20251231_120500.csv
```

### Scenario 4: Add profile URLs to data

```bash
python scripts/generate_owler_profile_urls.py
# Select file: 1. NAMES_3176_output_20251231_120500.csv
# Output: NAMES_3176_output_20251231_120500_with_urls_20251231_120600.csv
```

### Scenario 5: Bulk update task status

```bash
python scripts/update_task_status.py
# Enter: Task Type = NAMES
# Enter: Company ID = (leave empty for all)
# Enter: Limit = 1000
# Confirm: yes
# Updates 1000 records from OPEN to CLEAR_QUEUE
```

## Troubleshooting

### Connection Issues
- Verify MongoDB URI in `config.py`
- Check network connectivity
- Ensure SSL certificates are up to date: `pip install --upgrade certifi`

### Empty Results
- Verify collection names and filters
- Check if documents match the query criteria
- Review the filter query displayed by scripts

### CSV Import Issues
- Ensure CSV files are UTF-8 encoded
- Check column headers match expected format
- Verify file paths are correct

## Performance Tips

- Use appropriate limits for large datasets
- Enable batch processing for bulk operations
- Run read-only operations during off-peak hours
- Monitor execution time for optimization opportunities

## Best Practices

1. **Always backup data** before running update operations
2. **Test with small limits** before processing large datasets
3. **Review confirmation prompts** carefully for write operations
4. **Check output files** to verify results
5. **Keep mapping files updated** for accurate enrichment
