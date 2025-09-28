import sqlite3


def populate_database():
    """Populate the database with necessary items from HolaMundo.xlsx"""
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    # Clear existing data to start fresh
    cursor.execute("DELETE FROM transactions")
    cursor.execute("DELETE FROM monthly_budgets")

    # September  2025 data (from your Excel)
    september_data = [
        # Fixed Income
        ("income_fixed", 1000000, "Padres", "Padres", 9, 2025),
        ("income_fixed", 32761, "CDT intereses", "CDT intereses", 9, 2025),
        # Variable Income
        ("income_variable", 28000, "Retorno Pizza", "Proyectos", 9, 2025),
        ("income_variable", 200000, "Trabajos AI", "Trabajos AI", 9, 2025),
        ("income_variable", 60000, "Show de magia adelanto", "Show de magia", 9, 2025),
        ("income_variable", 60000, "Show de Magia", "Show de magia", 9, 2025),
        ("income_variable", 32300, "Sr.wok", "Proyectos", 9, 2025),
        # Necesarios Expenses
        ("expense_necesarios", 58570, "Adobe", "Adobe", 9, 2025),
        ("expense_necesarios", 40000, "Overleaf", "Overleaf", 9, 2025),
        ("expense_necesarios", 175000, "BodyTech", "BodyTech", 9, 2025),
        ("expense_necesarios", 21000, "YT Premium", "YT Premium", 9, 2025),
        ("expense_necesarios", 82000, "Claude", "Claude", 9, 2025),
        ("expense_necesarios", 72000, "Hostinger", "Hostinger", 9, 2025),
        # Innecesarios Expenses
        ("expense_innecesarios", 125000, "Platziconf", "Entretenimiento", 9, 2025),
        ("expense_innecesarios", 50000, "Pizza", "Pizza", 9, 2025),
        ("expense_innecesarios", 3900, "Café", "Café", 9, 2025),
        ("expense_innecesarios", 48000, "Desodorante", "Entretenimiento", 9, 2025),
        ("expense_innecesarios", 65000, "Pizza", "Pizza", 9, 2025),
        ("expense_innecesarios", 5900, "Chocolates", "Chocolates", 9, 2025),
        ("expense_innecesarios", 64600, "Sr.wok", "Sr.wok", 9, 2025),
        ("expense_innecesarios", 21900, "Café Quindio", "Café", 9, 2025),
        ("expense_innecesarios", 132000, "Bolos", "Bolos", 9, 2025),
        ("expense_innecesarios", 53000, "Camisa Fisica", "Entretenimiento", 9, 2025),
    ]

    # October  2025 data (from your Excel)
    october_data = [
        # Fixed Income
        ("income_fixed", 1000000, "Padres", "Padres", 10, 2025),
        ("income_fixed", 32761, "CDT intereses", "CDT intereses", 10, 2025),
        # Variable Income
        ("income_variable", 60000, "Trabajos varios", "Proyectos", 10, 2025),
        # Necesarios Expenses
        ("expense_necesarios", 58570, "Adobe", "Adobe", 10, 2025),
        ("expense_necesarios", 40000, "Overleaf", "Overleaf", 10, 2025),
        ("expense_necesarios", 175000, "BodyTech", "BodyTech", 10, 2025),
        ("expense_necesarios", 21000, "YT Premium", "YT Premium", 10, 2025),
        ("expense_necesarios", 82000, "Claude", "Claude", 10, 2025),
    ]

    # Insert September data
    for transaction_type, amount, description, category, month, year in september_data:
        date = f" 2025-{month:02d}-15 12:00:00"  # Use middle of month
        cursor.execute(
            """
            INSERT INTO transactions (type, amount, description, category, month, year, date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (transaction_type, amount, description, category, month, year, date),
        )

    # Insert October data
    for transaction_type, amount, description, category, month, year in october_data:
        date = f" 2025-{month:02d}-15 12:00:00"  # Use middle of month
        cursor.execute(
            """
            INSERT INTO transactions (type, amount, description, category, month, year, date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (transaction_type, amount, description, category, month, year, date),
        )

    # Create monthly budget entries
    cursor.execute(
        """
        INSERT OR REPLACE INTO monthly_budgets (month, year, total_income, ahorro_percentage, deuda_percentage, inversion_percentage)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (9, 2025, 1413061, 0.10, 0.05, 0.10),
    )

    cursor.execute(
        """
        INSERT OR REPLACE INTO monthly_budgets (month, year, total_income, ahorro_percentage, deuda_percentage, inversion_percentage)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (10, 2025, 1092761, 0.10, 0.05, 0.10),
    )

    conn.commit()
    conn.close()

    print("✅ Database populated successfully with Excel data!")
    print("📊 Added September and October  2025 transactions")
    print("💰 Total transactions added:", len(september_data) + len(october_data))


if __name__ == "__main__":
    populate_database()
