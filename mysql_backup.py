import os
import subprocess
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Original database (source)
original_db = {
    "host": os.getenv("ORIG_HOST_"),
    "port": int(os.getenv("ORIG_PORT_")),
    "user": os.getenv("ORIG_USER_"),
    "password": os.getenv("ORIG_PASS_"),
    "name": os.getenv("ORIG_DB_")
}

# Backup database (destination)
backup_db = {
    "host": os.getenv("BACKUP_HOST_"),
    "port": int(os.getenv("BACKUP_PORT_")),
    "user": os.getenv("BACKUP_USER_"),
    "password": os.getenv("BACKUP_PASS_"),
    "name": os.getenv("BACKUP_DB_")
}

# Dump file path
dump_file = Path('/tmp') / f"{original_db['name']}_{datetime.now().strftime('%Y%m%d')}.sql"

# --- Dump the original database ---
dump_cmd = [
    "mysqldump",
    "-h", original_db["host"],
    "-P", str(original_db["port"]),
    "-u", original_db["user"],
    f"-p{original_db['password']}",  # password inline
    "--routines",                    # include stored procedures/functions
    "--events",                      # include events
    "--single-transaction",          # consistent dump
    original_db["name"]
]

with open(dump_file, "w") as f:
    subprocess.run(dump_cmd, check=True, stdout=f)

print(f"Database dumped to {dump_file}")

# --- Restore to backup database ---
restore_cmd = [
    "mysql",
    "-h", backup_db["host"],
    "-P", str(backup_db["port"]),
    "-u", backup_db["user"],
    f"-p{backup_db['password']}",
    backup_db["name"]
]

with open(dump_file, "r") as f:
    subprocess.run(restore_cmd, stdin=f, check=True)

print(f"Database restored to {backup_db['name']}")
