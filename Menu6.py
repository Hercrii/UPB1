import customtkinter as ctk
import sqlite3

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class Bicicleta:
    def __init__(self, serial, marca, color, modelo, referencia, llanta):
        self.serial = serial
        self.marca = marca
        self.color = color
        self.modelo = modelo
        self.referencia = referencia
        self.llanta = llanta

class GestionBicicletas:
    ventana_actual = None
    DB_NAME = "bicicletas.db"

    @staticmethod
    def conectar_db():
        return sqlite3.connect(GestionBicicletas.DB_NAME)

    @staticmethod
    def inicializar_db():
        conn = GestionBicicletas.conectar_db()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bicicletas (
                serial INTEGER PRIMARY KEY,
                marca TEXT NOT NULL,
                color TEXT NOT NULL,
                modelo INTEGER NOT NULL,
                referencia TEXT NOT NULL,
                llanta REAL NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    @staticmethod
    def cerrar_ventana_anterior():
        if GestionBicicletas.ventana_actual and GestionBicicletas.ventana_actual.winfo_exists():
            GestionBicicletas.ventana_actual.destroy()
        GestionBicicletas.ventana_actual = None

    @staticmethod
    def menu_principal():
        GestionBicicletas.cerrar_ventana_anterior()
        GestionBicicletas.ventana_actual = ctk.CTk()
        GestionBicicletas.ventana_actual.geometry("400x500")
        GestionBicicletas.ventana_actual.title("Menú Principal")

        ctk.CTkLabel(GestionBicicletas.ventana_actual, text="Gestión de Bicicletas", font=("Arial", 16)).pack(pady=10)

        ctk.CTkButton(GestionBicicletas.ventana_actual, text="Registrar bicicleta", command=GestionBicicletas.abrir_registro).pack(pady=5)
        ctk.CTkButton(GestionBicicletas.ventana_actual, text="Ver Bicicletas", command=GestionBicicletas.ver_bicicletas).pack(pady=5)
        ctk.CTkButton(GestionBicicletas.ventana_actual, text="Modificar Bicicleta", command=GestionBicicletas.modificar_bicicleta).pack(pady=5)
        ctk.CTkButton(GestionBicicletas.ventana_actual, text="Eliminar Bicicleta", command=GestionBicicletas.eliminar_bicicleta).pack(pady=5)
        ctk.CTkButton(GestionBicicletas.ventana_actual, text="Salir", command=GestionBicicletas.ventana_actual.quit).pack(pady=5)

        GestionBicicletas.ventana_actual.mainloop()

    @staticmethod
    def abrir_registro():
        GestionBicicletas.cerrar_ventana_anterior()
        registro_win = ctk.CTk()
        registro_win.geometry("400x500")
        registro_win.title("Registrar Bicicleta")
        GestionBicicletas.ventana_actual = registro_win

        ctk.CTkLabel(registro_win, text="Serial(Numero):").pack()
        entrada_serial = ctk.CTkEntry(registro_win)
        entrada_serial.pack()

        ctk.CTkLabel(registro_win, text="Marca:").pack()
        entrada_marca = ctk.CTkEntry(registro_win)
        entrada_marca.pack()

        ctk.CTkLabel(registro_win, text="Color:").pack()
        entrada_color = ctk.CTkEntry(registro_win)
        entrada_color.pack()

        ctk.CTkLabel(registro_win, text="Modelo (número):").pack()
        entrada_modelo = ctk.CTkEntry(registro_win)
        entrada_modelo.pack()

        ctk.CTkLabel(registro_win, text="Referencia(Nombre):").pack()
        entrada_referencia = ctk.CTkEntry(registro_win)
        entrada_referencia.pack()

        ctk.CTkLabel(registro_win, text="Tamaño de la Llanta (Decimal en cm):").pack()
        entrada_llanta = ctk.CTkEntry(registro_win)
        entrada_llanta.pack()

        mensaje_error = ctk.CTkLabel(registro_win, text="", text_color="red")
        mensaje_error.pack()

        def registrar():
            try:
                serial = int(entrada_serial.get().strip())
                modelo = int(entrada_modelo.get().strip())
                llanta = float(entrada_llanta.get().strip())
            except ValueError:
                mensaje_error.configure(text="Error: Serial y modelo deben ser enteros, llanta debe ser decimal.")
                return

            marca = entrada_marca.get().strip()
            color = entrada_color.get().strip()
            referencia = entrada_referencia.get().strip()

            if not (marca and color and referencia):
                mensaje_error.configure(text="Todos los campos son obligatorios.")
                return

            try:
                conn = GestionBicicletas.conectar_db()
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO bicicletas (serial, marca, color, modelo, referencia, llanta)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (serial, marca, color, modelo, referencia, llanta))
                conn.commit()
                conn.close()
                GestionBicicletas.cerrar_ventana_anterior()
                GestionBicicletas.menu_principal()
            except sqlite3.IntegrityError:
                mensaje_error.configure(text="Error: El serial ya existe.")

        ctk.CTkButton(registro_win, text="Guardar", command=registrar).pack(pady=10)
        registro_win.mainloop()

    @staticmethod
    def ver_bicicletas():
        GestionBicicletas.cerrar_ventana_anterior()
        ver_win = ctk.CTk()
        ver_win.geometry("500x400")
        ver_win.title("Bicicletas Registradas")
        GestionBicicletas.ventana_actual = ver_win

        conn = GestionBicicletas.conectar_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM bicicletas")
        bicicletas = cursor.fetchall()
        conn.close()

        if not bicicletas:
            ctk.CTkLabel(ver_win, text="No hay bicicletas registradas.", text_color="red").pack(pady=10)
        else:
            for bici in bicicletas:
                info = f"- Serial: {bici[0]}\n - Marca: {bici[1]}\n - Color: {bici[2]}\n - Modelo: {bici[3]}\n - Referencia: {bici[4]}\n - Llanta: {bici[5]}"
                ctk.CTkLabel(ver_win, text=info).pack()

        ctk.CTkButton(ver_win, text="Volver", command=GestionBicicletas.menu_principal).pack(pady=10)
        ver_win.mainloop()

    @staticmethod
    def modificar_bicicleta():
        GestionBicicletas.cerrar_ventana_anterior()
        mod_win = ctk.CTk()
        mod_win.geometry("400x300")
        mod_win.title("Modificar Bicicleta")
        GestionBicicletas.ventana_actual = mod_win

        ctk.CTkLabel(mod_win, text="Ingrese el serial de la bicicleta:").pack()
        entrada_serial = ctk.CTkEntry(mod_win)
        entrada_serial.pack()
        mensaje_error = ctk.CTkLabel(mod_win, text="", text_color="red")
        mensaje_error.pack()

        def modificar():
            try:
                serial = int(entrada_serial.get().strip())
            except ValueError:
                mensaje_error.configure(text="El serial debe ser un número entero.")
                return

            conn = GestionBicicletas.conectar_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM bicicletas WHERE serial = ?", (serial,))
            bicicleta = cursor.fetchone()
            conn.close()

            if not bicicleta:
                mensaje_error.configure(text="Bicicleta no encontrada.")
                return

            opciones = ["marca", "color", "modelo", "referencia", "llanta"]
            variable = ctk.StringVar(value=opciones[0])
            ctk.CTkLabel(mod_win, text="Seleccionar campo a modificar:").pack()
            dropdown = ctk.CTkComboBox(mod_win, values=[o.capitalize() for o in opciones], variable=variable)
            dropdown.pack()

            ctk.CTkLabel(mod_win, text="Nuevo valor:").pack()
            nueva_entrada = ctk.CTkEntry(mod_win)
            nueva_entrada.pack()

            def guardar_cambio():
                nuevo_valor = nueva_entrada.get().strip()
                if not nuevo_valor:
                    mensaje_error.configure(text="El valor no puede estar vacío")
                    return

                try:
                    if variable.get().lower() == "modelo":
                        nuevo_valor = int(nuevo_valor)
                    elif variable.get().lower() == "llanta":
                        nuevo_valor = float(nuevo_valor)

                    conn = GestionBicicletas.conectar_db()
                    cursor = conn.cursor()
                    cursor.execute(f"UPDATE bicicletas SET {variable.get().lower()} = ? WHERE serial = ?", (nuevo_valor, serial))
                    conn.commit()
                    conn.close()
                    GestionBicicletas.menu_principal()
                except ValueError:
                    mensaje_error.configure(text="Error: Formato incorrecto para el campo seleccionado.")
                except sqlite3.Error as e:
                    mensaje_error.configure(text=f"Error en la base de datos: {e}")

            ctk.CTkButton(mod_win, text="Guardar", command=guardar_cambio).pack()

        ctk.CTkButton(mod_win, text="Buscar", command=modificar).pack(pady=5)
        mod_win.mainloop()

    @staticmethod
    def eliminar_bicicleta():
        GestionBicicletas.cerrar_ventana_anterior()
        elim_win = ctk.CTk()
        elim_win.geometry("400x300")
        elim_win.title("Eliminar Bicicleta")
        GestionBicicletas.ventana_actual = elim_win

        ctk.CTkLabel(elim_win, text="Ingrese el serial de la bicicleta a eliminar:").pack()
        entrada_serial = ctk.CTkEntry(elim_win)
        entrada_serial.pack()
        mensaje_error = ctk.CTkLabel(elim_win, text="", text_color="red")
        mensaje_error.pack()

        def eliminar():
            try:
                serial = int(entrada_serial.get().strip())
            except ValueError:
                mensaje_error.configure(text="El serial debe ser un número entero.")
                return

            conn = GestionBicicletas.conectar_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM bicicletas WHERE serial = ?", (serial,))
            bicicleta = cursor.fetchone()

            if not bicicleta:
                mensaje_error.configure(text="Bicicleta no encontrada.")
                conn.close()
                return

            # Confirmación
            confirmacion = ctk.CTk()
            confirmacion.geometry("300x200")
            confirmacion.title("Confirmar Eliminación")
            
            ctk.CTkLabel(confirmacion, text=f"¿Eliminar bicicleta con serial {serial}?").pack(pady=10)
            
            def confirmar_eliminar():
                cursor.execute("DELETE FROM bicicletas WHERE serial = ?", (serial,))
                conn.commit()
                conn.close()
                confirmacion.destroy()
                GestionBicicletas.menu_principal()

            ctk.CTkButton(confirmacion, text="Sí", command=confirmar_eliminar).pack(pady=5)
            ctk.CTkButton(confirmacion, text="No", command=confirmacion.destroy).pack(pady=5)
            confirmacion.mainloop()

        ctk.CTkButton(elim_win, text="Buscar", command=eliminar).pack(pady=10)
        ctk.CTkButton(elim_win, text="Volver", command=GestionBicicletas.menu_principal).pack(pady=5)
        elim_win.mainloop()

if __name__ == "__main__":
    GestionBicicletas.inicializar_db()  # Crear la tabla al iniciar
    GestionBicicletas.menu_principal()    