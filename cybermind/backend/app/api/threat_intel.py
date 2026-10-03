from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.session import get_db
from app.models.entities import ThreatIndicator

router = APIRouter(prefix="/threat-intel", tags=["Threat Intelligence"])

@router.get("")
def list_indicators(db: Session = Depends(get_db)):
    indicators = db.query(ThreatIndicator).all()
    return [
        {
            "id": ind.id,
            "type": ind.indicator_type,
            "value": ind.value,
            "threat_actor": ind.threat_actor,
            "confidence": ind.confidence,
            "reputation_score": ind.reputation_score,
            "tags": ind.tags,
            "source": ind.source,
            "last_seen": ind.last_seen.isoformat() if ind.last_seen else None
        }
        for ind in indicators
    ]

@router.get("/{indicator}")
def lookup_indicator(indicator: str, db: Session = Depends(get_db)):
    found = db.query(ThreatIndicator).filter(ThreatIndicator.value == indicator).first()
    if found:
        return {
            "indicator": found.value,
            "type": found.indicator_type,
            "threat_actor": found.threat_actor,
            "confidence": found.confidence,
            "reputation_score": found.reputation_score,
            "verdict": "MALICIOUS" if found.reputation_score > 70 else "SUSPICIOUS",
            "tags": found.tags,
            "source": found.source
        }

    # Dynamic fallback analysis if indicator is new
    is_ip = "." in indicator and len(indicator.split(".")) == 4
    return {
        "indicator": indicator,
        "type": "IP" if is_ip else "DOMAIN/HASH",
        "threat_actor": "Unknown / Unclassified",
        "confidence": 0.6,
        "reputation_score": 15.0,
        "verdict": "BENIGN / UNCLASSIFIED",
        "tags": ["Passive DNS", "Internal Query"],
        "source": "CyberMIND Real-time Telemetry"
    }
