from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from app.database import Base


class Source(Base):
    __tablename__ = "sources"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    url = Column(String)
    source_type = Column(String)
    reliability = Column(String, default="unverified")
    last_crawled = Column(DateTime, default=datetime.utcnow)
