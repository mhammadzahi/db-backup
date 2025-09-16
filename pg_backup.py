#pip install pgdumplib

import os
import subprocess
import csv
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import pgdumplib

# --- Configuration & Paths ---
PG_DUMP_PATH = "/usr/pgsql-17/bin/pg_dump"  # /usr/bin/pg_dump

load_dotenv()

original_db = {
    "host": os.getenv("ORIG_HOST"),
    "port": int(os.getenv("ORIG_PORT")),
    "user": os.getenv("ORIG_USER"),
    "password": os.getenv("ORIG_PASS"),
    "name": os.getenv("ORIG_DB")
}

# --- Output Directories ---
dump_file = Path('/tmp') / f"{original_db['name']}_{datetime.now().strftime('%Y%m%d')}.backup"
csv_output_dir = Path('/tmp') / f"{original_db['name']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_csv"
csv_output_dir.mkdir(parents=True, exist_ok=True) # Create the directory for CSV files

# --- 1. Perform the database dump (same as before) ---
print("Starting database dump...")
dump_cmd = [
    PG_DUMP_PATH,
    "-h", original_db["host"],
    "-p", str(original_db["port"]),
    "-U", original_db["user"],
    "-F", "c",  # Custom format is required for pgdumplib
    "-b",
    "--exclude-schema=_heroku",
    "-f", str(dump_file),
    original_db["name"]
]

env = os.environ.copy()
env["PGPASSWORD"] = original_db["password"]

try:
    subprocess.run(dump_cmd, check=True, env=env, capture_output=True, text=True)
    print(f"Database dumped successfully to {dump_file}")
except subprocess.CalledProcessError as e:
    print("Error during pg_dump:")
    print(e.stderr)
    exit(1)


# --- 2. Generate CSV files from the dump file (no restore) ---
print("\nStarting CSV generation from dump file...")
try:
    # Load the entire dump file into memory.
    # Note: For very large dumps, this may consume significant memory.
    dump = pgdumplib.load(dump_file)
    print(f"Successfully loaded dump file. Found {len(dump.entries)} entries.")

    table_count = 0
    # Iterate through all entries in the dump file
    for entry in dump.entries:
        # We only care about entries that contain table data
        if entry.desc == 'TABLE DATA':
            table_name = f"{entry.namespace}.{entry.tag}"
            csv_file_path = csv_output_dir / f"{table_name}.csv"
            
            print(f"Exporting table '{table_name}' to '{csv_file_path}'...")

            with open(csv_file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Write the column names as the header
                writer.writerow(entry.columns)
                
                # Write the data rows
                for row in entry.data:
                    writer.writerow(row)
            table_count += 1

    if table_count > 0:
        print(f"\nSuccessfully exported {table_count} tables to CSV files in '{csv_output_dir}'.")
    else:
        print("\nNo table data found in the dump file to export.")

except Exception as e:
    print(f"An error occurred during CSV generation: {e}")
