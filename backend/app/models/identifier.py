from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from app.database import Base


class Identifier(Base):
    __tablename__ = "identifiers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    actor_id = Column(UUID(as_uuid=True), ForeignKey("actors.id"))
    identifier_type = Column(String)
    value = Column(String, index=True)
    source_id = Column(UUID(as_uuid=True), ForeignKey("sources.id"), nullable=True)
    observed_at = Column(DateTime, default=datetime.utcnow)
