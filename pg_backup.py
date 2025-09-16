import os
import subprocess
import shutil
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import psycopg2 # You will need this library

# --- Prerequisites ---
# Make sure you have psycopg2 installed:
# pip install psycopg2-binary
# ---------------------


# --- Configuration & Paths ---
# Automatically find the path to the PostgreSQL tools
PG_DUMP_PATH = shutil.which("pg_dump")
PG_RESTORE_PATH = shutil.which("pg_restore")
PSQL_PATH = shutil.which("psql")

# Check that all required tools were found
for tool_path in [PG_DUMP_PATH, PG_RESTORE_PATH, PSQL_PATH]:
    if not tool_path:
        tool_name = os.path.basename(str(tool_path))
        print(f"Error: '{tool_name}' executable not found in your system's PATH.")
        print("Please ensure PostgreSQL client tools are installed and in your PATH.")
        exit(1)

print(f"Using pg_dump at: {PG_DUMP_PATH}")
print(f"Using pg_restore at: {PG_RESTORE_PATH}")
print(f"Using psql at: {PSQL_PATH}")


load_dotenv()

# --- Source Database (where the data comes from) ---
original_db = {
    "host": os.getenv("ORIG_HOST"),
    "port": int(os.getenv("ORIG_PORT")),
    "user": os.getenv("ORIG_USER"),
    "password": os.getenv("ORIG_PASS"),
    "name": os.getenv("ORIG_DB")
}

# --- Temporary Database (for restore and export) ---
# This can be a local, empty database. The script will clean it before restoring.
temp_db = {
    "host": os.getenv("BACKUP_HOST"),
    "port": int(os.getenv("BACKUP_PORT")),
    "user": os.getenv("BACKUP_USER"),
    "password": os.getenv("BACKUP_PASS"),
    "name": os.getenv("BACKUP_DB")
}

# --- Output Directories ---
dump_file = Path('/tmp') / f"{original_db['name']}_{datetime.now().strftime('%Y%m%d')}.backup"
csv_output_dir = Path('/tmp') / f"{original_db['name']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_csv"
csv_output_dir.mkdir(parents=True, exist_ok=True)

# --- 1. Perform the database dump ---
print("\nStep 1: Starting database dump...")
dump_cmd = [
    PG_DUMP_PATH, "-h", original_db["host"], "-p", str(original_db["port"]),
    "-U", original_db["user"], "-F", "c", "-b", "--exclude-schema=_heroku",
    "-f", str(dump_file), original_db["name"]
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

# --- 2. Restore the dump to the temporary database ---
print("\nStep 2: Restoring database to temporary location for export...")
restore_cmd = [
    PG_RESTORE_PATH, "-h", temp_db["host"], "-p", str(temp_db["port"]),
    "-U", temp_db["user"], "-d", temp_db["name"],
    "-c", "--if-exists", # Clean (drop) objects before recreating
    "--no-owner", "--no-privileges", "-v", str(dump_file)
]
env["PGPASSWORD"] = temp_db["password"]

try:
    subprocess.run(restore_cmd, check=True, env=env, capture_output=True, text=True)
    print(f"Database restored successfully to temporary DB '{temp_db['name']}'")
except subprocess.CalledProcessError as e:
    print("Error during pg_restore:")
    # We print stdout here because pg_restore -v prints progress to stdout
    print(e.stdout)
    print(e.stderr)
    exit(1)

# --- 3. Connect to temp DB and export each table to CSV ---
print("\nStep 3: Exporting tables to CSV files...")
try:
    conn = psycopg2.connect(
        dbname=temp_db["name"], user=temp_db["user"],
        password=temp_db["password"], host=temp_db["host"], port=temp_db["port"]
    )
    cur = conn.cursor()
    # Get all user tables (excluding system tables)
    cur.execute("""
        SELECT tablename FROM pg_catalog.pg_tables
        WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
    """)
    tables = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()

    if not tables:
        print("No user tables found in the restored database.")
        exit(0)

    print(f"Found {len(tables)} tables to export.")

    # Iterate and export each table
    for table_name in tables:
        csv_file_path = csv_output_dir / f"{table_name}.csv"
        print(f"  -> Exporting '{table_name}' to {csv_file_path}")

        # Use psql's \copy for efficient export with headers
        # The command is: \copy (SELECT * FROM "table_name") TO 'path' WITH (FORMAT CSV, HEADER)
        sql_command = f'\\copy (SELECT * FROM "{table_name}") TO \'{csv_file_path}\' WITH (FORMAT CSV, HEADER)'
        
        copy_cmd = [
            PSQL_PATH, "-h", temp_db["host"], "-p", str(temp_db["port"]),
            "-U", temp_db["user"], "-d", temp_db["name"], "-c", sql_command
        ]
        
        subprocess.run(copy_cmd, check=True, env=env, capture_output=True, text=True)

    print(f"\nSuccessfully exported {len(tables)} tables to '{csv_output_dir}'.")

except psycopg2.Error as e:
    print(f"Database connection or query error: {e}")
except subprocess.CalledProcessError as e:
    print(f"An error occurred during CSV export for table '{table_name}':")
    print(e.stderr)
except Exception as e:
    print(f"An unexpected error occurred: {e}")
