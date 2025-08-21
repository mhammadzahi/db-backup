<div align="center">
  <!-- Note: You will need to add a logo.png file to a .github folder in your repository for this to work -->
  <img src="https://raw.githubusercontent.com/mhammadzahi/db-backup/main/.github/logo.png" alt="DB-Backup Logo" width="150"/>
  <h1>db-backup</h1>
  <p>
    <strong>An automated PostgreSQL database backup and restore tool designed for seamless multi-environment workflows.</strong>
  </p>
  <p>
    <a href="https://github.com/mhammadzahi/db-backup/blob/main/LICENSE"><img src="https://img.shields.io/github/license/mhammadzahi/db-backup?style=for-the-badge" alt="License"></a>
    <a href="https://github.com/mhammadzahi/db-backup/issues"><img src="https://img.shields.io/github/issues/mhammadzahi/db-backup?style=for-the-badge&color=orange" alt="Issues"></a>
    <a href="https://github.com/mhammadzahi/db-backup/stargazers"><img src="https://img.shields.io/github/stars/mhammadzahi/db-backup?style=for-the-badge&color=yellow" alt="Stars"></a>
    <a href="#"><img src="https://img.shields.io/badge/PostgreSQL-17+-blue?style=for-the-badge&logo=postgresql" alt="PostgreSQL Version"></a>
  </p>
</div>

---

## 🚀 Overview

`db-backup` is a robust Python-based solution engineered to automate **PostgreSQL database backups and restores** across multiple environments. This tool ensures reliable, scheduled, and secure management of your database, making it an essential utility for development, staging, and production workflows.

---

## ✨ Key Features

- **Automated Operations**: Effortlessly automate database dump and restore tasks.
- **Environment-Driven Configuration**: Easily configure database credentials and settings using environment variables.
- **Advanced Control**: Handle schema exclusions and fine-tune ownership and privileges adjustments during restoration.
- **Cronjob-Friendly**: Designed to work reliably in cronjobs and other automated pipelines.
- **Modern Compatibility**: Fully compatible with PostgreSQL 17 and newer versions.

---

## 🏁 Quick Start

Get up and running in minutes:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/mhammadzahi/db-backup.git
    cd db-backup
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure your environment:**
    Create a `.env` file and populate it with your database credentials (see [Configuration](#-configuration)).

4.  **Run the script:**
    ```bash
    python app.py
    ```

---

## ⚙️ Installation

### Prerequisites

- Python 3.8+
- PostgreSQL client tools (`pg_dump`, `pg_restore`) installed and accessible in your system's PATH.

### Steps

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/mhammadzahi/db-backup.git
    cd db-backup
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate   # For Linux/macOS
    venv\Scripts\activate      # For Windows
    ```

3.  **Install the required Python packages:**
    ```bash
    pip install -r requirements.txt
    ```

---

## 🔧 Configuration

The script is configured using environment variables. For local development, create a `.env` file in the project's root directory.

```env
# Source Database (the one you want to back up)
ORIG_HOST=your_original_db_host
ORIG_PORT=5432
ORIG_USER=your_user
ORIG_PASS=your_password
ORIG_DB=your_database

# Destination Database (where the backup will be restored)
BACKUP_HOST=your_backup_db_host
BACKUP_PORT=5432
BACKUP_USER=your_user
BACKUP_PASS=your_password
BACKUP_DB=your_backup_database