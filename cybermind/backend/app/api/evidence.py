import hashlib
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from app.database.session import get_db
from app.models.entities import Evidence

router = APIRouter(prefix="/evidence", tags=["Blockchain Evidence Provenance"])

class EvidenceCreate(BaseModel):
    name: str
    evidence_type: str = "LOG"  # LOG, SCAN, FILE, ARTIFACT
    raw_content: str
    description: Optional[str] = None
    investigation_id: Optional[str] = None

class VerifyResponse(BaseModel):
    evidence_id: str
    name: str
    current_sha256: str
    anchored_sha256: str
    blockchain_tx: Optional[str]
    integrity_status: str  # INTEGRITY_VERIFIED or INTEGRITY_MISMATCH
    is_valid: bool
    verified_at: str

@router.get("")
def list_evidence(db: Session = Depends(get_db)):
    evidence_list = db.query(Evidence).all()
    return [
        {
            "id": e.id,
            "name": e.name,
            "evidence_type": e.evidence_type,
            "description": e.description,
            "sha256_hash": e.sha256_hash,
            "blockchain_status": e.blockchain_status,
            "blockchain_tx_hash": e.blockchain_tx_hash,
            "provenance_chain": e.provenance_chain or [],
            "created_at": e.created_at.isoformat() if e.created_at else None
        }
        for e in evidence_list
    ]

@router.post("", status_code=status.HTTP_201_CREATED)
def create_and_anchor_evidence(ev_in: EvidenceCreate, db: Session = Depends(get_db)):
    # 1. Compute deterministic SHA-256 hash of raw evidence
    sha256_calc = hashlib.sha256(ev_in.raw_content.encode("utf-8")).hexdigest()
    now_iso = datetime.now(timezone.utc).isoformat()

    # 2. Local EVM / Merkle anchor simulation
    simulated_tx = f"0x{hashlib.sha256((sha256_calc + now_iso).encode('utf-8')).hexdigest()}"

    evidence = Evidence(
        name=ev_in.name,
        evidence_type=ev_in.evidence_type,
        raw_content=ev_in.raw_content,
        description=ev_in.description,
        investigation_id=ev_in.investigation_id,
        sha256_hash=sha256_calc,
        blockchain_status="ANCHORED",
        blockchain_tx_hash=simulated_tx,
        provenance_chain=[
            {"step": "Acquisition", "timestamp": now_iso, "actor": "Forensics Agent"},
            {"step": "SHA-256 Hashed", "timestamp": now_iso, "actor": "Evidence Engine"},
            {"step": "Blockchain Anchor", "timestamp": now_iso, "actor": "EVM Smart Contract"}
        ]
    )

    db.add(evidence)
    db.commit()
    db.refresh(evidence)

    return {
        "id": evidence.id,
        "name": evidence.name,
        "sha256_hash": evidence.sha256_hash,
        "blockchain_tx_hash": evidence.blockchain_tx_hash,
        "blockchain_status": evidence.blockchain_status
    }

@router.post("/{evidence_id}/verify", response_model=VerifyResponse)
def verify_evidence_integrity(evidence_id: str, db: Session = Depends(get_db)):
    evidence = db.query(Evidence).filter(Evidence.id == evidence_id).first()
    if not evidence:
        raise HTTPException(status_code=404, detail="Evidence not found.")

    # Recompute current SHA-256 from raw content
    current_hash = hashlib.sha256((evidence.raw_content or "").encode("utf-8")).hexdigest()
    now_iso = datetime.now(timezone.utc).isoformat()

    is_valid = (current_hash == evidence.sha256_hash)
    integrity_status = "INTEGRITY_VERIFIED" if is_valid else "INTEGRITY_MISMATCH"

    return VerifyResponse(
        evidence_id=evidence.id,
        name=evidence.name,
        current_sha256=current_hash,
        anchored_sha256=evidence.sha256_hash,
        blockchain_tx=evidence.blockchain_tx_hash,
        integrity_status=integrity_status,
        is_valid=is_valid,
        verified_at=now_iso
    )
