"""
update_imagenes.py — Actualiza la imagen_url de las recetas en la BD.
Ejecutar con: python update_imagenes.py
"""
from database import SessionLocal
import models

db = SessionLocal()

actualizaciones = [
    ("Tacos al Pastor",    "assets/images/recetas/tacos_al_pastor.jpg"),
    ("Guacamole Tradicional", "assets/images/recetas/guacamole.jpg"),
    ("Pozole Rojo",        "assets/images/recetas/pozole_rojo.jpg"),
    ("Enchiladas Rojas",   "assets/images/recetas/enchiladas_rojas.jpg"),
    ("Caldo de Camarón",   "assets/images/recetas/caldo_camaron.jpg"),
    ("Churros con Chocolate", "assets/images/recetas/churros.jpg"),
    ("Pollo en Mole",      "assets/images/recetas/pollo_mole.jpg"),
    ("Caldo de Pollo",     "assets/images/recetas/caldo_pollo.jpg"),
    ("Birria de Res",      "assets/images/recetas/birria.jpg"),
    ("Carne Asada",        "assets/images/recetas/carne_asada.jpg"),
    ("Milanesa de Res",    "assets/images/recetas/milanesa.jpg"),
    ("Chiles Rellenos",    "assets/images/recetas/chiles_rellenos.jpg"),
    ("Enfrijoladas",       "assets/images/recetas/enfrijoladas.jpg"),
    ("Camarones a la Diabla", "assets/images/recetas/camarones_diabla.jpg"),
    ("Aguachile de Camarón",  "assets/images/recetas/aguachile.jpg"),
    ("Sopa de Lima",       "assets/images/recetas/sopa_lima.jpg"),
    ("Caldo Tlalpeño",     "assets/images/recetas/caldo_tlalpeno.jpg"),
    ("Flan Napolitano",    "assets/images/recetas/flan.jpg"),
    ("Arroz con Leche",    "assets/images/recetas/arroz_leche.jpg"),
]

for nombre, imagen_url in actualizaciones:
    receta = db.query(models.Receta).filter(models.Receta.nombre == nombre).first()
    if receta:
        receta.imagen_url = imagen_url
        print(f"OK - {nombre}")
    else:
        print(f"NO ENCONTRADA - {nombre}")

db.commit()
db.close()
print("\nImágenes actualizadas.")
