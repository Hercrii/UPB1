import sqlite3
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from bicicleta import Bicicleta
from database import Database

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class GestionBicicletas:
    ventana_actual = None

    @staticmethod
    def cerrar_ventana_anterior():
        if GestionBicicletas.ventana_actual and GestionBicicletas.ventana_actual.winfo_exists():
            GestionBicicletas.ventana_actual.destroy()
        GestionBicicletas.ventana_actual = None

    @staticmethod
    def obtener_marcas():
        """Obtiene las marcas únicas de la base de datos."""
        conn = Database.conectar_db()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT marca FROM bicicletas ORDER BY marca")
        marcas = [row[0] for row in cursor.fetchall()]
        conn.close()
        return marcas

    @staticmethod
    def menu_principal():
        GestionBicicletas.cerrar_ventana_anterior()
        ventana = ctk.CTk()
        GestionBicicletas.ventana_actual = ventana
        ventana.geometry("400x600")
        ventana.title("Gestión de Bicicletas")

        ctk.CTkLabel(ventana, text="Gestión de Bicicletas", font=("Arial", 24, "bold"), text_color="#1f77b4").pack(pady=20)

        button_frame = ctk.CTkFrame(ventana)
        button_frame.pack(pady=10, padx=20, fill="x")

        ctk.CTkButton(button_frame, text="Registrar Bicicleta", command=GestionBicicletas.abrir_registro, font=("Arial", 14), corner_radius=10, height=40).pack(pady=10, fill="x")
        ctk.CTkButton(button_frame, text="Ver Bicicletas", command=GestionBicicletas.ver_bicicletas, font=("Arial", 14), corner_radius=10, height=40).pack(pady=10, fill="x")
        ctk.CTkButton(button_frame, text="Modificar Bicicleta", command=GestionBicicletas.modificar_bicicleta, font=("Arial", 14), corner_radius=10, height=40).pack(pady=10, fill="x")
        ctk.CTkButton(button_frame, text="Eliminar Bicicleta", command=GestionBicicletas.eliminar_bicicleta, font=("Arial", 14), corner_radius=10, height=40).pack(pady=10, fill="x")
        ctk.CTkButton(button_frame, text="Buscar Bicicletas", command=GestionBicicletas.buscar_bicicletas, font=("Arial", 14), corner_radius=10, height=40).pack(pady=10, fill="x")
        ctk.CTkButton(button_frame, text="Estadísticas", command=GestionBicicletas.mostrar_estadisticas, font=("Arial", 14), corner_radius=10, height=40).pack(pady=10, fill="x")
        ctk.CTkButton(button_frame, text="Ver Historial", command=GestionBicicletas.ver_historial, font=("Arial", 14), corner_radius=10, height=40).pack(pady=10, fill="x")

        tema_frame = ctk.CTkFrame(ventana)
        tema_frame.pack(pady=20, padx=20, fill="x")
        ctk.CTkLabel(tema_frame, text="Tema:", font=("Arial", 14)).pack(side="left", padx=5)
        temas = ["dark", "light"]
        tema_var = ctk.StringVar(value="dark")
        ctk.CTkComboBox(tema_frame, values=temas, variable=tema_var, command=lambda x: ctk.set_appearance_mode(tema_var.get()), width=100).pack(side="left")

        def confirmar_salida():
            confirmacion = ctk.CTkToplevel(ventana)
            confirmacion.geometry("300x150")
            confirmacion.title("Confirmar Salida")
            ctk.CTkLabel(confirmacion, text="¿Seguro que quieres salir?", font=("Arial", 14)).pack(pady=20)
            ctk.CTkButton(confirmacion, text="Sí", command=ventana.quit, width=80, fg_color="#d9534f").pack(side="left", padx=20, pady=10)
            ctk.CTkButton(confirmacion, text="No", command=confirmacion.destroy, width=80, fg_color="#5cb85c").pack(side="right", padx=20, pady=10)

        ctk.CTkButton(ventana, text="Salir", command=confirmar_salida, font=("Arial", 14), fg_color="#d9534f", corner_radius=10, height=40).pack(pady=20, padx=20, fill="x")

        ventana.mainloop()

    @staticmethod
    def abrir_registro():
        GestionBicicletas.cerrar_ventana_anterior()
        ventana = ctk.CTk()
        GestionBicicletas.ventana_actual = ventana
        ventana.geometry("400x600")
        ventana.title("Registrar Bicicleta")

        ctk.CTkLabel(ventana, text="Registrar Nueva Bicicleta", font=("Arial", 20, "bold"), text_color="#1f77b4").pack(pady=15)

        scroll_frame = ctk.CTkScrollableFrame(ventana, width=350, height=400)
        scroll_frame.pack(pady=10, padx=20, fill="both", expand=True)

        def validar_serial(texto):
            if texto == "" or texto.isdigit():
                conn = Database.conectar_db()
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM bicicletas WHERE serial = ?", (texto,))
                existe = cursor.fetchone()[0] > 0
                conn.close()
                if existe and texto:
                    mensaje_error.configure(text="Serial ya existe", text_color="red")
                else:
                    mensaje_error.configure(text="")
                return True
            mensaje_error.configure(text="Solo números enteros", text_color="red")
            return False

        def validar_modelo(texto):
            if texto == "" or texto.isdigit():
                mensaje_error.configure(text="")
                return True
            mensaje_error.configure(text="Solo números enteros", text_color="red")
            return False

        def validar_llanta(texto):
            if texto == "":
                mensaje_error.configure(text="")
                return True
            if texto.replace(".", "").isdigit() and texto.count(".") <= 1:
                try:
                    valor = float(texto)
                    if not (20 <= valor <= 30):
                        mensaje_error.configure(text="Fuera de rango (20-30 cm)", text_color="red")
                    else:
                        mensaje_error.configure(text="")
                    return True
                except ValueError:
                    mensaje_error.configure(text="")
                    return True
            mensaje_error.configure(text="Solo números o decimales", text_color="red")
            return False

        marcas = GestionBicicletas.obtener_marcas()
        if not marcas:
            marcas = ["Trek", "Specialized", "Giant"]  # Lista por defecto si la base de datos está vacía

        campos = [
            ("Serial (Número):", lambda: ctk.CTkEntry(master=scroll_frame, validate="key", validatecommand=(ventana.register(validar_serial), '%P'))),
            ("Marca:", lambda: ctk.CTkComboBox(master=scroll_frame, values=marcas)),
            ("Color:", lambda: ctk.CTkEntry(master=scroll_frame)),
            ("Modelo (Número):", lambda: ctk.CTkEntry(master=scroll_frame, validate="key", validatecommand=(ventana.register(validar_modelo), '%P'))),
            ("Referencia (Nombre):", lambda: ctk.CTkEntry(master=scroll_frame)),
            ("Tamaño de la Llanta (20-30 cm):", lambda: ctk.CTkEntry(master=scroll_frame, validate="key", validatecommand=(ventana.register(validar_llanta), '%P'))),
            ("Tipo:", lambda: ctk.CTkComboBox(master=scroll_frame, values=["Montaña", "Carretera", "Urbana"])),
            ("Estado:", lambda: ctk.CTkComboBox(master=scroll_frame, values=["Nueva", "Usada", "En Reparación"]))
        ]

        entradas = {}
        for i, (label_text, entry_func) in enumerate(campos):
            ctk.CTkLabel(scroll_frame, text=label_text, font=("Arial", 12)).grid(row=i, column=0, pady=5, padx=10, sticky="w")
            entrada = entry_func()
            entrada.grid(row=i, column=1, pady=5, padx=10, sticky="ew")
            entradas[label_text] = entrada

        scroll_frame.grid_columnconfigure(1, weight=1)

        mensaje_error = ctk.CTkLabel(ventana, text="", text_color="red", font=("Arial", 12))
        mensaje_error.pack(pady=10)

        def registrar():
            serial = entradas["Serial (Número):"].get().strip()
            marca = entradas["Marca:"].get().strip()
            color = entradas["Color:"].get().strip()
            modelo = entradas["Modelo (Número):"].get().strip()
            referencia = entradas["Referencia (Nombre):"].get().strip()
            llanta = entradas["Tamaño de la Llanta (20-30 cm):"].get().strip()
            tipo = entradas["Tipo:"].get()
            estado = entradas["Estado:"].get()

            if not serial or not marca or not color or not modelo or not referencia or not llanta:
                mensaje_error.configure(text="Todos los campos son obligatorios.", text_color="red")
                return

            try:
                serial = int(serial)
                modelo = int(modelo)
                llanta = float(llanta)
                if not (20 <= llanta <= 30):
                    mensaje_error.configure(text="Llanta debe estar entre 20 y 30 cm.", text_color="red")
                    return
            except ValueError:
                mensaje_error.configure(text="Serial y Modelo deben ser enteros, Llanta debe ser un número.", text_color="red")
                return

            try:
                conn = Database.conectar_db()
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO bicicletas (serial, marca, color, modelo, referencia, llanta, tipo, estado)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (serial, marca, color, modelo, referencia, llanta, tipo, estado))
                cursor.execute("INSERT INTO historial (serial, accion, fecha) VALUES (?, ?, ?)",
                               (serial, "Registro", datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                conn.commit()
                conn.close()
                mensaje_error.configure(text="Bicicleta registrada con éxito.", text_color="green")
                ventana.after(1000, GestionBicicletas.menu_principal)
            except sqlite3.IntegrityError:
                mensaje_error.configure(text="Error: El serial ya existe.", text_color="red")
            except Exception as e:
                mensaje_error.configure(text=f"Error inesperado: {e}", text_color="red")

        btn_frame = ctk.CTkFrame(ventana)
        btn_frame.pack(pady=10)
        ctk.CTkButton(btn_frame, text="Guardar", command=registrar, fg_color="#5cb85c", font=("Arial", 14), width=100).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Volver", command=GestionBicicletas.menu_principal, fg_color="#f0ad4e", font=("Arial", 14), width=100).pack(side="left", padx=10)

        ventana.mainloop()

    @staticmethod
    def modificar_bicicleta():
        GestionBicicletas.cerrar_ventana_anterior()
        ventana = ctk.CTk()
        GestionBicicletas.ventana_actual = ventana
        ventana.geometry("400x500")
        ventana.title("Modificar Bicicleta")

        ctk.CTkLabel(ventana, text="Modificar Bicicleta", font=("Arial", 20, "bold"), text_color="#1f77b4").pack(pady=15)

        ctk.CTkLabel(ventana, text="Ingrese el serial de la bicicleta:", font=("Arial", 12)).pack(pady=5, padx=20)
        entrada_serial = ctk.CTkEntry(ventana, width=200)
        entrada_serial.pack(pady=5, padx=20)
        mensaje_error = ctk.CTkLabel(ventana, text="", text_color="red", font=("Arial", 12))
        mensaje_error.pack(pady=10)

        def buscar_serial():
            serial = entrada_serial.get().strip()
            if not serial:
                mensaje_error.configure(text="Ingrese un serial.", text_color="red")
                return

            try:
                serial = int(serial)
            except ValueError:
                mensaje_error.configure(text="El serial debe ser un número entero.", text_color="red")
                return

            conn = Database.conectar_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM bicicletas WHERE serial = ?", (serial,))
            bicicleta = cursor.fetchone()
            conn.close()

            if not bicicleta:
                mensaje_error.configure(text="Bicicleta no encontrada.", text_color="red")
                return

            for widget in ventana.winfo_children()[3:]:
                widget.destroy()

            marcas = GestionBicicletas.obtener_marcas()
            opciones = ["marca", "color", "modelo", "referencia", "llanta", "tipo", "estado"]
            variable = ctk.StringVar(value=opciones[0])
            ctk.CTkLabel(ventana, text="Seleccionar campo a modificar:", font=("Arial", 12)).pack(pady=5, padx=20)
            dropdown = ctk.CTkComboBox(ventana, values=[o.capitalize() for o in opciones], variable=variable, width=200)
            dropdown.pack(pady=5, padx=20)

            ctk.CTkLabel(ventana, text="Nuevo valor:", font=("Arial", 12)).pack(pady=5, padx=20)
            nueva_entrada = ctk.CTkEntry(ventana, width=200)
            nueva_entrada.pack(pady=5, padx=20)

            # Mostrar ComboBox para "marca", "tipo" o "estado" según corresponda
            def actualizar_entrada(*args):
                campo = variable.get().lower()
                nueva_entrada.pack_forget()
                if campo == "marca":
                    nueva_entrada.configure(state="disabled")
                    combo_marca = ctk.CTkComboBox(ventana, values=marcas, width=200)
                    combo_marca.pack(pady=5, padx=20)
                    nueva_entrada = combo_marca
                elif campo == "tipo":
                    nueva_entrada.configure(state="disabled")
                    combo_tipo = ctk.CTkComboBox(ventana, values=["Montaña", "Carretera", "Urbana"], width=200)
                    combo_tipo.pack(pady=5, padx=20)
                    nueva_entrada = combo_tipo
                elif campo == "estado":
                    nueva_entrada.configure(state="disabled")
                    combo_estado = ctk.CTkComboBox(ventana, values=["Nueva", "Usada", "En Reparación"], width=200)
                    combo_estado.pack(pady=5, padx=20)
                    nueva_entrada = combo_estado
                else:
                    nueva_entrada.configure(state="normal")
                    nueva_entrada.pack(pady=5, padx=20)

            dropdown.configure(command=actualizar_entrada)
            actualizar_entrada()  # Inicializar con el campo seleccionado por defecto

            mensaje_error_mod = ctk.CTkLabel(ventana, text="", text_color="red", font=("Arial", 12))
            mensaje_error_mod.pack(pady=10)

            def guardar_cambio():
                campo = variable.get().lower()
                nuevo_valor = nueva_entrada.get().strip()
                if not nuevo_valor:
                    mensaje_error_mod.configure(text="El valor no puede estar vacío.", text_color="red")
                    return

                try:
                    if campo == "modelo":
                        nuevo_valor = int(nuevo_valor)
                    elif campo == "llanta":
                        nuevo_valor = float(nuevo_valor)
                        if not (20 <= nuevo_valor <= 30):
                            raise ValueError("Llanta debe estar entre 20 y 30 cm.")
                    elif campo == "tipo":
                        if nuevo_valor not in ["Montaña", "Carretera", "Urbana"]:
                            raise ValueError("Tipo inválido.")
                    elif campo == "estado":
                        if nuevo_valor not in ["Nueva", "Usada", "En Reparación"]:
                            raise ValueError("Estado inválido.")

                    conn = Database.conectar_db()
                    cursor = conn.cursor()
                    cursor.execute(f"UPDATE bicicletas SET {campo} = ? WHERE serial = ?", (nuevo_valor, serial))
                    cursor.execute("INSERT INTO historial (serial, accion, fecha) VALUES (?, ?, ?)",
                                   (serial, f"Modificación de {campo}", datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                    conn.commit()
                    conn.close()
                    mensaje_error_mod.configure(text="Modificación exitosa.", text_color="green")
                    ventana.after(1000, GestionBicicletas.menu_principal)
                except ValueError as e:
                    mensaje_error_mod.configure(text=str(e), text_color="red")
                except sqlite3.Error as e:
                    mensaje_error_mod.configure(text=f"Error en la base de datos: {e}", text_color="red")

            ctk.CTkButton(ventana, text="Guardar", command=guardar_cambio, fg_color="#5cb85c", font=("Arial", 14), width=100).pack(pady=10)
            ctk.CTkButton(ventana, text="Volver", command=GestionBicicletas.menu_principal, fg_color="#f0ad4e", font=("Arial", 14), width=100).pack(pady=10)

        ctk.CTkButton(ventana, text="Buscar", command=buscar_serial, fg_color="#5bc0de", font=("Arial", 14), width=100).pack(pady=5)
        ctk.CTkButton(ventana, text="Volver", command=GestionBicicletas.menu_principal, fg_color="#f0ad4e", font=("Arial", 14), width=100).pack(pady=10)

        ventana.mainloop()

    @staticmethod
    def ver_bicicletas():
        GestionBicicletas.cerrar_ventana_anterior()
        ventana = ctk.CTk()
        GestionBicicletas.ventana_actual = ventana
        ventana.geometry("600x600")
        ventana.title("Bicicletas Registradas")

        ctk.CTkLabel(ventana, text="Bicicletas Registradas", font=("Arial", 20, "bold"), text_color="#1f77b4").pack(pady=15)

        orden_frame = ctk.CTkFrame(ventana)
        orden_frame.pack(pady=5, padx=20, fill="x")
        ctk.CTkLabel(orden_frame, text="Ordenar por:", font=("Arial", 12)).pack(side="left", padx=5)
        ordenes = ["serial", "marca", "modelo"]
        orden_var = ctk.StringVar(value="serial")
        ctk.CTkComboBox(orden_frame, values=[o.capitalize() for o in ordenes], variable=orden_var, width=150).pack(side="left")

        scroll_frame = ctk.CTkScrollableFrame(ventana, width=550, height=400, fg_color="#2b2b2b")
        scroll_frame.pack(pady=10, padx=20, fill="both", expand=True)

        ITEMS_POR_PAGINA = 5
        pagina_actual = 0

        def cargar_pagina():
            for widget in scroll_frame.winfo_children():
                widget.destroy()

            conn = Database.conectar_db()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM bicicletas")
            total_items = cursor.fetchone()[0]
            total_paginas = (total_items + ITEMS_POR_PAGINA - 1) // ITEMS_POR_PAGINA

            offset = pagina_actual * ITEMS_POR_PAGINA
            cursor.execute(f"SELECT * FROM bicicletas ORDER BY {orden_var.get().lower()} LIMIT ? OFFSET ?", (ITEMS_POR_PAGINA, offset))
            bicicletas = cursor.fetchall()
            conn.close()

            if not bicicletas:
                ctk.CTkLabel(scroll_frame, text="No hay bicicletas registradas.", text_color="red", font=("Arial", 12)).pack(pady=10)
            else:
                for bici in bicicletas:
                    frame = ctk.CTkFrame(scroll_frame, fg_color="#3c3c3c", corner_radius=5)
                    frame.pack(pady=5, padx=5, fill="x")
                    info = f"Serial: {bici[0]} | Marca: {bici[1]} | Color: {bici[2]} | Modelo: {bici[3]} | Ref: {bici[4]} | Llanta: {bici[5]} | Tipo: {bici[6]} | Estado: {bici[7]}"
                    ctk.CTkLabel(frame, text=info, font=("Arial", 11), anchor="w").pack(padx=10, pady=5)

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
            conn = Database.conectar_db()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM bicicletas")
            total_items = cursor.fetchone()[0]
            conn.close()
            total_paginas = (total_items + ITEMS_POR_PAGINA - 1) // ITEMS_POR_PAGINA
            if pagina_actual < total_paginas - 1:
                pagina_actual += 1
                cargar_pagina()

        nav_frame = ctk.CTkFrame(ventana)
        nav_frame.pack(pady=10)
        btn_anterior = ctk.CTkButton(nav_frame, text="◄ Anterior", command=pagina_anterior, width=100, font=("Arial", 12))
        btn_anterior.pack(side="left", padx=5)
        pagina_label = ctk.CTkLabel(nav_frame, text="Página 1 de 1", font=("Arial", 12))
        pagina_label.pack(side="left", padx=10)
        btn_siguiente = ctk.CTkButton(nav_frame, text="Siguiente ►", command=pagina_siguiente, width=100, font=("Arial", 12))
        btn_siguiente.pack(side="left", padx=5)

        ctk.CTkButton(ventana, text="Actualizar", command=cargar_pagina, fg_color="#5bc0de", font=("Arial", 14), width=120).pack(pady=5)
        cargar_pagina()
        ctk.CTkButton(ventana, text="Volver", command=GestionBicicletas.menu_principal, fg_color="#f0ad4e", font=("Arial", 14), width=120).pack(pady=10)

        ventana.mainloop()

    @staticmethod
    def eliminar_bicicleta():
        GestionBicicletas.cerrar_ventana_anterior()
        ventana = ctk.CTk()
        GestionBicicletas.ventana_actual = ventana
        ventana.geometry("400x300")
        ventana.title("Eliminar Bicicleta")

        ctk.CTkLabel(ventana, text="Eliminar Bicicleta", font=("Arial", 20, "bold"), text_color="#1f77b4").pack(pady=15)

        ctk.CTkLabel(ventana, text="Ingrese el serial de la bicicleta a eliminar:", font=("Arial", 12)).pack(pady=5, padx=20)
        entrada_serial = ctk.CTkEntry(ventana, width=200)
        entrada_serial.pack(pady=5, padx=20)
        mensaje_error = ctk.CTkLabel(ventana, text="", text_color="red", font=("Arial", 12))
        mensaje_error.pack(pady=10)

        def eliminar():
            try:
                serial = int(entrada_serial.get().strip())
            except ValueError:
                mensaje_error.configure(text="El serial debe ser un número entero.", text_color="red")
                return

            conn = Database.conectar_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM bicicletas WHERE serial = ?", (serial,))
            bicicleta = cursor.fetchone()

            if not bicicleta:
                mensaje_error.configure(text="Bicicleta no encontrada.", text_color="red")
                conn.close()
                return

            confirmacion = ctk.CTkToplevel(ventana)
            confirmacion.geometry("300x150")
            confirmacion.title("Confirmar Eliminación")
            ctk.CTkLabel(confirmacion, text=f"¿Eliminar bicicleta con serial {serial}?", font=("Arial", 14)).pack(pady=20)
            
            def confirmar_eliminar():
                cursor.execute("DELETE FROM bicicletas WHERE serial = ?", (serial,))
                cursor.execute("INSERT INTO historial (serial, accion, fecha) VALUES (?, ?, ?)",
                               (serial, "Eliminación", datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                conn.commit()
                conn.close()
                confirmacion.destroy()
                mensaje_error.configure(text="Bicicleta eliminada.", text_color="green")
                ventana.after(1000, GestionBicicletas.menu_principal)

            ctk.CTkButton(confirmacion, text="Sí", command=confirmar_eliminar, fg_color="#d9534f", width=80).pack(side="left", padx=20, pady=10)
            ctk.CTkButton(confirmacion, text="No", command=confirmacion.destroy, fg_color="#5cb85c", width=80).pack(side="right", padx=20, pady=10)

        ctk.CTkButton(ventana, text="Buscar", command=eliminar, fg_color="#5bc0de", font=("Arial", 14), width=100).pack(pady=5)
        ctk.CTkButton(ventana, text="Volver", command=GestionBicicletas.menu_principal, fg_color="#f0ad4e", font=("Arial", 14), width=100).pack(pady=10)

        ventana.mainloop()

    @staticmethod
    def buscar_bicicletas():
        GestionBicicletas.cerrar_ventana_anterior()
        ventana = ctk.CTk()
        GestionBicicletas.ventana_actual = ventana
        ventana.geometry("400x500")
        ventana.title("Buscar Bicicletas")

        ctk.CTkLabel(ventana, text="Buscar Bicicletas", font=("Arial", 20, "bold"), text_color="#1f77b4").pack(pady=15)

        buscar_frame = ctk.CTkFrame(ventana)
        buscar_frame.pack(pady=10, padx=20, fill="x")
        marcas = GestionBicicletas.obtener_marcas()
        campos = [
            ("Marca:", lambda: ctk.CTkComboBox(master=buscar_frame, values=[""] + marcas, width=200)),
            ("Color:", lambda: ctk.CTkEntry(master=buscar_frame, width=200)),
            ("Tipo:", lambda: ctk.CTkComboBox(master=buscar_frame, values=["", "Montaña", "Carretera", "Urbana"]))
        ]
        entradas = {}
        for i, (label_text, entry_func) in enumerate(campos):
            ctk.CTkLabel(buscar_frame, text=label_text, font=("Arial", 12)).grid(row=i, column=0, pady=5, padx=10, sticky="w")
            entrada = entry_func()
            entrada.grid(row=i, column=1, pady=5, padx=10, sticky="ew")
            entradas[label_text] = entrada
        buscar_frame.grid_columnconfigure(1, weight=1)

        resultado_label = ctk.CTkLabel(ventana, text="", font=("Arial", 12))
        resultado_label.pack(pady=10)

        scroll_frame = ctk.CTkScrollableFrame(ventana, width=350, height=200)
        scroll_frame.pack(pady=10, padx=20, fill="both", expand=True)

        def buscar():
            marca = entradas["Marca:"].get().strip()
            color = entradas["Color:"].get().strip()
            tipo = entradas["Tipo:"].get() if entradas["Tipo:"].get() else None

            query = "SELECT * FROM bicicletas WHERE 1=1"
            params = []
            if marca:
                query += " AND marca = ?"
                params.append(marca)
            if color:
                query += " AND color LIKE ?"
                params.append(f"%{color}%")
            if tipo:
                query += " AND tipo = ?"
                params.append(tipo)

            conn = Database.conectar_db()
            cursor = conn.cursor()
            cursor.execute(query, params)
            resultados = cursor.fetchall()
            conn.close()

            for widget in scroll_frame.winfo_children():
                widget.destroy()

            resultado_label.configure(text=f"Encontradas {len(resultados)} bicicletas", text_color="green")
            if not resultados:
                ctk.CTkLabel(scroll_frame, text="No se encontraron bicicletas.", text_color="red", font=("Arial", 12)).pack(pady=10)
            else:
                for bici in resultados:
                    frame = ctk.CTkFrame(scroll_frame, fg_color="#3c3c3c", corner_radius=5)
                    frame.pack(pady=5, fill="x")
                    info = f"Serial: {bici[0]} | Marca: {bici[1]} | Color: {bici[2]}"
                    ctk.CTkLabel(frame, text=info, font=("Arial", 11)).pack(padx=10, pady=5)

        btn_frame = ctk.CTkFrame(ventana)
        btn_frame.pack(pady=10)
        ctk.CTkButton(btn_frame, text="Buscar", command=buscar, fg_color="#5bc0de", font=("Arial", 14), width=100).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Volver", command=GestionBicicletas.menu_principal, fg_color="#f0ad4e", font=("Arial", 14), width=100).pack(side="left", padx=10)

        ventana.mainloop()

    @staticmethod
    def mostrar_estadisticas():
        GestionBicicletas.cerrar_ventana_anterior()
        ventana = ctk.CTk()
        GestionBicicletas.ventana_actual = ventana
        ventana.geometry("400x400")
        ventana.title("Estadísticas")

        ctk.CTkLabel(ventana, text="Estadísticas", font=("Arial", 20, "bold"), text_color="#1f77b4").pack(pady=15)

        conn = Database.conectar_db()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM bicicletas")
        total = cursor.fetchone()[0]
        cursor.execute("SELECT marca, COUNT(*) FROM bicicletas GROUP BY marca")
        marcas = cursor.fetchall()
        cursor.execute("SELECT AVG(llanta) FROM bicicletas")
        avg_llanta = cursor.fetchone()[0]
        conn.close()

        stats_frame = ctk.CTkFrame(ventana, fg_color="#2b2b2b", corner_radius=10)
        stats_frame.pack(pady=10, padx=20, fill="both", expand=True)
        ctk.CTkLabel(stats_frame, text=f"Total de bicicletas: {total}", font=("Arial", 14)).pack(pady=10)
        ctk.CTkLabel(stats_frame, text="Marcas más comunes:", font=("Arial", 14)).pack(pady=5)
        for marca, count in marcas:
            ctk.CTkLabel(stats_frame, text=f"{marca}: {count}", font=("Arial", 12)).pack(pady=2)
        ctk.CTkLabel(stats_frame, text=f"Promedio de llanta: {avg_llanta:.2f} cm", font=("Arial", 14)).pack(pady=10)

        ctk.CTkButton(ventana, text="Volver", command=GestionBicicletas.menu_principal, fg_color="#f0ad4e", font=("Arial", 14), width=120).pack(pady=20)

        ventana.mainloop()

    @staticmethod
    def ver_historial():
        GestionBicicletas.cerrar_ventana_anterior()
        ventana = ctk.CTk()
        GestionBicicletas.ventana_actual = ventana
        ventana.geometry("600x600")
        ventana.title("Historial de Cambios")

        ctk.CTkLabel(ventana, text="Historial de Cambios", font=("Arial", 20, "bold"), text_color="#1f77b4").pack(pady=15)

        scroll_frame = ctk.CTkScrollableFrame(ventana, width=550, height=450, fg_color="#2b2b2b")
        scroll_frame.pack(pady=10, padx=20, fill="both", expand=True)

        conn = Database.conectar_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, serial, accion, fecha FROM historial ORDER BY fecha DESC")
        historial = cursor.fetchall()
        conn.close()

        if not historial:
            ctk.CTkLabel(scroll_frame, text="No hay registros en el historial.", text_color="red", font=("Arial", 12)).pack(pady=10)
        else:
            for registro in historial:
                frame = ctk.CTkFrame(scroll_frame, fg_color="#3c3c3c", corner_radius=5)
                frame.pack(pady=5, padx=5, fill="x")
                info = f"ID: {registro[0]} | Serial: {registro[1]} | Acción: {registro[2]} | Fecha: {registro[3]}"
                ctk.CTkLabel(frame, text=info, font=("Arial", 11), anchor="w").pack(padx=10, pady=5)

        ctk.CTkButton(ventana, text="Volver", command=GestionBicicletas.menu_principal, fg_color="#f0ad4e", font=("Arial", 14), width=120).pack(pady=10)

        ventana.mainloop()
