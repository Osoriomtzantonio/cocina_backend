from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from auth import get_current_user
import models
from pydantic import BaseModel

router = APIRouter(prefix="/calificaciones", tags=["Calificaciones"])


# ── SCHEMA ────────────────────────────────────────────────────────────
class CalificacionCrear(BaseModel):
    puntuacion: int  # 1 a 5


# ── GET /calificaciones/{receta_id} (público) ─────────────────────────
@router.get("/{receta_id}")
def obtener_calificacion(
    receta_id: int,
    db: Session = Depends(get_db),
    usuario = Depends(lambda: None),  # opcional — no fuerza login
):
    """
    Devuelve el promedio de calificaciones de una receta y el total de votos.
    No requiere autenticación.
    """
    resultado = db.query(
        func.avg(models.Calificacion.puntuacion).label("promedio"),
        func.count(models.Calificacion.id).label("total"),
    ).filter(models.Calificacion.receta_id == receta_id).first()

    promedio = round(float(resultado.promedio), 1) if resultado.promedio else 0.0
    total    = resultado.total or 0

    return {"promedio": promedio, "total": total}


# ── GET /calificaciones/{receta_id}/mia (requiere login) ─────────────
@router.get("/{receta_id}/mia")
def mi_calificacion(
    receta_id: int,
    db: Session = Depends(get_db),
    usuario = Depends(get_current_user),
):
    """Devuelve la calificación que el usuario actual dio a esta receta."""
    cal = db.query(models.Calificacion).filter(
        models.Calificacion.receta_id  == receta_id,
        models.Calificacion.usuario_id == usuario.id,
    ).first()

    return {"puntuacion": cal.puntuacion if cal else 0}


# ── POST /calificaciones/{receta_id} (requiere login) ─────────────────
@router.post("/{receta_id}")
def calificar_receta(
    receta_id: int,
    datos: CalificacionCrear,
    db: Session = Depends(get_db),
    usuario = Depends(get_current_user),
):
    """
    Califica una receta con 1-5 estrellas.
    Si el usuario ya la calificó antes, actualiza su calificación.
    """
    if not (1 <= datos.puntuacion <= 5):
        raise HTTPException(status_code=400, detail="La puntuación debe ser entre 1 y 5")

    receta = db.query(models.Receta).filter(models.Receta.id == receta_id).first()
    if not receta:
        raise HTTPException(status_code=404, detail="Receta no encontrada")

    # Buscar si ya existe una calificación de este usuario para esta receta
    cal_existente = db.query(models.Calificacion).filter(
        models.Calificacion.receta_id  == receta_id,
        models.Calificacion.usuario_id == usuario.id,
    ).first()

    if cal_existente:
        # Actualizar calificación existente
        cal_existente.puntuacion = datos.puntuacion
    else:
        # Crear nueva calificación
        nueva = models.Calificacion(
            usuario_id = usuario.id,
            receta_id  = receta_id,
            puntuacion = datos.puntuacion,
        )
        db.add(nueva)

    db.commit()

    # Recalcular promedio actualizado
    resultado = db.query(
        func.avg(models.Calificacion.puntuacion).label("promedio"),
        func.count(models.Calificacion.id).label("total"),
    ).filter(models.Calificacion.receta_id == receta_id).first()

    return {
        "mensaje":    "Calificación guardada",
        "puntuacion": datos.puntuacion,
        "promedio":   round(float(resultado.promedio), 1),
        "total":      resultado.total,
    }
