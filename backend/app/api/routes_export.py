import csv
import io
import json
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.actor import Actor

router = APIRouter()


@router.get("/csv")
def export_csv(db: Session = Depends(get_db)):
    actors = db.query(Actor).all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["handle", "category", "confidence", "last_scan_date"])
    for a in actors:
        writer.writerow([a.primary_handle, a.category, a.attribution_confidence, a.last_scan_date])
    output.seek(0)
    return StreamingResponse(output, media_type="text/csv")


@router.get("/json")
def export_json(db: Session = Depends(get_db)):
    actors = db.query(Actor).all()
    data = [
        {
            "handle": a.primary_handle,
            "category": a.category,
            "confidence": a.attribution_confidence,
            "last_scan_date": str(a.last_scan_date),
        }
        for a in actors
    ]
    return json.loads(json.dumps(data))
