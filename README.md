# Zenith Duplicate Case Folder Detector

A Python CLI tool built to solve a real workflow problem at a personal injury law firm. OneDrive occasionally generates untagged duplicate folders alongside the real tagged case folders (e.g. `Smith, John 3.14.24` appearing next to `Smith, John 3.14.24 (DROPPED)`), cluttering the client directory. This script detects those duplicates and exports the untagged copies to a CSV for manual review before deletion — preserving human oversight given the sensitivity of legal records.

## How It Works

1. Scans a specified directory for case folders
2. Normalizes each folder name by stripping trailing status tags using regex
3. Groups folders by their normalized name using a hash map
4. Writes only the untagged duplicates to a CSV grouped by ID — these are the OneDrive-generated copies flagged for review and deletion

## Usage

```bash
python find_dupes.py <path_to_cases_directory>
```

A `duplicates.csv` file will be generated in the current directory.

## Example

Given these folders:
Smith, John 3.14.24
Smith, John 3.14.24 (DROPPED)
Garcia, Maria 1.05.23
Garcia, Maria 1.05.23 (CLOSED)

Output CSV:
group_id,folder_name
0,Smith, John 3.14.24
1,Garcia, Maria 1.05.23


The tagged folders contain the real files. The untagged entries above are the OneDrive-generated duplicates flagged for deletion.

## Requirements

No external dependencies — runs on the Python standard library only.
Python 3.10+

## Notes

- Designed for Windows paths but works cross-platform
- Falls back gracefully if no directory argument is provided
- Built for ~2,000 client folders; reduces 2-3 days of manual review to a single automated scan