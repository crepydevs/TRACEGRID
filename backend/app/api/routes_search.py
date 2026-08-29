from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.actor import Actor

router = APIRouter()


@router.get("/")
def search_actors(
    handle: str = None,
    category: str = None,
    min_confidence: float = 0.0,
    db: Session = Depends(get_db),
):
    query = db.query(Actor)
    if handle:
        query = query.filter(Actor.primary_handle.ilike(f"%{handle}%"))
    if category:
        query = query.filter(Actor.category == category)
    query = query.filter(Actor.attribution_confidence >= min_confidence)
    return query.all()
