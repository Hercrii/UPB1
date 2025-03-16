import sqlite3
from datetime import datetime

class Database:
    DB_NAME = "bicicletas.db"

    @staticmethod
    def conectar_db():
        return sqlite3.connect(Database.DB_NAME)

    @staticmethod
    def inicializar_db():
        conn = Database.conectar_db()
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