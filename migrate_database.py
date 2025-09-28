import sqlite3
import os

def migrate_database():
    """Migrate the existing database to the new schema"""

    # Backup the existing database
    if os.path.exists("finance.db"):
        os.rename("finance.db", "finance_backup.db")
        print("📦 Backed up existing database to finance_backup.db")

    # Create new database with updated schema
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    # Create transactions table with new schema
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            amount REAL NOT NULL,
            description TEXT NOT NULL,
            category TEXT NOT NULL,
            month INTEGER NOT NULL,
            year INTEGER NOT NULL,
            date TEXT NOT NULL
        )
    """
    )

    # Create monthly budgets table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS monthly_budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            month INTEGER NOT NULL,
            year INTEGER NOT NULL,
            total_income REAL DEFAULT 0,
            ahorro_percentage REAL DEFAULT 0.10,
            deuda_percentage REAL DEFAULT 0.05,
            inversion_percentage REAL DEFAULT 0.10,
            UNIQUE(month, year)
        )
    """
    )

    conn.commit()
    conn.close()

    print("✅ Database migrated successfully!")
    print("🗃️  New schema created with month/year columns")

if __name__ == "__main__":
    migrate_database()