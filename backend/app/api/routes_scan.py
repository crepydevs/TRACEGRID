from fastapi import APIRouter
from pydantic import BaseModel
from app.services.infra_scanner import run_full_scan

router = APIRouter()


class ScanRequest(BaseModel):
    onion_address: str
    candidate_clearnet_domains: list[str] = []


@router.post("/infra")
def scan_infra(request: ScanRequest):
    findings = run_full_scan(request.onion_address, request.candidate_clearnet_domains)
    return {"onion_address": request.onion_address, "findings": findings}
