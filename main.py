import tkinter as tk
from tkinter import ttk
import sqlite3
import math
from datetime import datetime


def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius=15, **kwargs):
    """Create a rounded rectangle on a canvas using arcs and lines"""
    if radius > (x2 - x1) / 2:
        radius = (x2 - x1) / 2
    if radius > (y2 - y1) / 2:
        radius = (y2 - y1) / 2

    # Create the rounded rectangle using multiple shapes and return all IDs
    elements = []

    # Main rectangles
    elements.append(canvas.create_rectangle(x1 + radius, y1, x2 - radius, y2, outline="", **kwargs))
    elements.append(canvas.create_rectangle(x1, y1 + radius, x2, y2 - radius, outline="", **kwargs))

    # Corners (ovals)
    elements.append(canvas.create_oval(x1, y1, x1 + 2*radius, y1 + 2*radius, outline="", **kwargs))  # Top-left
    elements.append(canvas.create_oval(x2 - 2*radius, y1, x2, y1 + 2*radius, outline="", **kwargs))  # Top-right
    elements.append(canvas.create_oval(x1, y2 - 2*radius, x1 + 2*radius, y2, outline="", **kwargs))  # Bottom-left
    elements.append(canvas.create_oval(x2 - 2*radius, y2 - 2*radius, x2, y2, outline="", **kwargs))  # Bottom-right

    return elements

# Add method to Canvas class
tk.Canvas.create_rounded_rectangle = create_rounded_rectangle


class FinanceApp:
    def create_rounded_button(self, parent, text, command, bg_color, fg_color, font, width=140, height=45, corner_radius=12):
        """Create a button with rounded corners using Canvas"""
        # Get parent background color
        try:
            parent_bg = parent.cget('bg')
        except:
            parent_bg = "#2c2c2c"

        canvas = tk.Canvas(parent, width=width, height=height, highlightthickness=0, bg=parent_bg, bd=0)

        # Create rounded rectangle and store all element IDs
        button_elements = canvas.create_rounded_rectangle(
            2, 2, width - 2, height - 2,
            radius=corner_radius, fill=bg_color
        )

        # Add text
        text_id = canvas.create_text(
            width // 2, height // 2,
            text=text, fill=fg_color, font=font
        )

        # Store references for hover effect
        canvas.bg_color = bg_color
        canvas.text_id = text_id
        canvas.button_elements = button_elements

        # Bind click event
        canvas.bind("<Button-1>", lambda e: command())
        canvas.bind("<Enter>", lambda e: self.on_button_hover_enter(canvas))
        canvas.bind("<Leave>", lambda e: self.on_button_hover_leave(canvas))
        canvas.configure(cursor="hand2")

        return canvas

    def on_button_hover_enter(self, canvas):
        """Handle button hover enter"""
        hover_color = self.darken_color(canvas.bg_color)
        # Update all button elements
        if hasattr(canvas, 'button_elements'):
            for element_id in canvas.button_elements:
                try:
                    canvas.itemconfig(element_id, fill=hover_color)
                except:
                    pass

    def on_button_hover_leave(self, canvas):
        """Handle button hover leave"""
        # Restore original color for all button elements
        if hasattr(canvas, 'button_elements'):
            for element_id in canvas.button_elements:
                try:
                    canvas.itemconfig(element_id, fill=canvas.bg_color)
                except:
                    pass

    def darken_color(self, color):
        """Darken a hex color"""
        if color.startswith('#'):
            hex_color = color[1:]
            rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            darkened = tuple(max(0, int(c * 0.8)) for c in rgb)
            return '#%02x%02x%02x' % darkened
        return color

    def create_rounded_entry(self, parent, font, width=200, height=35, corner_radius=8):
        """Create an entry widget with rounded corners"""
        try:
            parent_bg = parent.cget('bg')
        except:
            parent_bg = "#404040"

        # Container frame
        container = tk.Frame(parent, bg=parent_bg)

        # Canvas for rounded background
        canvas = tk.Canvas(container, width=width, height=height, highlightthickness=0, bg=parent_bg, bd=0)
        canvas.pack()

        # Create rounded rectangle background
        canvas.create_rounded_rectangle(
            1, 1, width - 1, height - 1,
            radius=corner_radius, fill="white"
        )

        # Entry widget
        entry = tk.Entry(
            canvas,
            font=font,
            bg="white",
            fg="#2c2c2c",
            relief="flat",
            bd=0,
            highlightthickness=0
        )

        # Position entry in center of canvas
        canvas.create_window(width//2, height//2, window=entry, width=width-20, height=height-10)

        return container, entry

    def create_rounded_frame(self, parent, bg_color, width, height, corner_radius=15):
        """Create a frame with rounded corners using Canvas"""
        try:
            parent_bg = parent.cget('bg')
        except:
            parent_bg = "#2c2c2c"

        canvas = tk.Canvas(parent, width=width, height=height, highlightthickness=0, bg=parent_bg, bd=0)

        # Create rounded rectangle
        canvas.create_rounded_rectangle(
            0, 0, width, height,
            radius=corner_radius, fill=bg_color
        )

        return canvas

    def show_custom_popup(self, title, message, popup_type="info"):
        """Create a custom popup window without system frames"""
        # Create toplevel window
        popup = tk.Toplevel(self.root)
        popup.overrideredirect(True)  # Remove system window decorations
        popup.configure(bg="#2c2c2c")

        # Calculate size and position
        width = 450
        height = 250
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (width // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (height // 2)
        popup.geometry(f"{width}x{height}+{x}+{y}")

        # Make popup modal
        popup.transient(self.root)

        # Main container with rounded appearance
        main_frame = tk.Frame(popup, bg="#2c2c2c")
        main_frame.pack(fill="both", expand=True, padx=8, pady=8)

        # Inner frame with rounded background
        inner_frame = tk.Frame(main_frame, bg="#3a3a3a")
        inner_frame.pack(fill="both", expand=True, padx=4, pady=4)

        # Title section
        title_frame = tk.Frame(inner_frame, bg="#3a3a3a")
        title_frame.pack(fill="x", pady=(15, 10))

        title_label = tk.Label(
            title_frame,
            text=title,
            font=("Poppins", 14, "bold"),
            fg="white",
            bg="#3a3a3a"
        )
        title_label.pack()

        # Message section
        message_frame = tk.Frame(inner_frame, bg="#3a3a3a")
        message_frame.pack(fill="both", expand=True, pady=(0, 20))

        message_label = tk.Label(
            message_frame,
            text=message,
            font=("Poppins", 11),
            fg="#e0e0e0",
            bg="#3a3a3a",
            wraplength=400,
            justify="center"
        )
        message_label.pack(expand=True, pady=(10, 20))

        # Button section
        button_frame = tk.Frame(inner_frame, bg="#3a3a3a")
        button_frame.pack(pady=(0, 15))

        # Determine button color based on popup type
        button_colors = {
            "info": "#2196F3",
            "success": "#4CAF50",
            "warning": "#FF9800",
            "error": "#f44336"
        }
        button_color = button_colors.get(popup_type, "#2196F3")

        # Rounded close button
        close_btn = self.create_rounded_button(
            button_frame,
            text="Cerrar",
            command=popup.destroy,
            bg_color=button_color,
            fg_color="white",
            font=("Poppins", 11, "bold"),
            width=100,
            height=40,
            corner_radius=10
        )
        close_btn.pack()

        # Add subtle shadow effect with multiple frames
        shadow_frame1 = tk.Frame(popup, bg="#1a1a1a", height=2)
        shadow_frame1.place(x=2, y=height-2, width=width-2)

        shadow_frame2 = tk.Frame(popup, bg="#1a1a1a", width=2)
        shadow_frame2.place(x=width-2, y=2, height=height-2)

        # Bind Escape key to close
        popup.bind('<Escape>', lambda e: popup.destroy())

        # Make sure window is visible before grab_set
        popup.update_idletasks()
        popup.grab_set()

        # Focus on popup
        popup.focus_set()

        return popup

    def show_info_popup(self, message):
        """Show an info popup"""
        return self.show_custom_popup("Información", message, "info")

    def show_success_popup(self, message):
        """Show a success popup"""
        return self.show_custom_popup("Éxito", message, "success")

    def show_warning_popup(self, message):
        """Show a warning popup"""
        return self.show_custom_popup("Advertencia", message, "warning")

    def show_error_popup(self, message):
        """Show an error popup"""
        return self.show_custom_popup("Error", message, "error")

    def show_confirmation_popup(self, title, message):
        """Show a confirmation popup with Yes/No buttons"""
        # Create toplevel window
        popup = tk.Toplevel(self.root)
        popup.overrideredirect(True)
        popup.configure(bg="#2c2c2c")

        # Calculate size and position
        width = 480
        height = 260
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (width // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (height // 2)
        popup.geometry(f"{width}x{height}+{x}+{y}")

        # Make popup modal
        popup.transient(self.root)

        # Store result
        result = {"value": False}

        # Main container
        main_frame = tk.Frame(popup, bg="#2c2c2c")
        main_frame.pack(fill="both", expand=True, padx=8, pady=8)

        inner_frame = tk.Frame(main_frame, bg="#3a3a3a")
        inner_frame.pack(fill="both", expand=True, padx=4, pady=4)

        # Title
        title_frame = tk.Frame(inner_frame, bg="#3a3a3a")
        title_frame.pack(fill="x", pady=(15, 10))

        title_label = tk.Label(
            title_frame,
            text=title,
            font=("Poppins", 14, "bold"),
            fg="white",
            bg="#3a3a3a"
        )
        title_label.pack()

        # Message
        message_frame = tk.Frame(inner_frame, bg="#3a3a3a")
        message_frame.pack(fill="both", expand=True, pady=(0, 20))

        message_label = tk.Label(
            message_frame,
            text=message,
            font=("Poppins", 11),
            fg="#e0e0e0",
            bg="#3a3a3a",
            wraplength=420,
            justify="center"
        )
        message_label.pack(expand=True, pady=(10, 20))

        # Buttons
        button_frame = tk.Frame(inner_frame, bg="#3a3a3a")
        button_frame.pack(pady=(0, 15))

        def on_yes():
            result["value"] = True
            popup.destroy()

        def on_no():
            result["value"] = False
            popup.destroy()

        # Yes button
        yes_btn = self.create_rounded_button(
            button_frame,
            text="Sí",
            command=on_yes,
            bg_color="#4CAF50",
            fg_color="white",
            font=("Poppins", 11, "bold"),
            width=80,
            height=35,
            corner_radius=8
        )
        yes_btn.pack(side="left", padx=(0, 10))

        # No button
        no_btn = self.create_rounded_button(
            button_frame,
            text="No",
            command=on_no,
            bg_color="#f44336",
            fg_color="white",
            font=("Poppins", 11, "bold"),
            width=80,
            height=35,
            corner_radius=8
        )
        no_btn.pack(side="left")

        # Shadow effect
        shadow_frame1 = tk.Frame(popup, bg="#1a1a1a", height=2)
        shadow_frame1.place(x=2, y=height-2, width=width-2)

        shadow_frame2 = tk.Frame(popup, bg="#1a1a1a", width=2)
        shadow_frame2.place(x=width-2, y=2, height=height-2)

        # Bind keys
        popup.bind('<Return>', lambda e: on_yes())
        popup.bind('<Escape>', lambda e: on_no())

        # Make sure window is visible before grab_set
        popup.update_idletasks()
        popup.grab_set()

        popup.focus_set()
        popup.wait_window()  # Wait for window to close

        return result["value"]

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
        style.configure('TNotebook', background='#2c2c2c', borderwidth=0, tabmargins=0)
        style.configure('TNotebook.Tab', background='#404040', foreground='white',
                       padding=[20, 8], borderwidth=0, focuscolor='none', relief='flat')
        style.map('TNotebook.Tab', background=[('selected', '#505050')])

        # Configure combobox to be flat
        style.configure('TCombobox', fieldbackground='white', borderwidth=0, relief='flat')
        style.configure('TCombobox.Listbox', background='white', borderwidth=0)

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
        # Form frame with rounded appearance
        outer_frame = tk.Frame(parent, bg="#3a3a3a")
        outer_frame.pack(pady=15, padx=20, fill="x")

        form_frame = tk.Frame(outer_frame, bg="#404040")
        form_frame.pack(pady=8, padx=8, fill="x", ipady=12, ipadx=12)

        tk.Label(
            form_frame,
            text="Valor:",
            fg="white",
            bg="#404040",
            font=("Poppins", 10, "bold"),
        ).pack(anchor="w")
        amount_entry = tk.Entry(
            form_frame,
            font=("Poppins", 11),
            bg="white",
            fg="#2c2c2c",
            relief="flat",
            bd=0,
            highlightthickness=0
        )
        amount_entry.pack(fill="x", pady=(5, 12), padx=4, ipady=6)

        tk.Label(
            form_frame,
            text="Descripción:",
            fg="white",
            bg="#404040",
            font=("Poppins", 10, "bold"),
        ).pack(anchor="w")
        desc_entry = tk.Entry(
            form_frame,
            font=("Poppins", 11),
            bg="white",
            fg="#2c2c2c",
            relief="flat",
            bd=0,
            highlightthickness=0
        )
        desc_entry.pack(fill="x", pady=(5, 12), padx=4, ipady=6)

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
            bg="#404040",
            font=("Poppins", 10, "bold"),
        ).pack(anchor="w")
        category_combo = ttk.Combobox(
            form_frame,
            values=categories[income_type],
            font=("Poppins", 11),
        )
        category_combo.pack(fill="x", pady=(5, 15), padx=4, ipady=4)

        # Rounded Add button
        add_btn = self.create_rounded_button(
            form_frame,
            text="Agregar",
            command=lambda: self.add_transaction(
                income_type, amount_entry, desc_entry, category_combo
            ),
            bg_color="#4CAF50",
            fg_color="white",
            font=("Poppins", 11, "bold"),
            width=140,
            height=45
        )
        add_btn.pack(pady=12)

        # List frame with rounded appearance
        list_outer_frame = tk.Frame(parent, bg="#3a3a3a")
        list_outer_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        list_frame = tk.Frame(list_outer_frame, bg="#454545")
        list_frame.pack(fill="both", expand=True, padx=8, pady=8, ipady=8, ipadx=8)

        # Scrollable listbox
        listbox_frame = tk.Frame(list_frame, bg="#454545")
        listbox_frame.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(
            listbox_frame,
            bg="#505050",
            troughcolor="#454545",
            bd=0,
            highlightthickness=0,
            relief="flat",
            width=12
        )
        scrollbar.pack(side="right", fill="y")

        listbox = tk.Listbox(
            listbox_frame,
            yscrollcommand=scrollbar.set,
            font=("Poppins", 9),
            bg="#505050",
            fg="white",
            relief="flat",
            bd=0,
            highlightthickness=0,
            selectbackground="#606060",
            selectforeground="white",
            activestyle="none"
        )
        listbox.pack(fill="both", expand=True, padx=(4, 16), pady=4)
        scrollbar.config(command=listbox.yview)

        # Store references
        if income_type == "income_fixed":
            self.fixed_listbox = listbox
        else:
            self.variable_listbox = listbox

        # Bind selection event to update allocations
        listbox.bind('<<ListboxSelect>>', lambda event: self.on_income_select(event, income_type))

        # Rounded Delete button
        delete_btn = self.create_rounded_button(
            list_frame,
            text="Eliminar Seleccionado",
            command=lambda: self.delete_transaction(income_type),
            bg_color="#f44336",
            fg_color="white",
            font=("Poppins", 9, "bold"),
            width=180,
            height=35,
            corner_radius=8
        )
        delete_btn.pack(pady=8)

    def create_allocations_section(self):
        """Create allocations section below income area"""
        # Outer frame for rounded appearance
        allocations_outer_frame = tk.Frame(self.root, bg="#2c2c2c", height=110)
        allocations_outer_frame.pack(fill="x", padx=20, pady=(10, 0))
        allocations_outer_frame.pack_propagate(False)

        allocations_frame = tk.Frame(allocations_outer_frame, bg="#3a3a3a")
        allocations_frame.pack(fill="both", expand=True, padx=8, pady=8, ipady=8, ipadx=8)

        # Title
        title_label = tk.Label(
            allocations_frame,
            text="Asignaciones Automáticas (Selecciona un ingreso)",
            font=("Poppins", 12, "bold"),
            fg="white",
            bg="#404040",
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
            bg="#404040",
        )
        self.selected_ahorro_label.pack(side="left", padx=20)

        # Debt payment allocation
        self.selected_deuda_label = tk.Label(
            allocations_row,
            text="Pago Deuda (5%): $0",
            font=("Poppins", 11, "bold"),
            fg="#FFB74D",
            bg="#404040",
        )
        self.selected_deuda_label.pack(side="left", padx=20)

        # Investment allocation
        self.selected_inversion_label = tk.Label(
            allocations_row,
            text="Inversión (10%): $0",
            font=("Poppins", 11, "bold"),
            fg="#64B5F6",
            bg="#404040",
        )
        self.selected_inversion_label.pack(side="left", padx=20)

    def on_income_select(self, event, income_type):
        """Handle income item selection to update allocations"""
        listbox = event.widget
        selection = listbox.curselection()

        if selection:
            # Get selected item text
            selected_text = listbox.get(selection[0])

            # Extract amount from the text (format: "$amount - description (category) | ID: id_val")
            try:
                # Split by " - " and take the first part which contains "$amount"
                amount_part = selected_text.split(" - ")[0]
                # Remove the "$" and any commas, then convert to float
                amount_str = amount_part.replace("$", "").replace(",", "")
                amount = float(amount_str)

                # Calculate allocations for this specific income
                ahorro = amount * 0.10
                deuda = amount * 0.05
                inversion = amount * 0.10

                # Update allocation labels
                self.selected_ahorro_label.config(text=f"Ahorro (10%): ${ahorro:,.0f}")
                self.selected_deuda_label.config(text=f"Pago Deuda (5%): ${deuda:,.0f}")
                self.selected_inversion_label.config(text=f"Inversión (10%): ${inversion:,.0f}")

            except (IndexError, ValueError) as e:
                # Reset if can't parse amount
                print(f"Error parsing amount from: {selected_text} - {e}")
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
        # Form frame with rounded appearance
        outer_frame = tk.Frame(parent, bg="#3a3a3a")
        outer_frame.pack(pady=15, padx=20, fill="x")

        form_frame = tk.Frame(outer_frame, bg="#404040")
        form_frame.pack(pady=8, padx=8, fill="x", ipady=12, ipadx=12)

        tk.Label(
            form_frame,
            text="Valor:",
            fg="white",
            bg="#404040",
            font=("Poppins", 10, "bold"),
        ).pack(anchor="w")
        amount_entry = tk.Entry(
            form_frame,
            font=("Poppins", 11),
            bg="white",
            fg="#2c2c2c",
            relief="flat",
            bd=0,
            highlightthickness=0
        )
        amount_entry.pack(fill="x", pady=(5, 12), padx=4, ipady=6)

        tk.Label(
            form_frame,
            text="Descripción:",
            fg="white",
            bg="#404040",
            font=("Poppins", 10, "bold"),
        ).pack(anchor="w")
        desc_entry = tk.Entry(
            form_frame,
            font=("Poppins", 11),
            bg="white",
            fg="#2c2c2c",
            relief="flat",
            bd=0,
            highlightthickness=0
        )
        desc_entry.pack(fill="x", pady=(5, 12), padx=4, ipady=6)

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
            bg="#404040",
            font=("Poppins", 10, "bold"),
        ).pack(anchor="w")
        category_combo = ttk.Combobox(
            form_frame,
            values=categories[expense_type],
            font=("Poppins", 11),
        )
        category_combo.pack(fill="x", pady=(5, 15), padx=4, ipady=4)

        # Rounded Add button for expenses
        add_btn = self.create_rounded_button(
            form_frame,
            text="Agregar",
            command=lambda: self.add_transaction(
                expense_type, amount_entry, desc_entry, category_combo
            ),
            bg_color="#FF5722",
            fg_color="white",
            font=("Poppins", 11, "bold"),
            width=140,
            height=45
        )
        add_btn.pack(pady=12)

        # List frame with rounded appearance
        list_outer_frame = tk.Frame(parent, bg="#3a3a3a")
        list_outer_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        list_frame = tk.Frame(list_outer_frame, bg="#454545")
        list_frame.pack(fill="both", expand=True, padx=8, pady=8, ipady=8, ipadx=8)

        # Scrollable listbox
        listbox_frame = tk.Frame(list_frame, bg="#454545")
        listbox_frame.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(
            listbox_frame,
            bg="#505050",
            troughcolor="#454545",
            bd=0,
            highlightthickness=0,
            relief="flat",
            width=12
        )
        scrollbar.pack(side="right", fill="y")

        listbox = tk.Listbox(
            listbox_frame,
            yscrollcommand=scrollbar.set,
            font=("Poppins", 9),
            bg="#505050",
            fg="white",
            relief="flat",
            bd=0,
            highlightthickness=0,
            selectbackground="#606060",
            selectforeground="white",
            activestyle="none"
        )
        listbox.pack(fill="both", expand=True, padx=(4, 16), pady=4)
        scrollbar.config(command=listbox.yview)

        # Store references
        if expense_type == "expense_indispensable":
            self.indispensable_listbox = listbox
        elif expense_type == "expense_necesarios":
            self.necesarios_listbox = listbox
        else:
            self.innecesarios_listbox = listbox

        # Rounded Delete button for expenses
        delete_btn = self.create_rounded_button(
            list_frame,
            text="Eliminar Seleccionado",
            command=lambda: self.delete_transaction(expense_type),
            bg_color="#f44336",
            fg_color="white",
            font=("Poppins", 9, "bold"),
            width=180,
            height=35,
            corner_radius=8
        )
        delete_btn.pack(pady=8)

    def create_summary_section(self):
        """Create comprehensive summary section"""
        summary_frame = tk.Frame(self.root, bg="#2c2c2c", height=140)
        summary_frame.pack(fill="x", side="bottom", padx=20, pady=(0, 20))
        summary_frame.pack_propagate(False)

        # Top row - Income totals
        top_frame = tk.Frame(summary_frame, bg="#2c2c2c")
        top_frame.pack(fill="x", pady=(10, 5))

        self.income_fixed_label = tk.Label(
            top_frame,
            text="Ingresos Fijos: $0",
            font=("Poppins", 11, "bold"),
            fg="#4CAF50",
            bg="#2c2c2c",
        )
        self.income_fixed_label.pack(side="left", padx=15)

        self.income_variable_label = tk.Label(
            top_frame,
            text="Ingresos Variables: $0",
            font=("Poppins", 11, "bold"),
            fg="#4CAF50",
            bg="#2c2c2c",
        )
        self.income_variable_label.pack(side="left", padx=15)

        self.total_income_label = tk.Label(
            top_frame,
            text="Total Ingresos (A): $0",
            font=("Poppins", 12, "bold"),
            fg="#66BB6A",
            bg="#2c2c2c",
        )
        self.total_income_label.pack(side="right", padx=15)

        # Middle row - Expenses
        middle_frame = tk.Frame(summary_frame, bg="#2c2c2c")
        middle_frame.pack(fill="x", pady=2)

        self.indispensable_label = tk.Label(
            middle_frame,
            text="Indispensables: $0",
            font=("Poppins", 10),
            fg="#FF7043",
            bg="#2c2c2c",
        )
        self.indispensable_label.pack(side="left", padx=15)

        self.necesarios_label = tk.Label(
            middle_frame,
            text="Necesarios: $0",
            font=("Poppins", 10),
            fg="#FF7043",
            bg="#2c2c2c",
        )
        self.necesarios_label.pack(side="left", padx=15)

        self.innecesarios_label = tk.Label(
            middle_frame,
            text="Innecesarios: $0",
            font=("Poppins", 10),
            fg="#FF7043",
            bg="#2c2c2c",
        )
        self.innecesarios_label.pack(side="left", padx=15)

        self.total_expenses_label = tk.Label(
            middle_frame,
            text="Total Egresos (C): $0",
            font=("Poppins", 12, "bold"),
            fg="#FF5722",
            bg="#2c2c2c",
        )
        self.total_expenses_label.pack(side="right", padx=15)

        # Bottom row - Automatic calculations and balance
        bottom_frame = tk.Frame(summary_frame, bg="#2c2c2c")
        bottom_frame.pack(fill="x", pady=(5, 10))

        self.ahorro_label = tk.Label(
            bottom_frame,
            text="Ahorro (10%): $0",
            font=("Poppins", 10),
            fg="#81C784",
            bg="#2c2c2c",
        )
        self.ahorro_label.pack(side="left", padx=15)

        self.deuda_label = tk.Label(
            bottom_frame,
            text="Pago Deuda (5%): $0",
            font=("Poppins", 10),
            fg="#FFB74D",
            bg="#2c2c2c",
        )
        self.deuda_label.pack(side="left", padx=15)

        self.inversion_label = tk.Label(
            bottom_frame,
            text="Inversión (10%): $0",
            font=("Poppins", 10),
            fg="#64B5F6",
            bg="#2c2c2c",
        )
        self.inversion_label.pack(side="left", padx=15)

        self.balance_label = tk.Label(
            bottom_frame,
            text="Balance Final: $0",
            font=("Poppins", 14, "bold"),
            fg="white",
            bg="#2c2c2c",
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
                self.show_error_popup("Por favor completa todos los campos")
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
            self.show_success_popup("Transacción agregada exitosamente!")

        except ValueError:
            self.show_error_popup("Por favor ingresa un valor válido")

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
            self.show_warning_popup("Por favor selecciona una transacción para eliminar")
            return

        # Get the transaction ID from the selected item
        selected_text = listbox.get(selection[0])
        transaction_id = (
            selected_text.split(" | ID: ")[1] if " | ID: " in selected_text else None
        )

        if transaction_id:
            if self.show_confirmation_popup(
                "Confirmar", "¿Estás seguro de que quieres eliminar esta transacción?"
            ):
                self.cursor.execute(
                    "DELETE FROM transactions WHERE id = ?", (transaction_id,)
                )
                self.conn.commit()
                self.load_data()
                self.show_success_popup("Transacción eliminada exitosamente!")

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
