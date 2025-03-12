import customtkinter as ctk
import sqlite3
from tkinter import filedialog, messagebox
from datetime import datetime

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class Bicicleta:
    def __init__(self, serial, marca, color, modelo, referencia, llanta, tipo, estado):
        self.serial = serial
        self.marca = marca
        self.color = color
        self.modelo = modelo
        self.referencia = referencia
        self.llanta = llanta
        self.tipo = tipo
        self.estado = estado

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
                llanta REAL NOT NULL,
                tipo TEXT,
                estado TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS historial (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                serial INTEGER,
                accion TEXT,
                fecha TEXT
            )
        ''')

        cursor.execute("SELECT COUNT(*) FROM bicicletas")
        if cursor.fetchone()[0] == 0:
            bicicletas_ejemplo = [
                (1001, "Trek", "Negro", 2023, "Marlin 5", 27.5, "Montaña", "Nueva"),
                (1002, "Specialized", "Rojo", 2022, "Rockhopper", 29.0, "Montaña", "Usada"),
                (1003, "Giant", "Azul", 2021, "Talon 1", 27.5, "Montaña", "Nueva"),
                (1004, "Cannondale", "Verde", 2023, "Trail 6", 29.0, "Montaña", "Nueva"),
                (1005, "Scott", "Blanco", 2022, "Aspect 950", 29.0, "Montaña", "En Reparación"),
                (1006, "Bianchi", "Gris", 2023, "Kuma 27.2", 27.5, "Montaña", "Nueva"),
                (1007, "Specialized", "Negro", 2021, "Sirrus 3.0", 28.0, "Urbana", "Usada"),
                (1008, "Trek", "Azul", 2022, "FX 2 Disc", 28.0, "Urbana", "Nueva"),
                (1009, "Giant", "Amarillo", 2023, "Escape 3", 28.0, "Urbana", "Nueva"),
                (1010, "Pinarello", "Negro", 2023, "Dogma F", 28.0, "Carretera", "Nueva"),
                (1011, "Cervélo", "Rojo", 2022, "R3", 28.0, "Carretera", "Usada"),
                (1012, "Cannondale", "Blanco", 2021, "SuperSix EVO", 28.0, "Carretera", "Nueva")
            ]
            cursor.executemany('''
                INSERT INTO bicicletas (serial, marca, color, modelo, referencia, llanta, tipo, estado)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', bicicletas_ejemplo)
            for bici in bicicletas_ejemplo:
                cursor.execute("INSERT INTO historial (serial, accion, fecha) VALUES (?, ?, ?)",
                               (bici[0], "Registro inicial", datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

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
        GestionBicicletas.ventana_actual.geometry("400x600")
        GestionBicicletas.ventana_actual.title("Menú Principal")

        ctk.CTkLabel(GestionBicicletas.ventana_actual, text="Gestión de Bicicletas", font=("Arial", 16)).pack(pady=10)

        ctk.CTkButton(GestionBicicletas.ventana_actual, text="Registrar bicicleta", command=GestionBicicletas.abrir_registro).pack(pady=5)
        ctk.CTkButton(GestionBicicletas.ventana_actual, text="Ver Bicicletas", command=GestionBicicletas.ver_bicicletas).pack(pady=5)
        ctk.CTkButton(GestionBicicletas.ventana_actual, text="Modificar Bicicleta", command=GestionBicicletas.modificar_bicicleta).pack(pady=5)
        ctk.CTkButton(GestionBicicletas.ventana_actual, text="Eliminar Bicicleta", command=GestionBicicletas.eliminar_bicicleta).pack(pady=5)
        ctk.CTkButton(GestionBicicletas.ventana_actual, text="Buscar Bicicletas", command=GestionBicicletas.buscar_bicicletas).pack(pady=5)
        ctk.CTkButton(GestionBicicletas.ventana_actual, text="Estadísticas", command=GestionBicicletas.mostrar_estadisticas).pack(pady=5)
        ctk.CTkButton(GestionBicicletas.ventana_actual, text="Ver Historial", command=GestionBicicletas.ver_historial).pack(pady=5)

        temas = ["dark", "light"]
        tema_var = ctk.StringVar(value="dark")
        ctk.CTkLabel(GestionBicicletas.ventana_actual, text="Tema:").pack(pady=5)
        ctk.CTkComboBox(GestionBicicletas.ventana_actual, values=temas, variable=tema_var, command=lambda x: ctk.set_appearance_mode(tema_var.get())).pack(pady=5)

        def confirmar_salida():
            confirmacion = ctk.CTkToplevel(GestionBicicletas.ventana_actual)
            confirmacion.geometry("300x150")
            confirmacion.title("Confirmar Salida")
            ctk.CTkLabel(confirmacion, text="¿Seguro que quieres salir?").pack(pady=10)
            ctk.CTkButton(confirmacion, text="Sí", command=GestionBicicletas.ventana_actual.quit).pack(pady=5)
            ctk.CTkButton(confirmacion, text="No", command=confirmacion.destroy).pack(pady=5)

        ctk.CTkButton(GestionBicicletas.ventana_actual, text="Salir", command=confirmar_salida).pack(pady=5)

        GestionBicicletas.ventana_actual.mainloop()

    @staticmethod
    def abrir_registro():
        GestionBicicletas.cerrar_ventana_anterior()
        registro_win = ctk.CTk()
        registro_win.geometry("400x500")
        registro_win.title("Registrar Bicicleta")
        GestionBicicletas.ventana_actual = registro_win

        scroll_frame = ctk.CTkScrollableFrame(registro_win, width=350, height=400)
        scroll_frame.pack(pady=10, fill="both", expand=True)

        def validar_serial(texto):
            if texto.isdigit() or texto == "":
                conn = GestionBicicletas.conectar_db()
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM bicicletas WHERE serial = ?", (texto,))
                existe = cursor.fetchone()[0] > 0
                conn.close()
                mensaje_error.configure(text="Serial ya existe" if existe and texto else "")
                return True
            mensaje_error.configure(text="Solo números enteros")
            return False

        def validar_modelo(texto):
            if texto.isdigit() or texto == "":
                mensaje_error.configure(text="")
                return True
            mensaje_error.configure(text="Solo números enteros")
            return False

        def validar_llanta(texto):
            try:
                if texto == "":
                    mensaje_error.configure(text="")
                    return True
                valor = float(texto)
                if 20 <= valor <= 30:
                    mensaje_error.configure(text="")
                    return True
                mensaje_error.configure(text="Llanta debe estar entre 20-30 cm")
                return False
            except ValueError:
                mensaje_error.configure(text="Solo números decimales")
                return False

        ctk.CTkLabel(scroll_frame, text="Serial(Numero):").pack(pady=5)
        entrada_serial = ctk.CTkEntry(scroll_frame, validate="key", validatecommand=(registro_win.register(validar_serial), '%P'))
        entrada_serial.pack(pady=5)

        ctk.CTkLabel(scroll_frame, text="Marca:").pack(pady=5)
        entrada_marca = ctk.CTkEntry(scroll_frame)
        entrada_marca.pack(pady=5)

        ctk.CTkLabel(scroll_frame, text="Color:").pack(pady=5)
        entrada_color = ctk.CTkEntry(scroll_frame)
        entrada_color.pack(pady=5)

        ctk.CTkLabel(scroll_frame, text="Modelo (número):").pack(pady=5)
        entrada_modelo = ctk.CTkEntry(scroll_frame, validate="key", validatecommand=(registro_win.register(validar_modelo), '%P'))
        entrada_modelo.pack(pady=5)

        ctk.CTkLabel(scroll_frame, text="Referencia(Nombre):").pack(pady=5)
        entrada_referencia = ctk.CTkEntry(scroll_frame)
        entrada_referencia.pack(pady=5)

        ctk.CTkLabel(scroll_frame, text="Tamaño de la Llanta (20-30 cm):").pack(pady=5)
        entrada_llanta = ctk.CTkEntry(scroll_frame, validate="key", validatecommand=(registro_win.register(validar_llanta), '%P'))
        entrada_llanta.pack(pady=5)

        ctk.CTkLabel(scroll_frame, text="Tipo:").pack(pady=5)
        tipos = ["Montaña", "Carretera", "Urbana"]
        entrada_tipo = ctk.CTkComboBox(scroll_frame, values=tipos)
        entrada_tipo.pack(pady=5)

        ctk.CTkLabel(scroll_frame, text="Estado:").pack(pady=5)
        estados = ["Nueva", "Usada", "En Reparación"]
        entrada_estado = ctk.CTkComboBox(scroll_frame, values=estados)
        entrada_estado.pack(pady=5)

        mensaje_error = ctk.CTkLabel(registro_win, text="", text_color="red")
        mensaje_error.pack(pady=5)

        def registrar():
            try:
                serial = int(entrada_serial.get().strip())
                modelo = int(entrada_modelo.get().strip())
                llanta = float(entrada_llanta.get().strip())
                if not (20 <= llanta <= 30):
                    raise ValueError("Llanta fuera de rango")
            except ValueError:
                mensaje_error.configure(text="Error: Verifique los campos numéricos.")
                return

            marca = entrada_marca.get().strip()
            color = entrada_color.get().strip()
            referencia = entrada_referencia.get().strip()
            tipo = entrada_tipo.get()
            estado = entrada_estado.get()

            if not (marca and color and referencia):
                mensaje_error.configure(text="Todos los campos son obligatorios.")
                return

            try:
                conn = GestionBicicletas.conectar_db()
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO bicicletas (serial, marca, color, modelo, referencia, llanta, tipo, estado)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (serial, marca, color, modelo, referencia, llanta, tipo, estado))
                cursor.execute("INSERT INTO historial (serial, accion, fecha) VALUES (?, ?, ?)",
                               (serial, "Registro", datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                conn.commit()
                conn.close()
                GestionBicicletas.cerrar_ventana_anterior()
                GestionBicicletas.menu_principal()
            except sqlite3.IntegrityError:
                mensaje_error.configure(text="Error: El serial ya existe.")

        ctk.CTkButton(registro_win, text="Guardar", command=registrar).pack(pady=5)
        ctk.CTkButton(registro_win, text="Volver", command=GestionBicicletas.menu_principal).pack(pady=5)
        registro_win.mainloop()

    @staticmethod
    def ver_bicicletas():
        GestionBicicletas.cerrar_ventana_anterior()
        ver_win = ctk.CTk()
        ver_win.geometry("600x600")
        ver_win.title("Bicicletas Registradas")
        GestionBicicletas.ventana_actual = ver_win

        ctk.CTkLabel(ver_win, text="Ordenar por:").pack(pady=5)
        ordenes = ["serial", "marca", "modelo"]
        orden_var = ctk.StringVar(value="serial")
        ctk.CTkComboBox(ver_win, values=[o.capitalize() for o in ordenes], variable=orden_var).pack(pady=5)

        scroll_frame = ctk.CTkScrollableFrame(ver_win, width=550, height=400)
        scroll_frame.pack(pady=10, fill="both", expand=True)

        ITEMS_POR_PAGINA = 5
        pagina_actual = 0

        def cargar_pagina():
            for widget in scroll_frame.winfo_children():
                widget.destroy()

            conn = GestionBicicletas.conectar_db()
            cursor = conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM bicicletas")
            total_items = cursor.fetchone()[0]
            total_paginas = (total_items + ITEMS_POR_PAGINA - 1) // ITEMS_POR_PAGINA

            offset = pagina_actual * ITEMS_POR_PAGINA
            cursor.execute(f"SELECT * FROM bicicletas ORDER BY {orden_var.get().lower()} LIMIT ? OFFSET ?", (ITEMS_POR_PAGINA, offset))
            bicicletas = cursor.fetchall()
            conn.close()

            if not bicicletas:
                ctk.CTkLabel(scroll_frame, text="No hay bicicletas registradas.", text_color="red").pack(pady=10)
            else:
                for bici in bicicletas:
                    frame = ctk.CTkFrame(scroll_frame)
                    frame.pack(pady=5, fill="x")
                    info = f"- Serial: {bici[0]}\n - Marca: {bici[1]}\n - Color: {bici[2]}\n - Modelo: {bici[3]}\n - Referencia: {bici[4]}\n - Llanta: {bici[5]}\n - Tipo: {bici[6]}\n - Estado: {bici[7]}"
                    ctk.CTkLabel(frame, text=info, anchor="w").pack(side="left", padx=10)

            btn_anterior.configure(state="normal" if pagina_actual > 0 else "disabled")
            btn_siguiente.configure(state="normal" if pagina_actual < total_paginas - 1 else "disabled")
            pagina_label.configure(text=f"Página {pagina_actual + 1} de {total_paginas}")

        def pagina_anterior():
            nonlocal pagina_actual
            if pagina_actual > 0:
                pagina_actual -= 1
                cargar_pagina()

        def pagina_siguiente():
            nonlocal pagina_actual
            conn = GestionBicicletas.conectar_db()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM bicicletas")
            total_items = cursor.fetchone()[0]
            conn.close()
            total_paginas = (total_items + ITEMS_POR_PAGINA - 1) // ITEMS_POR_PAGINA
            if pagina_actual < total_paginas - 1:
                pagina_actual += 1
                cargar_pagina()

        nav_frame = ctk.CTkFrame(ver_win)
        nav_frame.pack(pady=5)
        btn_anterior = ctk.CTkButton(nav_frame, text="Anterior", command=pagina_anterior)
        btn_anterior.pack(side="left", padx=5)
        pagina_label = ctk.CTkLabel(nav_frame, text="Página 1 de 1")
        pagina_label.pack(side="left", padx=5)
        btn_siguiente = ctk.CTkButton(nav_frame, text="Siguiente", command=pagina_siguiente)
        btn_siguiente.pack(side="left", padx=5)

        ctk.CTkButton(ver_win, text="Actualizar", command=cargar_pagina).pack(pady=5)
        cargar_pagina()
        ctk.CTkButton(ver_win, text="Volver", command=GestionBicicletas.menu_principal).pack(pady=5)
        ver_win.mainloop()

    @staticmethod
    def modificar_bicicleta():
        GestionBicicletas.cerrar_ventana_anterior()
        mod_win = ctk.CTk()
        mod_win.geometry("400x500")
        mod_win.title("Modificar Bicicleta")
        GestionBicicletas.ventana_actual = mod_win

        ctk.CTkLabel(mod_win, text="Ingrese el serial de la bicicleta:").pack(pady=5)
        entrada_serial = ctk.CTkEntry(mod_win)
        entrada_serial.pack(pady=5)
        mensaje_error = ctk.CTkLabel(mod_win, text="", text_color="red")
        mensaje_error.pack(pady=5)

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

            opciones = ["marca", "color", "modelo", "referencia", "llanta", "tipo", "estado"]
            variable = ctk.StringVar(value=opciones[0])
            ctk.CTkLabel(mod_win, text="Seleccionar campo a modificar:").pack(pady=5)
            dropdown = ctk.CTkComboBox(mod_win, values=[o.capitalize() for o in opciones], variable=variable)
            dropdown.pack(pady=5)

            ctk.CTkLabel(mod_win, text="Nuevo valor:").pack(pady=5)
            nueva_entrada = ctk.CTkEntry(mod_win)
            nueva_entrada.pack(pady=5)

            def guardar_cambio():
                campo = variable.get().lower()
                nuevo_valor = nueva_entrada.get().strip()
                if not nuevo_valor:
                    mensaje_error.configure(text="El valor no puede estar vacío")
                    return

                try:
                    if campo == "modelo":
                        nuevo_valor = int(nuevo_valor)
                    elif campo == "llanta":
                        nuevo_valor = float(nuevo_valor)
                        if not (20 <= nuevo_valor <= 30):
                            raise ValueError("Llanta fuera de rango")

                    conn = GestionBicicletas.conectar_db()
                    cursor = conn.cursor()
                    cursor.execute(f"UPDATE bicicletas SET {campo} = ? WHERE serial = ?", (nuevo_valor, serial))
                    cursor.execute("INSERT INTO historial (serial, accion, fecha) VALUES (?, ?, ?)",
                                   (serial, f"Modificación de {campo}", datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                    conn.commit()
                    conn.close()
                    GestionBicicletas.menu_principal()
                except ValueError:
                    mensaje_error.configure(text="Error: Formato incorrecto para el campo seleccionado.")
                except sqlite3.Error as e:
                    mensaje_error.configure(text=f"Error en la base de datos: {e}")

            ctk.CTkButton(mod_win, text="Guardar", command=guardar_cambio).pack(pady=5)

        ctk.CTkButton(mod_win, text="Buscar", command=modificar).pack(pady=5)
        ctk.CTkButton(mod_win, text="Volver", command=GestionBicicletas.menu_principal).pack(pady=5)
        mod_win.mainloop()

    @staticmethod
    def eliminar_bicicleta():
        GestionBicicletas.cerrar_ventana_anterior()
        elim_win = ctk.CTk()
        elim_win.geometry("400x300")
        elim_win.title("Eliminar Bicicleta")
        GestionBicicletas.ventana_actual = elim_win

        ctk.CTkLabel(elim_win, text="Ingrese el serial de la bicicleta a eliminar:").pack(pady=5)
        entrada_serial = ctk.CTkEntry(elim_win)
        entrada_serial.pack(pady=5)
        mensaje_error = ctk.CTkLabel(elim_win, text="", text_color="red")
        mensaje_error.pack(pady=5)

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

            confirmacion = ctk.CTkToplevel(elim_win)
            confirmacion.geometry("300x150")
            confirmacion.title("Confirmar Eliminación")
            ctk.CTkLabel(confirmacion, text=f"¿Eliminar bicicleta con serial {serial}?").pack(pady=10)
            
            def confirmar_eliminar():
                cursor.execute("DELETE FROM bicicletas WHERE serial = ?", (serial,))
                cursor.execute("INSERT INTO historial (serial, accion, fecha) VALUES (?, ?, ?)",
                               (serial, "Eliminación", datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                conn.commit()
                conn.close()
                confirmacion.destroy()
                GestionBicicletas.menu_principal()

            ctk.CTkButton(confirmacion, text="Sí", command=confirmar_eliminar).pack(pady=5)
            ctk.CTkButton(confirmacion, text="No", command=confirmacion.destroy).pack(pady=5)
            confirmacion.mainloop()

        ctk.CTkButton(elim_win, text="Buscar", command=eliminar).pack(pady=5)
        ctk.CTkButton(elim_win, text="Volver", command=GestionBicicletas.menu_principal).pack(pady=5)
        elim_win.mainloop()

    @staticmethod
    def buscar_bicicletas():
        GestionBicicletas.cerrar_ventana_anterior()
        buscar_win = ctk.CTk()
        buscar_win.geometry("400x500")
        buscar_win.title("Buscar Bicicletas")
        GestionBicicletas.ventana_actual = buscar_win

        ctk.CTkLabel(buscar_win, text="Marca:").pack(pady=5)
        entrada_marca = ctk.CTkEntry(buscar_win)
        entrada_marca.pack(pady=5)

        ctk.CTkLabel(buscar_win, text="Color:").pack(pady=5)
        entrada_color = ctk.CTkEntry(buscar_win)
        entrada_color.pack(pady=5)

        ctk.CTkLabel(buscar_win, text="Tipo:").pack(pady=5)
        entrada_tipo = ctk.CTkComboBox(buscar_win, values=["", "Montaña", "Carretera", "Urbana"])
        entrada_tipo.pack(pady=5)

        resultado_label = ctk.CTkLabel(buscar_win, text="")
        resultado_label.pack(pady=5)

        def buscar():
            marca = entrada_marca.get().strip()
            color = entrada_color.get().strip()
            tipo = entrada_tipo.get() if entrada_tipo.get() else None

            query = "SELECT * FROM bicicletas WHERE 1=1"
            params = []
            if marca:
                query += " AND marca LIKE ?"
                params.append(f"%{marca}%")
            if color:
                query += " AND color LIKE ?"
                params.append(f"%{color}%")
            if tipo:
                query += " AND tipo = ?"
                params.append(tipo)

            conn = GestionBicicletas.conectar_db()
            cursor = conn.cursor()
            cursor.execute(query, params)
            resultados = cursor.fetchall()
            conn.close()

            resultado_label.configure(text=f"Encontradas {len(resultados)} bicicletas")
            for widget in buscar_win.winfo_children()[8:]:
                widget.destroy()
            for bici in resultados:
                frame = ctk.CTkFrame(buscar_win)
                frame.pack(pady=5, fill="x")
                info = f"Serial: {bici[0]}, Marca: {bici[1]}, Color: {bici[2]}"
                ctk.CTkLabel(frame, text=info).pack()

        ctk.CTkButton(buscar_win, text="Buscar", command=buscar).pack(pady=5)
        ctk.CTkButton(buscar_win, text="Volver", command=GestionBicicletas.menu_principal).pack(pady=5)
        buscar_win.mainloop()

    @staticmethod
    def mostrar_estadisticas():
        GestionBicicletas.cerrar_ventana_anterior()
        stats_win = ctk.CTk()
        stats_win.geometry("400x400")
        stats_win.title("Estadísticas")
        GestionBicicletas.ventana_actual = stats_win

        conn = GestionBicicletas.conectar_db()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM bicicletas")
        total = cursor.fetchone()[0]
        cursor.execute("SELECT marca, COUNT(*) FROM bicicletas GROUP BY marca")
        marcas = cursor.fetchall()
        cursor.execute("SELECT AVG(llanta) FROM bicicletas")
        avg_llanta = cursor.fetchone()[0]
        conn.close()

        ctk.CTkLabel(stats_win, text=f"Total de bicicletas: {total}").pack(pady=5)
        ctk.CTkLabel(stats_win, text="Marcas más comunes:").pack(pady=5)
        for marca, count in marcas:
            ctk.CTkLabel(stats_win, text=f"{marca}: {count}").pack(pady=2)
        ctk.CTkLabel(stats_win, text=f"Promedio de llanta: {avg_llanta:.2f} cm").pack(pady=5)

        ctk.CTkButton(stats_win, text="Volver", command=GestionBicicletas.menu_principal).pack(pady=10)
        stats_win.mainloop()

    @staticmethod
    def ver_historial():
        GestionBicicletas.cerrar_ventana_anterior()
        hist_win = ctk.CTk()
        hist_win.geometry("600x600")
        hist_win.title("Historial de Cambios")
        GestionBicicletas.ventana_actual = hist_win

        scroll_frame = ctk.CTkScrollableFrame(hist_win, width=550, height=500)
        scroll_frame.pack(pady=10, fill="both", expand=True)

        conn = GestionBicicletas.conectar_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, serial, accion, fecha FROM historial ORDER BY fecha DESC")
        historial = cursor.fetchall()
        conn.close()

        if not historial:
            ctk.CTkLabel(scroll_frame, text="No hay registros en el historial.", text_color="red").pack(pady=10)
        else:
            for registro in historial:
                frame = ctk.CTkFrame(scroll_frame)
                frame.pack(pady=5, fill="x")
                info = f"ID: {registro[0]} - Serial: {registro[1]} - Acción: {registro[2]} - Fecha: {registro[3]}"
                ctk.CTkLabel(frame, text=info, anchor="w").pack(side="left", padx=10)

        ctk.CTkButton(hist_win, text="Volver", command=GestionBicicletas.menu_principal).pack(pady=5)
        hist_win.mainloop()

if __name__ == "__main__":
    GestionBicicletas.inicializar_db()
    GestionBicicletas.menu_principal()