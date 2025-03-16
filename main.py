from database import Database
from gui import GestionBicicletas

if __name__ == "__main__":
    Database.inicializar_db()
    GestionBicicletas.menu_principal()