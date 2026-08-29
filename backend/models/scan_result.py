from sqlalchemy import Column, String, DateTime, Text, Float
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from app.database import Base

class ScanResult(Base):
__tablename__ = "scan_results"
id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
onion_address = Column(String, index=True)
finding_type = Column(String)  
matched_clearnet_target = Column(String, nullable=True)
confidence = Column(Float, default=0.0)
raw_evidence = Column(Text)
scanned_at = Column(DateTime, default=datetime.utcnow)