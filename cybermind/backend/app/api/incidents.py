from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, ConfigDict
from app.database.session import get_db
from app.models.entities import Incident

router = APIRouter(prefix="/incidents", tags=["Incidents"])

class IncidentCreate(BaseModel):
    title: str
    description: str
    severity: str = "HIGH"
    status: str = "OPEN"
    affected_assets: List[str] = []
    indicators: List[str] = []
    mitre_techniques: List[str] = []
    timeline: List[Dict[str, Any]] = []
    recommendations: List[str] = []

@router.get("", response_model=List[dict])
def list_incidents(db: Session = Depends(get_db)):
    incidents = db.query(Incident).all()
    return [
        {
            "id": inc.id,
            "title": inc.title,
            "description": inc.description,
            "severity": inc.severity,
            "status": inc.status,
            "affected_assets": inc.affected_assets,
            "indicators": inc.indicators,
            "mitre_techniques": inc.mitre_techniques,
            "timeline": inc.timeline,
            "recommendations": inc.recommendations,
            "created_at": inc.created_at.isoformat() if inc.created_at else None
        }
        for inc in incidents
    ]

@router.post("", status_code=status.HTTP_201_CREATED)
def create_incident(inc_in: IncidentCreate, db: Session = Depends(get_db)):
    incident = Incident(**inc_in.model_dump())
    db.add(incident)
    db.commit()
    db.refresh(incident)
    return {
        "id": incident.id,
        "title": incident.title,
        "status": incident.status
    }
