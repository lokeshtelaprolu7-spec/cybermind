from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from pydantic import BaseModel
from app.database.session import get_db

router = APIRouter(prefix="/cyber-memory", tags=["Cyber Memory"])

class SimilarIncidentRequest(BaseModel):
    query: str = "Credential stuffing spikes on authentication service"

@router.get("/summary")
def get_memory_summary(db: Session = Depends(get_db)):
    return {
        "episodic_memory": {
            "total_incidents_recorded": 12,
            "last_incident": "INC-2026-001 (AUTH-01 Credential Spraying)",
            "average_dwell_time": "14 minutes"
        },
        "semantic_memory": {
            "critical_asset_inventory": 8,
            "monitored_subnets": ["198.51.100.0/24", "10.0.1.0/24", "10.0.2.0/24"],
            "crown_jewel_designation": "DB-01 Customer Database"
        },
        "procedural_memory": {
            "active_playbooks": [
                "PB-01: Autonomous Token Invalidation & Session Termination",
                "PB-02: Edge CIDR Rate-Limiting & WAF Blocklist Update",
                "PB-03: S3 Bucket ACL Audit & Public Access Enforcement",
                "PB-04: Emergency PostgreSQL Connection Drain & Snapshot"
            ]
        },
        "historical_memory": {
            "repeated_root_causes": ["Missing WAF on microservices", "Permissive S3 access policies"],
            "detection_gap_closures": "Closed 4 detection blindspots in Q3 2026"
        }
    }

@router.post("/similar-incidents")
def search_similar_incidents(req: SimilarIncidentRequest, db: Session = Depends(get_db)):
    return {
        "query": req.query,
        "matched_incidents": [
            {
                "incident_id": "INC-2025-089",
                "title": "Distributed Brute Force against VPN Gateway",
                "similarity_score": 0.89,
                "common_indicators": ["Failed login spikes", "Tor exit node IPs", "Credential spraying"],
                "common_techniques": ["T1110.004 - Credential Stuffing", "T1078 - Valid Accounts"],
                "proven_remediation": "Applied Cloudflare WAF bot management rules and rotated compromised user credentials.",
                "outcome": "Resolved with 0 unauthorized data exfiltration."
            },
            {
                "incident_id": "INC-2025-042",
                "title": "API Key Spraying on Staging Subdomain",
                "similarity_score": 0.74,
                "common_indicators": ["Rapid 401 Unauthorized bursts"],
                "common_techniques": ["T1110 - Brute Force"],
                "proven_remediation": "Rate limited key requests to 10 req/min and enforced IP allowlists.",
                "outcome": "Threat actor abandoned probe after 5 minutes."
            }
        ],
        "recommended_playbook": "PB-01: Autonomous Token Invalidation & Session Termination"
    }
