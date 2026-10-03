from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, ConfigDict
from app.database.session import get_db
from app.models.entities import Finding

router = APIRouter(prefix="/findings", tags=["Findings"])

class FindingCreate(BaseModel):
    title: str
    description: str
    severity: str = "MEDIUM"
    confidence: float = 0.9
    asset_id: Optional[str] = None
    mitre_technique: Optional[str] = None
    source: str = "Manual / Scan"
    remediation: Optional[str] = None

class FindingOut(FindingCreate):
    id: str
    status: str
    created_at: str

    model_config = ConfigDict(from_attributes=True)

@router.get("", response_model=List[dict])
def list_findings(db: Session = Depends(get_db)):
    findings = db.query(Finding).all()
    return [
        {
            "id": f.id,
            "title": f.title,
            "description": f.description,
            "severity": f.severity,
            "confidence": f.confidence,
            "asset_id": f.asset_id,
            "mitre_technique": f.mitre_technique,
            "source": f.source,
            "status": f.status,
            "remediation": f.remediation,
            "created_at": f.created_at.isoformat() if f.created_at else None
        }
        for f in findings
    ]

@router.post("", status_code=status.HTTP_201_CREATED)
def create_finding(finding_in: FindingCreate, db: Session = Depends(get_db)):
    finding = Finding(**finding_in.model_dump())
    db.add(finding)
    db.commit()
    db.refresh(finding)
    return {
        "id": finding.id,
        "title": finding.title,
        "severity": finding.severity,
        "status": finding.status
    }
