import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime


class FinanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Coiner - Gestor Financiero Personal")
        self.root.geometry("1400x900")
        self.root.configure(bg="#2c2c2c")

        # Initialize current month and year
        now = datetime.now()
        self.current_month = now.month
        self.current_year = now.year

        # Initialize database
        self.init_database()

        # Create main interface
        self.create_widgets()
        self.load_data()

    def init_database(self):
        """Initialize SQLite database with new schema"""
        self.conn = sqlite3.connect("finance.db")
        self.cursor = self.conn.cursor()

        # Create transactions table with new schema
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL,  -- 'income_fixed', 'income_variable', 'expense_indispensable', 'expense_necesarios', 'expense_innecesarios'
                amount REAL NOT NULL,
                description TEXT NOT NULL,
                category TEXT NOT NULL,
                month INTEGER NOT NULL,
                year INTEGER NOT NULL,
                date TEXT NOT NULL
            )
        """
        )

        # Create monthly budgets table for automatic calculations
        self.cursor.execute(
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

        self.conn.commit()

    def create_widgets(self):
        """Create the main UI components"""
        # Title and month navigation
        self.create_header()

        # Main content frame
        main_frame = tk.Frame(self.root, bg="#2c2c2c")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Income section (left side)
        self.create_income_section(main_frame)

        # Automatic allocations section (below income)
        self.create_allocations_section()

        # Outcome section (right side)
        self.create_outcome_section(main_frame)

        # Summary frame at bottom
        self.create_summary_section()

    def create_header(self):
        """Create title and month navigation"""
        header_frame = tk.Frame(self.root, bg="#2c2c2c", height=120)
        header_frame.pack(fill="x", pady=(20, 10))
        header_frame.pack_propagate(False)

        # Title
        title_label = tk.Label(
            header_frame,
            text="Coiner",
            font=("Poppins", 32, "normal"),
            fg="#f8f9fa",
            bg="#2c2c2c",
        )
        title_label.pack(pady=(15, 8))

        # Month navigation
        nav_frame = tk.Frame(header_frame, bg="#2c2c2c")
        nav_frame.pack(pady=10)

        prev_btn = tk.Button(
            nav_frame,
            text="‹",
            command=self.prev_month,
            bg="#2c2c2c",
            fg="#9ca3af",
            font=("Poppins", 20),
            cursor="hand2",
            bd=0,
            highlightthickness=0,
            activebackground="#374151",
            activeforeground="#f3f4f6",
            relief="flat",
        )
        prev_btn.pack(side="left", padx=15)

        self.month_label = tk.Label(
            nav_frame,
            text=self.get_month_year_text(),
            font=("Poppins", 18, "bold"),
            fg="#f3f4f6",
            bg="#2c2c2c",
        )
        self.month_label.pack(side="left", padx=25)

        next_btn = tk.Button(
            nav_frame,
            text="›",
            command=self.next_month,
            bg="#2c2c2c",
            fg="#9ca3af",
            font=("Poppins", 20),
            cursor="hand2",
            bd=0,
            highlightthickness=0,
            activebackground="#374151",
            activeforeground="#f3f4f6",
            relief="flat",
        )
        next_btn.pack(side="left", padx=15)

    def create_income_section(self, parent):
        """Create the income section with categories"""
        income_frame = tk.Frame(parent, bg="#2c2c2c")
        income_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # Income header
        income_header = tk.Label(
            income_frame,
            text="INGRESOS",
            font=("Poppins", 18, "bold"),
            fg="white",
            bg="#2c2c2c",
        )
        income_header.pack(pady=(15, 10))

        # Create notebook for income categories
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background='#2c2c2c', borderwidth=0)
        style.configure('TNotebook.Tab', background='#404040', foreground='white',
                       padding=[20, 8], borderwidth=0, focuscolor='none')
        style.map('TNotebook.Tab', background=[('selected', '#505050')])

        income_notebook = ttk.Notebook(income_frame)
        income_notebook.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        # Fixed Income Tab
        fixed_frame = tk.Frame(income_notebook, bg="#3a3a3a")
        income_notebook.add(fixed_frame, text="FIJOS")
        self.create_income_form(fixed_frame, "income_fixed")

        # Variable Income Tab
        variable_frame = tk.Frame(income_notebook, bg="#3a3a3a")
        income_notebook.add(variable_frame, text="VARIABLES")
        self.create_income_form(variable_frame, "income_variable")

    def create_income_form(self, parent, income_type):
        """Create income form for specific type"""
        # Form frame
        form_frame = tk.Frame(parent, bg="#3a3a3a")
        form_frame.pack(pady=15, padx=20, fill="x")

        tk.Label(
            form_frame,
            text="Valor:",
            fg="white",
            bg="#3a3a3a",
            font=("Poppins", 10, "bold"),
        ).pack(anchor="w")
        amount_entry = tk.Entry(
            form_frame,
            font=("Poppins", 11),
            bg="white",
            fg="#2c2c2c",
            relief="flat",
            bd=1
        )
        amount_entry.pack(fill="x", pady=(5, 12))

        tk.Label(
            form_frame,
            text="Descripción:",
            fg="white",
            bg="#3a3a3a",
            font=("Poppins", 10, "bold"),
        ).pack(anchor="w")
        desc_entry = tk.Entry(
            form_frame,
            font=("Poppins", 11),
            bg="white",
            fg="#2c2c2c",
            relief="flat",
            bd=1
        )
        desc_entry.pack(fill="x", pady=(5, 12))

        # Category based on type (from HolaMundo.xlsx)
        categories = {
            "income_fixed": [
                "Padres",
                "CDT intereses",
                "Salario",
                "Pensión",
                "Arriendo recibido",
                "Otro",
            ],
            "income_variable": [
                "Freelance",
                "Trabajos AI",
                "Show de magia",
                "Proyectos",
                "Retorno Pizza",
                "Consultoría",
                "Otro",
            ],
        }

        tk.Label(
            form_frame,
            text="Categoría:",
            fg="white",
            bg="#3a3a3a",
            font=("Poppins", 10, "bold"),
        ).pack(anchor="w")
        category_combo = ttk.Combobox(
            form_frame,
            values=categories[income_type],
            font=("Poppins", 11),
        )
        category_combo.pack(fill="x", pady=(5, 15))

        add_btn = tk.Button(
            form_frame,
            text="Agregar",
            command=lambda: self.add_transaction(
                income_type, amount_entry, desc_entry, category_combo
            ),
            bg="#4CAF50",
            fg="white",
            font=("Poppins", 11, "bold"),
            cursor="hand2",
            relief="flat",
            bd=0,
            padx=20,
            pady=8
        )
        add_btn.pack(pady=12)

        # List frame
        list_frame = tk.Frame(parent, bg="#3a3a3a")
        list_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Scrollable listbox
        listbox_frame = tk.Frame(list_frame, bg="#3a3a3a")
        listbox_frame.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(listbox_frame, bg="#4a4a4a", troughcolor="#3a3a3a")
        scrollbar.pack(side="right", fill="y")

        listbox = tk.Listbox(
            listbox_frame,
            yscrollcommand=scrollbar.set,
            font=("Poppins", 9),
            bg="#4a4a4a",
            fg="white",
            relief="flat",
            bd=0,
            selectbackground="#5a5a5a",
            selectforeground="white"
        )
        listbox.pack(fill="both", expand=True, padx=(0, 2))
        scrollbar.config(command=listbox.yview)

        # Store references
        if income_type == "income_fixed":
            self.fixed_listbox = listbox
        else:
            self.variable_listbox = listbox

        # Bind selection event to update allocations
        listbox.bind('<<ListboxSelect>>', lambda event: self.on_income_select(event, income_type))

        # Delete button
        delete_btn = tk.Button(
            list_frame,
            text="Eliminar Seleccionado",
            command=lambda: self.delete_transaction(income_type),
            bg="#f44336",
            fg="white",
            font=("Poppins", 9, "bold"),
            relief="flat",
            bd=0,
            padx=15,
            pady=5,
            cursor="hand2"
        )
        delete_btn.pack(pady=8)

    def create_allocations_section(self):
        """Create allocations section below income area"""
        allocations_frame = tk.Frame(self.root, bg="#3a3a3a", height=100)
        allocations_frame.pack(fill="x", padx=20, pady=(10, 0))
        allocations_frame.pack_propagate(False)

        # Title
        title_label = tk.Label(
            allocations_frame,
            text="Asignaciones Automáticas (Selecciona un ingreso)",
            font=("Poppins", 12, "bold"),
            fg="white",
            bg="#3a3a3a",
        )
        title_label.pack(pady=(10, 5))

        # Allocations row
        allocations_row = tk.Frame(allocations_frame, bg="#3a3a3a")
        allocations_row.pack(fill="x", pady=(0, 10))

        # Savings allocation
        self.selected_ahorro_label = tk.Label(
            allocations_row,
            text="Ahorro (10%): $0",
            font=("Poppins", 11, "bold"),
            fg="#81C784",
            bg="#3a3a3a",
        )
        self.selected_ahorro_label.pack(side="left", padx=20)

        # Debt payment allocation
        self.selected_deuda_label = tk.Label(
            allocations_row,
            text="Pago Deuda (5%): $0",
            font=("Poppins", 11, "bold"),
            fg="#FFB74D",
            bg="#3a3a3a",
        )
        self.selected_deuda_label.pack(side="left", padx=20)

        # Investment allocation
        self.selected_inversion_label = tk.Label(
            allocations_row,
            text="Inversión (10%): $0",
            font=("Poppins", 11, "bold"),
            fg="#64B5F6",
            bg="#3a3a3a",
        )
        self.selected_inversion_label.pack(side="left", padx=20)

    def on_income_select(self, event, income_type):
        """Handle income item selection to update allocations"""
        listbox = event.widget
        selection = listbox.curselection()

        if selection:
            # Get selected item text
            selected_text = listbox.get(selection[0])

            # Extract amount from the text (format: "Description - Category: $Amount")
            try:
                amount_str = selected_text.split(": $")[1].replace(",", "")
                amount = float(amount_str)

                # Calculate allocations for this specific income
                ahorro = amount * 0.10
                deuda = amount * 0.05
                inversion = amount * 0.10

                # Update allocation labels
                self.selected_ahorro_label.config(text=f"Ahorro (10%): ${ahorro:,.0f}")
                self.selected_deuda_label.config(text=f"Pago Deuda (5%): ${deuda:,.0f}")
                self.selected_inversion_label.config(text=f"Inversión (10%): ${inversion:,.0f}")

            except (IndexError, ValueError):
                # Reset if can't parse amount
                self.selected_ahorro_label.config(text="Ahorro (10%): $0")
                self.selected_deuda_label.config(text="Pago Deuda (5%): $0")
                self.selected_inversion_label.config(text="Inversión (10%): $0")
        else:
            # Reset when no selection
            self.selected_ahorro_label.config(text="Ahorro (10%): $0")
            self.selected_deuda_label.config(text="Pago Deuda (5%): $0")
            self.selected_inversion_label.config(text="Inversión (10%): $0")

    def create_outcome_section(self, parent):
        """Create the expense section with categories"""
        outcome_frame = tk.Frame(parent, bg="#2c2c2c")
        outcome_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))

        # Expense header
        outcome_header = tk.Label(
            outcome_frame,
            text="EGRESOS",
            font=("Poppins", 18, "bold"),
            fg="white",
            bg="#2c2c2c",
        )
        outcome_header.pack(pady=(15, 10))

        # Create notebook for expense categories
        expense_notebook = ttk.Notebook(outcome_frame)
        expense_notebook.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        # Indispensable Tab
        indispensable_frame = tk.Frame(expense_notebook, bg="#3a3a3a")
        expense_notebook.add(indispensable_frame, text="INDISPENSABLES")
        self.create_expense_form(indispensable_frame, "expense_indispensable")

        # Necesarios Tab
        necesarios_frame = tk.Frame(expense_notebook, bg="#3a3a3a")
        expense_notebook.add(necesarios_frame, text="NECESARIOS")
        self.create_expense_form(necesarios_frame, "expense_necesarios")

        # Innecesarios Tab
        innecesarios_frame = tk.Frame(expense_notebook, bg="#3a3a3a")
        expense_notebook.add(innecesarios_frame, text="INNECESARIOS")
        self.create_expense_form(innecesarios_frame, "expense_innecesarios")

    def create_expense_form(self, parent, expense_type):
        """Create expense form for specific type"""
        # Form frame
        form_frame = tk.Frame(parent, bg="#3a3a3a")
        form_frame.pack(pady=15, padx=20, fill="x")

        tk.Label(
            form_frame,
            text="Valor:",
            fg="white",
            bg="#3a3a3a",
            font=("Poppins", 10, "bold"),
        ).pack(anchor="w")
        amount_entry = tk.Entry(
            form_frame,
            font=("Poppins", 11),
            bg="white",
            fg="#2c2c2c",
            relief="flat",
            bd=1
        )
        amount_entry.pack(fill="x", pady=(5, 12))

        tk.Label(
            form_frame,
            text="Descripción:",
            fg="white",
            bg="#3a3a3a",
            font=("Poppins", 10, "bold"),
        ).pack(anchor="w")
        desc_entry = tk.Entry(
            form_frame,
            font=("Poppins", 11),
            bg="white",
            fg="#2c2c2c",
            relief="flat",
            bd=1
        )
        desc_entry.pack(fill="x", pady=(5, 12))

        # Categories based on type (from HolaMundo.xlsx)
        categories = {
            "expense_indispensable": [
                "Arriendo",
                "Servicios públicos",
                "Alimentación básica",
                "Transporte público",
                "Seguro médico",
                "Medicamentos",
                "Otro",
            ],
            "expense_necesarios": [
                "Adobe",
                "Overleaf",
                "BodyTech",
                "YT Premium",
                "Claude",
                "Hostinger",
                "Netflix",
                "Spotify",
                "Internet",
                "Teléfono",
                "Otro",
            ],
            "expense_innecesarios": [
                "Pizza",
                "Café",
                "Chocolates",
                "Sr.wok",
                "Bolos",
                "Entretenimiento",
                "Platziconf",
                "Desodorante",
                "Café Quindio",
                "Camisa Fisica",
                "Otro",
            ],
        }

        tk.Label(
            form_frame,
            text="Categoría:",
            fg="white",
            bg="#3a3a3a",
            font=("Poppins", 10, "bold"),
        ).pack(anchor="w")
        category_combo = ttk.Combobox(
            form_frame,
            values=categories[expense_type],
            font=("Poppins", 11),
        )
        category_combo.pack(fill="x", pady=(5, 15))

        add_btn = tk.Button(
            form_frame,
            text="Agregar",
            command=lambda: self.add_transaction(
                expense_type, amount_entry, desc_entry, category_combo
            ),
            bg="#FF5722",
            fg="white",
            font=("Poppins", 11, "bold"),
            cursor="hand2",
            relief="flat",
            bd=0,
            padx=20,
            pady=8
        )
        add_btn.pack(pady=12)

        # List frame
        list_frame = tk.Frame(parent, bg="#3a3a3a")
        list_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Scrollable listbox
        listbox_frame = tk.Frame(list_frame, bg="#3a3a3a")
        listbox_frame.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(listbox_frame, bg="#4a4a4a", troughcolor="#3a3a3a")
        scrollbar.pack(side="right", fill="y")

        listbox = tk.Listbox(
            listbox_frame,
            yscrollcommand=scrollbar.set,
            font=("Poppins", 9),
            bg="#4a4a4a",
            fg="white",
            relief="flat",
            bd=0,
            selectbackground="#5a5a5a",
            selectforeground="white"
        )
        listbox.pack(fill="both", expand=True, padx=(0, 2))
        scrollbar.config(command=listbox.yview)

        # Store references
        if expense_type == "expense_indispensable":
            self.indispensable_listbox = listbox
        elif expense_type == "expense_necesarios":
            self.necesarios_listbox = listbox
        else:
            self.innecesarios_listbox = listbox

        # Delete button
        delete_btn = tk.Button(
            list_frame,
            text="Eliminar Seleccionado",
            command=lambda: self.delete_transaction(expense_type),
            bg="#f44336",
            fg="white",
            font=("Poppins", 9, "bold"),
            relief="flat",
            bd=0,
            padx=15,
            pady=5,
            cursor="hand2"
        )
        delete_btn.pack(pady=8)

    def create_summary_section(self):
        """Create comprehensive summary section"""
        summary_frame = tk.Frame(self.root, bg="#333333", height=140)
        summary_frame.pack(fill="x", side="bottom", padx=20, pady=(0, 20))
        summary_frame.pack_propagate(False)

        # Top row - Income totals
        top_frame = tk.Frame(summary_frame, bg="#333333")
        top_frame.pack(fill="x", pady=(10, 5))

        self.income_fixed_label = tk.Label(
            top_frame,
            text="Ingresos Fijos: $0",
            font=("Poppins", 11, "bold"),
            fg="#4CAF50",
            bg="#333333",
        )
        self.income_fixed_label.pack(side="left", padx=15)

        self.income_variable_label = tk.Label(
            top_frame,
            text="Ingresos Variables: $0",
            font=("Poppins", 11, "bold"),
            fg="#4CAF50",
            bg="#333333",
        )
        self.income_variable_label.pack(side="left", padx=15)

        self.total_income_label = tk.Label(
            top_frame,
            text="Total Ingresos (A): $0",
            font=("Poppins", 12, "bold"),
            fg="#66BB6A",
            bg="#333333",
        )
        self.total_income_label.pack(side="right", padx=15)

        # Middle row - Expenses
        middle_frame = tk.Frame(summary_frame, bg="#333333")
        middle_frame.pack(fill="x", pady=2)

        self.indispensable_label = tk.Label(
            middle_frame,
            text="Indispensables: $0",
            font=("Poppins", 10),
            fg="#FF7043",
            bg="#333333",
        )
        self.indispensable_label.pack(side="left", padx=15)

        self.necesarios_label = tk.Label(
            middle_frame,
            text="Necesarios: $0",
            font=("Poppins", 10),
            fg="#FF7043",
            bg="#333333",
        )
        self.necesarios_label.pack(side="left", padx=15)

        self.innecesarios_label = tk.Label(
            middle_frame,
            text="Innecesarios: $0",
            font=("Poppins", 10),
            fg="#FF7043",
            bg="#333333",
        )
        self.innecesarios_label.pack(side="left", padx=15)

        self.total_expenses_label = tk.Label(
            middle_frame,
            text="Total Egresos (C): $0",
            font=("Poppins", 12, "bold"),
            fg="#FF5722",
            bg="#333333",
        )
        self.total_expenses_label.pack(side="right", padx=15)

        # Bottom row - Automatic calculations and balance
        bottom_frame = tk.Frame(summary_frame, bg="#333333")
        bottom_frame.pack(fill="x", pady=(5, 10))

        self.ahorro_label = tk.Label(
            bottom_frame,
            text="Ahorro (10%): $0",
            font=("Poppins", 10),
            fg="#81C784",
            bg="#333333",
        )
        self.ahorro_label.pack(side="left", padx=15)

        self.deuda_label = tk.Label(
            bottom_frame,
            text="Pago Deuda (5%): $0",
            font=("Poppins", 10),
            fg="#FFB74D",
            bg="#333333",
        )
        self.deuda_label.pack(side="left", padx=15)

        self.inversion_label = tk.Label(
            bottom_frame,
            text="Inversión (10%): $0",
            font=("Poppins", 10),
            fg="#64B5F6",
            bg="#333333",
        )
        self.inversion_label.pack(side="left", padx=15)

        self.balance_label = tk.Label(
            bottom_frame,
            text="Balance Final: $0",
            font=("Poppins", 14, "bold"),
            fg="white",
            bg="#333333",
        )
        self.balance_label.pack(side="right", padx=15)

    def get_month_year_text(self):
        """Get formatted month and year text"""
        month_names = [
            "Enero",
            "Febrero",
            "Marzo",
            "Abril",
            "Mayo",
            "Junio",
            "Julio",
            "Agosto",
            "Septiembre",
            "Octubre",
            "Noviembre",
            "Diciembre",
        ]
        return f"{month_names[self.current_month - 1]} {self.current_year}"

    def prev_month(self):
        """Navigate to previous month"""
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.month_label.config(text=self.get_month_year_text())
        self.load_data()

    def next_month(self):
        """Navigate to next month"""
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.month_label.config(text=self.get_month_year_text())
        self.load_data()

    def add_transaction(
        self, transaction_type, amount_entry, desc_entry, category_combo
    ):
        """Add a new transaction of any type"""
        try:
            amount = float(amount_entry.get())
            description = desc_entry.get().strip()
            category = category_combo.get()

            if not description or not category:
                messagebox.showerror("Error", "Por favor completa todos los campos")
                return

            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            self.cursor.execute(
                """
                INSERT INTO transactions (type, amount, description, category, month, year, date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    transaction_type,
                    amount,
                    description,
                    category,
                    self.current_month,
                    self.current_year,
                    date,
                ),
            )

            self.conn.commit()

            # Clear entries
            amount_entry.delete(0, tk.END)
            desc_entry.delete(0, tk.END)
            category_combo.set("")

            self.load_data()
            messagebox.showinfo("Éxito", "Transacción agregada exitosamente!")

        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa un valor válido")

    def delete_transaction(self, transaction_type):
        """Delete selected transaction"""
        # Get the appropriate listbox
        listbox_map = {
            "income_fixed": self.fixed_listbox,
            "income_variable": self.variable_listbox,
            "expense_indispensable": self.indispensable_listbox,
            "expense_necesarios": self.necesarios_listbox,
            "expense_innecesarios": self.innecesarios_listbox,
        }

        listbox = listbox_map.get(transaction_type)
        if not listbox:
            return

        selection = listbox.curselection()
        if not selection:
            messagebox.showwarning(
                "Advertencia", "Por favor selecciona una transacción para eliminar"
            )
            return

        # Get the transaction ID from the selected item
        selected_text = listbox.get(selection[0])
        transaction_id = (
            selected_text.split(" | ID: ")[1] if " | ID: " in selected_text else None
        )

        if transaction_id:
            if messagebox.askyesno(
                "Confirmar", "¿Estás seguro de que quieres eliminar esta transacción?"
            ):
                self.cursor.execute(
                    "DELETE FROM transactions WHERE id = ?", (transaction_id,)
                )
                self.conn.commit()
                self.load_data()
                messagebox.showinfo("Éxito", "Transacción eliminada exitosamente!")

    def load_data(self):
        """Load data from database and update UI for current month"""
        # Clear all listboxes
        listboxes = {
            "income_fixed": self.fixed_listbox,
            "income_variable": self.variable_listbox,
            "expense_indispensable": self.indispensable_listbox,
            "expense_necesarios": self.necesarios_listbox,
            "expense_innecesarios": self.innecesarios_listbox,
        }

        for listbox in listboxes.values():
            listbox.delete(0, tk.END)

        # Initialize totals
        totals = {
            "income_fixed": 0,
            "income_variable": 0,
            "expense_indispensable": 0,
            "expense_necesarios": 0,
            "expense_innecesarios": 0,
        }

        # Load transactions for current month and year
        for transaction_type in listboxes.keys():
            self.cursor.execute(
                "SELECT * FROM transactions WHERE type = ? AND month = ? AND year = ? ORDER BY date DESC",
                (transaction_type, self.current_month, self.current_year),
            )
            transactions = self.cursor.fetchall()

            for transaction in transactions:
                # Handle both old and new schema
                if len(transaction) == 6:  # Old schema
                    id_val, _, amount, description, category, _ = transaction
                else:  # New schema
                    id_val, _, amount, description, category, _, _, _ = transaction

                totals[transaction_type] += amount
                display_text = (
                    f"${amount:,.0f} - {description} ({category}) | ID: {id_val}"
                )
                listboxes[transaction_type].insert(tk.END, display_text)

        # Calculate totals and automatic allocations
        total_income = totals["income_fixed"] + totals["income_variable"]
        total_expenses = (
            totals["expense_indispensable"]
            + totals["expense_necesarios"]
            + totals["expense_innecesarios"]
        )

        # Automatic calculations (percentages of total income)
        ahorro = total_income * 0.10
        pago_deuda = total_income * 0.05
        inversion = total_income * 0.10
        total_otros = ahorro + pago_deuda + inversion

        # Final balance
        balance = total_income - total_otros - total_expenses

        # Update all labels
        self.income_fixed_label.config(
            text=f"Ingresos Fijos: ${totals['income_fixed']:,.0f}"
        )
        self.income_variable_label.config(
            text=f"Ingresos Variables: ${totals['income_variable']:,.0f}"
        )
        self.total_income_label.config(text=f"Total Ingresos (A): ${total_income:,.0f}")

        self.indispensable_label.config(
            text=f"Indispensables: ${totals['expense_indispensable']:,.0f}"
        )
        self.necesarios_label.config(
            text=f"Necesarios: ${totals['expense_necesarios']:,.0f}"
        )
        self.innecesarios_label.config(
            text=f"Innecesarios: ${totals['expense_innecesarios']:,.0f}"
        )
        self.total_expenses_label.config(
            text=f"Total Egresos (C): ${total_expenses:,.0f}"
        )

        self.ahorro_label.config(text=f"Ahorro (10%): ${ahorro:,.0f}")
        self.deuda_label.config(text=f"Pago Deuda (5%): ${pago_deuda:,.0f}")
        self.inversion_label.config(text=f"Inversión (10%): ${inversion:,.0f}")

        balance_color = "#4CAF50" if balance >= 0 else "#f44336"
        self.balance_label.config(
            text=f"Balance Final: ${balance:,.0f}", fg=balance_color
        )

    def __del__(self):
        """Close database connection when app is destroyed"""
        if hasattr(self, "conn"):
            self.conn.close()


def main():
    root = tk.Tk()
    app = FinanceApp(root)

    def on_closing():
        if hasattr(app, "conn"):
            app.conn.close()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
