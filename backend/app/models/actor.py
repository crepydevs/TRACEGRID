from sqlalchemy import Column, String, Float, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from app.database import Base

class Actor(Base):
__tablename__ = "actors"
id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
primary_handle = Column(String, nullable=False, index=True)
category = Column(String)  
attribution_confidence = Column(Float, default=0.0)  
first_seen = Column(DateTime, default=datetime.utcnow)
last_scan_date = Column(DateTime, default=datetime.utcnow)
notes = Column(Text, nullable=True)