import os
import subprocess
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv


PG_DUMP_PATH = "/usr/pgsql-17/bin/pg_dump"  # <-- Use the full path here
PG_RESTORE_PATH = "/usr/pgsql-17/bin/pg_restore" # <-- And here

load_dotenv()


original_db = {
    "host": os.getenv("ORIG_HOST"),
    "port": int(os.getenv("ORIG_PORT")),
    "user": os.getenv("ORIG_USER"),
    "password": os.getenv("ORIG_PASS"),
    "name": os.getenv("ORIG_DB")
}


backup_db = {
    "host": os.getenv("BACKUP_HOST"),
    "port": int(os.getenv("BACKUP_PORT")),
    "user": os.getenv("BACKUP_USER"),
    "password": os.getenv("BACKUP_PASS"),
    "name": os.getenv("BACKUP_DB")
}


dump_file = Path('/tmp') / f"{original_db['name']}_{datetime.now().strftime('%Y%m%d')}.backup"

dump_cmd = [
    PG_DUMP_PATH,
    "-h", original_db["host"],
    "-p", str(original_db["port"]),
    "-U", original_db["user"],
    "-F", "c",
    "-b",
    "--exclude-schema=_heroku",  # <-- Add this line
    "-f", str(dump_file),
    original_db["name"]
]

env = os.environ.copy()
env["PGPASSWORD"] = original_db["password"]

subprocess.run(dump_cmd, check=True, env=env)
print(f"Database dumped to {dump_file}")


restore_cmd = [
    PG_RESTORE_PATH,
    "-h", backup_db["host"],
    "-p", str(backup_db["port"]),
    "-U", backup_db["user"],
    "-d", backup_db["name"],
    "-c",               # Keep clean, but add --if-exists
    "--if-exists",      # Suppresses "does not exist" errors during clean
    "--no-owner",       # Do not attempt to set original ownership
    "--no-privileges",  # Do not attempt to restore access privileges (ACLs)
    "-v",
    str(dump_file)
]
env["PGPASSWORD"] = backup_db["password"]

subprocess.run(restore_cmd, env=env)
print(f"Database restored to {backup_db['name']}")
