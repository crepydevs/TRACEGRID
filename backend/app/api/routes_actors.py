from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.actor import Actor

router = APIRouter()


@router.get("/{actor_id}")
def get_actor(actor_id: str, db: Session = Depends(get_db)):
    actor = db.query(Actor).filter(Actor.id == actor_id).first()
    return actor
