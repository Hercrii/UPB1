import customtkinter as ctk

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
    bicicletas = []
    ventana_actual = None

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

        ctk.CTkLabel(registro_win, text="Tamaño de la Llanta (Decimal en cm(Centimetros)):").pack()
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
                mensaje_error.configure(text="Error: Serial y modelo deben ser numeros enteros, llanta debe ser numero decimal.")
                return

            marca = entrada_marca.get().strip()
            color = entrada_color.get().strip()
            referencia = entrada_referencia.get().strip()

            if not (marca and color and referencia):
                mensaje_error.configure(text="Todos los campos son obligatorios.")
                return

            bicicleta = Bicicleta(serial, marca, color, modelo, referencia, llanta)
            GestionBicicletas.bicicletas.append(bicicleta)

            GestionBicicletas.cerrar_ventana_anterior()
            GestionBicicletas.menu_principal()

        ctk.CTkButton(registro_win, text="Guardar", command=registrar).pack(pady=10)
        registro_win.mainloop()

    @staticmethod
    def ver_bicicletas():
        GestionBicicletas.cerrar_ventana_anterior()
        ver_win = ctk.CTk()
        ver_win.geometry("500x400")
        ver_win.title("Bicicletas Registradas")
        GestionBicicletas.ventana_actual = ver_win

        if not GestionBicicletas.bicicletas:
            ctk.CTkLabel(ver_win, text="No hay bicicletas registradas.", text_color="red").pack(pady=10)
        else:
            for bicicleta in GestionBicicletas.bicicletas:
                info = f"- Serial{bicicleta.serial}\n - Marca: {bicicleta.marca}\n - Color: {bicicleta.color}\n - Modelo: {bicicleta.modelo}\n - Referencia: {bicicleta.referencia}\n - Llanta: {bicicleta.llanta}"
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

            bicicleta = next((b for b in GestionBicicletas.bicicletas if b.serial == serial), None)
            if not bicicleta:
                mensaje_error.configure(text="Bicicleta no encontrada.")
                return

            opciones = ["Marca", "Color", "Modelo", "Referencia", "Tamaño de la llanta"]
            variable = ctk.StringVar(value=opciones[0])
            ctk.CTkLabel(mod_win, text="Seleccionar campo a modificar:").pack()
            dropdown = ctk.CTkComboBox(mod_win, values=opciones, variable=variable)
            dropdown.pack()

            ctk.CTkLabel(mod_win, text="Nuevo valor:").pack()
            nueva_entrada = ctk.CTkEntry(mod_win)
            nueva_entrada.pack()

            def guardar_cambio():
                nuevo_valor = nueva_entrada.get().strip()
                if not nuevo_valor:
                    mensaje_error.configure(text="El valor no puede estar vacío")
                    return

                setattr(bicicleta, variable.get().lower(), nuevo_valor)
                GestionBicicletas.menu_principal()

            ctk.CTkButton(mod_win, text="Guardar", command=guardar_cambio).pack()

        ctk.CTkButton(mod_win, text="Buscar", command=modificar).pack(pady=5)
        mod_win.mainloop()

if __name__ == "__main__":
    GestionBicicletas.menu_principal()





