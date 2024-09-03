import tkinter as tk                            # Used to create GUI
from tkinter import ttk, messagebox as mssg     # Provides a set of widgets, display dialog boxes, 
import sqlite3                                  # Python library for interacting with SQLite databases
import datetime                                 # Provides classes for working with dates and times in Python.

class DataBaseBuild:
    def __init__(self):
        # Name of the database file
        self.db_name = 'manejo_inventario.db'
        # Create the database file if it doesn't exist
        self.database_build()
    
    def database_build(self):  
        # Establish a connection to the database 
        with sqlite3.connect(self.db_name) as conn:
            
            # In order to interact with the database.
            cursor = conn.cursor()
            
            # Execute an SQL query to create the 'Proveedores' table if it does not exist.
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Proveedores (
                    IdNit TEXT PRIMARY KEY,
                    Nombre TEXT,
                    FechaCompra TEXT
                )
            """)
            
            # Execute an SQL query to create the 'Productos' table if it does not exist.
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Productos (
                    IdNit TEXT,
                    Codigo TEXT PRIMARY KEY,
                    Nombre TEXT,
                    Medida INTEGER,
                    Cantidad INTEGER,
                    Precio REAL,
                    FechaVencimiento TEXT,
                    FOREIGN KEY(IdNit) REFERENCES Proveedores(IdNit)
                )
            """)
            
            # Commit the changes made to the database.
            conn.commit()

    def run_query(self, query, parameters=()):
        # Open a connection to the SQLite database 
        with sqlite3.connect(self.db_name) as conn:
            # Create a cursor 
            cursor = conn.cursor()
            
            # Execute the SQL query with the provided parameters
            # query: SELECT, INSERT, UPDATE, DELETE. The action
            # parameters: the values
            result = cursor.execute(query, parameters)
            
            # Commit the transaction to save changes to the database (e.g., INSERT, UPDATE, DELETE)
            conn.commit()
        
        # Return the result of the executed query
        return result

    # Proveedores operations

    # Insert a new proveedor
    def insert_proveedor(self, id_nit, nombre, fecha_compra):   
        query = 'INSERT INTO Proveedores VALUES (?, ?, ?)'  # The ? will be change with the values
        parameters = (id_nit, nombre, fecha_compra)         # The values to be inserted, replace the ?, ?, ?
        # Call the run_query method to execute the command.
        self.run_query(query, parameters)               

    # Gets all records from Proveedores table
    def get_proveedores(self):
        # SQL query to select all rows from Proveedores table
        query = 'SELECT * FROM Proveedores'
        # Call the run_query method to return the result
        return self.run_query(query)

    # Update an existing record in Proveedores table
    def update_proveedor(self, id_nit, nombre, fecha_compra):
        # SQL query to update
        query = 'UPDATE Proveedores SET Nombre = ?, FechaCompra = ? WHERE IdNit = ?'
        # New values for Nombre and FechaCompra
        parameters = (nombre, fecha_compra, id_nit)
        # Call the run_query method to update parameters
        self.run_query(query, parameters)

    # Delete a record from the Proveedores table
    def delete_proveedor(self, id_nit):
        # SQL query to delete a row 
        query = 'DELETE FROM Proveedores WHERE IdNit = ?'
        # Call the run_query method to remove the row where IdNit matches the given value.
        self.run_query(query, (id_nit,))

    # Search for a specific record in the Proveedores table
    def search_proveedor(self, id_nit):
        # SQL query to select a row where IdNit matches the given value
        query = 'SELECT * FROM Proveedores WHERE IdNit = ?'
        # Call the run_query method to return the result
        return self.run_query(query, (id_nit,))

    # Product operations
    # Same logic as Proveedor operations
    def insert_producto(self, id_nit, codigo, nombre, unidad, cantidad, precio, fecha_vencimiento):
        query = 'INSERT INTO Productos VALUES (?, ?, ?, ?, ?, ?, ?)'
        parameters = (id_nit, codigo, nombre, unidad, cantidad, precio, fecha_vencimiento)
        self.run_query(query, parameters)

    def get_productos(self):
        query = 'SELECT * FROM Productos'
        return self.run_query(query)

    def update_producto(self, codigo, nombre, unidad, cantidad, precio, fecha_vencimiento):
        query = '''
            UPDATE Productos 
            SET Nombre = ?, Medida = ?, Cantidad = ?, Precio = ?, FechaVencimiento = ? 
            WHERE Codigo = ?
        '''
        parameters = (nombre, unidad, cantidad, precio, fecha_vencimiento, codigo)
        self.run_query(query, parameters)

    def delete_producto(self, codigo):
        query = 'DELETE FROM Productos WHERE Codigo = ?'
        self.run_query(query, (codigo,))

    def search_producto(self, codigo):
        query = 'SELECT * FROM Productos WHERE Codigo = ?'
        return self.run_query(query, (codigo,))

class DataValidator:
    def __init__(self):
        pass                # This class does not perform any actions

    def no_spaces(self, text):
        # Check if there is at least one space in the text
        if ' ' in text:
            return False  
        else:
            return True   

    def max_length(self, text, length):
        # Check if the length of the provided text does not exceed the specified length
        text_length = len(text)  # Get the length of the text
        if text_length <= length:
            return True  
        else:
            return False 

    # Function to check if the provided text can be converted to a float
    def is_float(self, text):
        # Check if the provided text can be converted to a float
        try:
            # Try to convert the text to a float
            float_value = float(text)
            return True
        except ValueError:
            return False

    # Function to check if the provided text can be converted to an integer
    def is_integer(self, text):
        # Check if the provided text can be converted to an integer
        try:
            int(text)
            return True
        except ValueError:
            return False

    def is_valid_date(self, date_text):
        # Check if the length of date_text is 10 characters and format is 'dd/mm/yyyy'
        if len(date_text) != 10 or date_text[2] != '/' or date_text[5] != '/':
            return False

        # Extract day, month, and year parts from the date_text
        day_str = date_text[:2]
        month_str = date_text[3:5]
        year_str = date_text[6:]

        # Check if day, month, and year are all numeric
        if not (day_str.isdigit() and month_str.isdigit() and year_str.isdigit()):
            return False

        day = int(day_str)
        month = int(month_str)
        year = int(year_str)

        try:
            # Attempt to create a datetime object with the provided date
            datetime.datetime(year, month, day)
            return True
        except ValueError:
            return False
        
    def validate_id_nit(self, id_nit):
            if not self.no_spaces(id_nit):
                return "El ID NIT no debe contener espacios."
            return None

    def validate_nombre_proveedor(self, nombre):
        if not self.max_length(nombre, 25):
            return "El Nombre del Proveedor no debe exceder 25 caracteres."
        return None

    def validate_fecha_compra(self, fecha):
        if not self.is_valid_date(fecha):
            return "La Fecha de Compra no es válida. Use el formato dd/mm/yyyy."
        return None

    def validate_codigo(self, codigo):
        if not self.no_spaces(codigo):
            return "El Código no debe contener espacios."
        return None

    def validate_nombre_producto(self, nombre):
        if not self.max_length(nombre, 50):
            return "El Nombre del Producto no debe exceder 50 caracteres."
        return None

    def validate_unidad(self, unidad):
        if not self.is_integer(unidad):
            return "La Medida debe ser un número entero."
        return None

    def validate_cantidad(self, cantidad):
        if not self.is_integer(cantidad):
            return "La Cantidad debe ser un número entero."
        return None

    def validate_precio(self, precio):
        if not self.is_float(precio):
            return "El Precio debe ser un número."
        return None

    def validate_fecha_vencimiento(self, fecha):
        if not self.is_valid_date(fecha):
            return "La Fecha de Vencimiento no es válida. Use el formato dd/mm/yyyy."
        return None

class MainWindow:
    def __init__(self, window):
        # Store the reference to the main window
        self.wind = window
        self.wind.title("Sistema de Inventario")
        self.wind.geometry('1000x700')
        self.wind.resizable(False, False)

        # Initialize Database and Validator
        # Create an instance of DataBaseBuild to handle database operations
        self.db = DataBaseBuild()
        
        # Create an instance of DataValidator to handle data validation
        self.validator = DataValidator()

        # Set up the UI
        # Call the method to configure and set up the user interface
        self.setup_GUI()

        # Populate initial data
        # Fetch and display the initial product data from the database
        self.get_productos()

    def setup_GUI(self):
        # Frames
        frame = tk.LabelFrame(self.wind, text="Registrar Nuevo Producto")
        frame.grid(row=0, column=0, padx=20, pady=10)

        # Labels and Entries
        # Proveedor ID
        tk.Label(frame, text="ID NIT:").grid(row=0, column=0, pady=5, padx=5, sticky='e')
        self.id_nit = tk.Entry(frame)
        self.id_nit.grid(row=0, column=1, pady=5, padx=5)
        self.id_nit.bind("<FocusOut>", self.validate_id_nit)

        # Nombre Proveedor
        tk.Label(frame, text="Nombre Proveedor:").grid(row=1, column=0, pady=5, padx=5, sticky='e')
        self.nombre_proveedor = tk.Entry(frame)
        self.nombre_proveedor.grid(row=1, column=1, pady=5, padx=5)
        self.nombre_proveedor.bind("<FocusOut>", self.validate_nombre_proveedor)

        # Fecha Compra
        tk.Label(frame, text="Fecha Compra (dd/mm/yyyy):").grid(row=2, column=0, pady=5, padx=5, sticky='e')
        self.fecha_compra = tk.Entry(frame)
        self.fecha_compra.grid(row=2, column=1, pady=5, padx=5)
        self.fecha_compra.insert(0, 'dd/mm/yyyy')
        self.fecha_compra.bind("<FocusIn>", lambda e: self.fecha_compra.delete(0, tk.END))
        self.fecha_compra.bind("<FocusOut>", self.validate_fecha_compra)

        # Código Producto
        tk.Label(frame, text="Código Producto:").grid(row=3, column=0, pady=5, padx=5, sticky='e')
        self.codigo = tk.Entry(frame)
        self.codigo.grid(row=3, column=1, pady=5, padx=5)
        self.codigo.bind("<FocusOut>", self.validate_codigo)

        # Nombre Producto
        tk.Label(frame, text="Nombre Producto:").grid(row=4, column=0, pady=5, padx=5, sticky='e')
        self.nombre_producto = tk.Entry(frame)
        self.nombre_producto.grid(row=4, column=1, pady=5, padx=5)
        self.nombre_producto.bind("<FocusOut>", self.validate_nombre_producto)

        # Medida
        tk.Label(frame, text="Medida:").grid(row=5, column=0, pady=5, padx=5, sticky='e')
        self.unidad = tk.Entry(frame)
        self.unidad.grid(row=5, column=1, pady=5, padx=5)
        self.unidad.bind("<FocusOut>", self.validate_unidad)

        # Cantidad
        tk.Label(frame, text="Cantidad:").grid(row=6, column=0, pady=5, padx=5, sticky='e')
        self.cantidad = tk.Entry(frame)
        self.cantidad.grid(row=6, column=1, pady=5, padx=5)
        self.cantidad.bind("<FocusOut>", self.validate_cantidad)

        # Precio
        tk.Label(frame, text="Precio:").grid(row=7, column=0, pady=5, padx=5, sticky='e')
        self.precio = tk.Entry(frame)
        self.precio.grid(row=7, column=1, pady=5, padx=5)
        self.precio.bind("<FocusOut>", self.validate_precio)

        # Fecha Vencimiento
        tk.Label(frame, text="Fecha Vencimiento (dd/mm/yyyy):").grid(row=8, column=0, pady=5, padx=5, sticky='e')
        self.fecha_vencimiento = tk.Entry(frame)
        self.fecha_vencimiento.grid(row=8, column=1, pady=5, padx=5)
        self.fecha_vencimiento.insert(0, 'dd/mm/yyyy')
        self.fecha_vencimiento.bind("<FocusIn>", lambda e: self.fecha_vencimiento.delete(0, tk.END))
        self.fecha_vencimiento.bind("<FocusOut>", self.validate_fecha_vencimiento)

        # Buttons
        ttk.Button(frame, text="Guardar Producto", command=self.add_producto).grid(row=9, column=0, pady=10, padx=5)
        ttk.Button(frame, text="Actualizar Producto", command=self.update_producto).grid(row=9, column=1, pady=10, padx=5)
        ttk.Button(frame, text="Eliminar Producto", command=self.delete_producto).grid(row=10, column=0, pady=10, padx=5)
        ttk.Button(frame, text="Limpiar Campos", command=self.clear_fields).grid(row=10, column=1, pady=10, padx=5)

        # Treeview
        self.tree = ttk.Treeview(self.wind, columns=("IdNit", "Codigo", "Nombre", "Medida", "Cantidad", "Precio", "FechaVencimiento"), show='headings')
        self.tree.heading("IdNit", text="ID NIT")
        self.tree.heading("Codigo", text="Código")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Medida", text="Medida")
        self.tree.heading("Cantidad", text="Cantidad")
        self.tree.heading("Precio", text="Precio")
        self.tree.heading("FechaVencimiento", text="Fecha Vencimiento")
        self.tree.column("IdNit", width=100)
        self.tree.column("Codigo", width=100)
        self.tree.column("Nombre", width=150)
        self.tree.column("Medida", width=100)
        self.tree.column("Cantidad", width=100)
        self.tree.column("Precio", width=100)
        self.tree.column("FechaVencimiento", width=120)
        self.tree.bind('<Double-Button-1>', self.on_double_click)
        self.tree.grid(row=1, column=0, columnspan=2, padx=20, pady=10)

    def validate_id_nit(self, event):
        error_message = self.validator.validate_id_nit(self.id_nit.get())
        if error_message:
            mssg.showerror("Error", error_message)
            self.id_nit.focus_set()
            return False
        return True

    def validate_nombre_proveedor(self, event):
        error_message = self.validator.validate_nombre_proveedor(self.nombre_proveedor.get())
        if error_message:
            mssg.showerror("Error", error_message)
            self.nombre_proveedor.focus_set()
            return False
        return True

    def validate_fecha_compra(self, event):
        error_message = self.validator.validate_fecha_compra(self.fecha_compra.get())
        if error_message:
            mssg.showerror("Error", error_message)
            self.fecha_compra.focus_set()
            return False
        return True

    def validate_codigo(self, event):
        error_message = self.validator.validate_codigo(self.codigo.get())
        if error_message:
            mssg.showerror("Error", error_message)
            self.codigo.focus_set()
            return False
        return True

    def validate_nombre_producto(self, event):
        error_message = self.validator.validate_nombre_producto(self.nombre_producto.get())
        if error_message:
            mssg.showerror("Error", error_message)
            self.nombre_producto.focus_set()
            return False
        return True

    def validate_unidad(self, event):
        error_message = self.validator.validate_unidad(self.unidad.get())
        if error_message:
            mssg.showerror("Error", error_message)
            self.unidad.focus_set()
            return False
        return True

    def validate_cantidad(self, event):
        error_message = self.validator.validate_cantidad(self.cantidad.get())
        if error_message:
            mssg.showerror("Error", error_message)
            self.cantidad.focus_set()
            return False
        return True

    def validate_precio(self, event):
        error_message = self.validator.validate_precio(self.precio.get())
        if error_message:
            mssg.showerror("Error", error_message)
            self.precio.focus_set()
            return False
        return True

    def validate_fecha_vencimiento(self, event):
        error_message = self.validator.validate_fecha_vencimiento(self.fecha_vencimiento.get())
        if error_message:
            mssg.showerror("Error", error_message)
            self.fecha_vencimiento.focus_set()
            return False
        return True

    # Methods with the DataBase

    def add_producto(self):
        # Validate all input fields before proceeding
        if self.validate_all_fields():
            try:
                # Insert the provider into the database
                self.db.insert_proveedor(
                    self.id_nit.get(),
                    self.nombre_proveedor.get(),
                    self.fecha_compra.get()
                )
            except sqlite3.IntegrityError:
                # Provider already exists, so continue
                pass
            
            try:
                # Insert the product into the database
                self.db.insert_producto(
                    self.id_nit.get(),
                    self.codigo.get(),
                    self.nombre_producto.get(),
                    self.unidad.get(),
                    int(self.cantidad.get()),
                    float(self.precio.get()),
                    self.fecha_vencimiento.get()
                )
                # Show success message and refresh the product list
                mssg.showinfo("Éxito", "Producto agregado correctamente.")
                self.get_productos()
                self.clear_fields()
            except sqlite3.IntegrityError:
                # Product code already exists
                mssg.showerror("Error", "El código de producto ya existe.")

    def get_productos(self):
        # Clear existing items in the treeview
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        
        # Retrieve and display all products from the database
        for row in self.db.get_productos():
            self.tree.insert('', tk.END, values=row)

    def update_producto(self):
        # Validate all input fields before proceeding
        if self.validate_all_fields():
            # Search for the product by code
            producto = self.db.search_producto(self.codigo.get())
            if producto.fetchone():
                # Update the product details in the database
                self.db.update_producto(
                    self.codigo.get(),
                    self.nombre_producto.get(),
                    self.unidad.get(),
                    int(self.cantidad.get()),
                    float(self.precio.get()),
                    self.fecha_vencimiento.get()
                )
                # Show success message and refresh the product list
                mssg.showinfo("Éxito", "Producto actualizado correctamente.")
                self.get_productos()
                self.clear_fields()
            else:
                # Product does not exist
                mssg.showerror("Error", "El producto no existe.")

    def delete_producto(self):
        # Retrieve the product code from the input field
        codigo = self.codigo.get()
        if codigo:
            # Search for the product by code
            producto = self.db.search_producto(codigo)
            if producto.fetchone():
                # Delete the product from the database
                self.db.delete_producto(codigo)
                # Show success message and refresh the product list
                mssg.showinfo("Éxito", "Producto eliminado correctamente.")
                self.get_productos()
                self.clear_fields()
            else:
                # Product does not exist
                mssg.showerror("Error", "El producto no existe.")
        else:
            # No product code provided
            mssg.showerror("Error", "Debe ingresar el código del producto a eliminar.")

    def on_double_click(self, event):
        # Get the selected item from the treeview
        selected_item = self.tree.selection()[0]
        values = self.tree.item(selected_item, 'values')
        
        # Clear the input fields
        self.clear_fields()
        
        # Populate input fields with selected item values
        self.id_nit.insert(0, values[0])
        self.codigo.insert(0, values[1])
        self.nombre_producto.insert(0, values[2])
        self.unidad.insert(0, values[3])
        self.cantidad.insert(0, values[4])
        self.precio.insert(0, values[5])
        self.fecha_vencimiento.insert(0, values[6])
        
        # Retrieve and display the provider details associated with the product
        proveedor = self.db.search_proveedor(values[0]).fetchone()
        if proveedor:
            self.nombre_proveedor.insert(0, proveedor[1])
            self.fecha_compra.insert(0, proveedor[2])

    def clear_fields(self):
        # Clear all input fields and set default values
        self.id_nit.delete(0, tk.END)
        self.nombre_proveedor.delete(0, tk.END)
        self.fecha_compra.delete(0, tk.END)
        self.fecha_compra.insert(0, 'dd/mm/yyyy')
        self.codigo.delete(0, tk.END)
        self.nombre_producto.delete(0, tk.END)
        self.unidad.delete(0, tk.END)
        self.cantidad.delete(0, tk.END)
        self.precio.delete(0, tk.END)
        self.fecha_vencimiento.delete(0, tk.END)
        self.fecha_vencimiento.insert(0, 'dd/mm/yyyy')

    def validate_all_fields(self):
        return (
            self.validate_id_nit(None) and
            self.validate_nombre_proveedor(None) and
            self.validate_fecha_compra(None) and
            self.validate_codigo(None) and
            self.validate_nombre_producto(None) and
            self.validate_unidad(None) and
            self.validate_cantidad(None) and
            self.validate_precio(None) and
            self.validate_fecha_vencimiento(None)
        )

if __name__ == '__main__':
    window = tk.Tk()
    app = MainWindow(window)
    window.mainloop()