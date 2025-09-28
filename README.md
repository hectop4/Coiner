# Coiner - Personal Finance Manager

Una aplicación de gestión de finanzas personales desarrollada con tkinter que permite rastrear ingresos y gastos.

## Características

- **Gestión de Ingresos**: Añade y rastrea diferentes tipos de ingresos (salario, freelance, inversiones, etc.)
- **Gestión de Gastos**: Registra gastos en diferentes categorías (comida, transporte, vivienda, etc.)
- **Base de Datos**: Almacenamiento persistente usando SQLite
- **Resumen Financiero**: Visualiza el balance total, ingresos y gastos
- **Interfaz Intuitiva**: Diseño limpio inspirado en aplicaciones modernas de finanzas

## Estructura de la Aplicación

```
coiner/
├── main.py              # Aplicación principal
├── requirements.txt     # Dependencias del proyecto
├── README.md           # Documentación
└── finance.db          # Base de datos SQLite (se crea automáticamente)
```

## Instalación y Uso

1. **Clonar o descargar el proyecto**

   ```bash
   cd /home/hectorpuentes/projects/in_progress/coiner
   ```

2. **Activar el entorno virtual** (si existe)

   ```bash
   source .venv/bin/activate
   ```

3. **Ejecutar la aplicación**
   ```bash
   python main.py
   ```

## Funcionalidades

### Añadir Ingresos

1. En la sección "Incomes" (izquierda):
   - Ingresa el monto
   - Añade una descripción
   - Selecciona una categoría
   - Haz clic en "Add Income"

### Añadir Gastos

1. En la sección "Outcomes" (derecha):
   - Ingresa el monto del gasto
   - Añade una descripción
   - Selecciona una categoría
   - Haz clic en "Add Expense"

### Eliminar Transacciones

1. Selecciona una transacción de la lista
2. Haz clic en "Delete Selected"
3. Confirma la eliminación

### Ver Resumen

- El panel inferior muestra:
  - Total de ingresos
  - Total de gastos
  - Balance actual (verde si es positivo, rojo si es negativo)

## Categorías Predefinidas

### Ingresos

- Salary (Salario)
- Freelance
- Investment (Inversión)
- Business (Negocio)
- Other (Otro)

### Gastos

- Food (Comida)
- Transportation (Transporte)
- Housing (Vivienda)
- Entertainment (Entretenimiento)
- Healthcare (Salud)
- Other (Otro)

## Base de Datos

La aplicación utiliza SQLite para almacenar las transacciones. La base de datos se crea automáticamente al ejecutar la aplicación por primera vez.

### Esquema de la Base de Datos

```sql
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL,        -- 'income' o 'outcome'
    amount REAL NOT NULL,      -- Monto de la transacción
    description TEXT NOT NULL, -- Descripción de la transacción
    category TEXT NOT NULL,    -- Categoría de la transacción
    date TEXT NOT NULL         -- Fecha y hora de la transacción
);
```

## Personalización

Puedes personalizar fácilmente:

- Colores de la interfaz modificando los valores hexadecimales en `main.py`
- Categorías añadiendo nuevos valores en las listas de `values` de los ComboBox
- Funcionalidades adicionales extendiendo la clase `FinanceApp`

## Requisitos del Sistema

- Python 3.7 o superior
- tkinter (incluido en la instalación estándar de Python)
- sqlite3 (incluido en la instalación estándar de Python)

## Notas

- La aplicación guarda automáticamente todos los datos en la base de datos local
- Los datos persisten entre sesiones de la aplicación
- La interfaz está diseñada para ser responsive y user-friendly
