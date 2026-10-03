from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from datetime import datetime, timezone
from app.database.session import get_db
from app.models.entities import Asset, Finding, Incident, Evidence, Vulnerability

router = APIRouter(prefix="/reports", tags=["Reporting Engine"])

class ReportRequest(BaseModel):
    report_type: str = "Executive Security Report"  # Executive Security Report, Attack Surface Assessment, Incident Report, Digital Twin Audit
    title: Optional[str] = None

@router.post("/generate")
def generate_report(req: ReportRequest, db: Session = Depends(get_db)):
    assets = db.query(Asset).all()
    findings = db.query(Finding).all()
    incidents = db.query(Incident).all()
    vulns = db.query(Vulnerability).all()
    evidence_items = db.query(Evidence).all()

    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    report = {
        "title": req.title or f"{req.report_type} — CyberMIND Autonomous Assessment",
        "generated_at": now_str,
        "organization": "CyberMIND Demo Organization",
        "executive_summary": "Autonomous agentic investigation completed across 8 digital twin nodes. 2 perimeter assets identified directly exposed to the internet. 1 critical attack path discovered traversing from public ingress to core customer database. Immediate compensating controls and API gateway mTLS enforcement recommended.",
        "scope": {
            "monitored_assets": len(assets),
            "critical_vulnerabilities": len([v for v in vulns if v.severity == "CRITICAL"]),
            "open_findings": len(findings),
            "investigated_incidents": len(incidents)
        },
        "environment": {
            "critical_assets": ["WEB-01", "API-01", "DB-01", "AUTH-01", "AWS-S3-01"],
            "network_zones": ["Public Perimeter (198.51.100.0/24)", "Internal App Tier (10.0.1.0/24)", "Secure Data Tier (10.0.2.0/24)"]
        },
        "attack_surface": {
            "overall_index": 65,
            "status": "ELEVATED",
            "exposed_services": ["WEB-01 (443)", "VPN-01 (1194)"],
            "unprotected_endpoints": ["API-01 /customers (Simulated exposure candidate)"]
        },
        "key_findings": [
            {
                "title": f.title,
                "severity": f.severity,
                "confidence": f.confidence,
                "mitre": f.mitre_technique,
                "remediation": f.remediation
            }
            for f in findings
        ],
        "attack_paths": [
            {
                "path_id": "PATH-01",
                "entry": "Internet (0.0.0.0/0)",
                "hops": "Internet -> WEB-01 -> APP-01 -> DB-01",
                "risk": "9.2 CRITICAL",
                "impact": "Full database read/write access and customer PII exfiltration"
            }
        ],
        "evidence_integrity": [
            {
                "name": e.name,
                "sha256": e.sha256_hash,
                "blockchain_status": e.blockchain_status,
                "anchor_tx": e.blockchain_tx_hash
            }
            for e in evidence_items
        ],
        "mitre_mapping": [
            {"technique": "T1190", "name": "Exploit Public-Facing Application", "tactic": "Initial Access"},
            {"technique": "T1110.004", "name": "Credential Stuffing", "tactic": "Credential Access"},
            {"technique": "T1530", "name": "Data from Cloud Storage Object", "tactic": "Collection"}
        ],
        "recommendations": [
            "1. Deploy Web Application Firewall (WAF) rate limiting and DDoS mitigation across WEB-01.",
            "2. Enforce API Gateway reverse proxy with mTLS and OAuth2 Bearer token introspection for API-01.",
            "3. Enforce Multi-Factor Authentication (MFA) across all identity providers including AUTH-01 and VPN-01.",
            "4. Enable S3 Block Public Access on AWS-S3-01 backup bucket.",
            "5. Implement automated evidence anchoring for all high-severity incident logs."
        ],
        "sources": [
            "OWASP Top 10:2021",
            "OWASP API Security Top 10:2023",
            "MITRE ATT&CK Enterprise Matrix v14",
            "NIST Cybersecurity Framework (CSF 2.0)",
            "CIS Critical Security Controls v8"
        ],
        "limitations": "Assessment reflects snapshot of digital twin model. Automated validation recommended after applying compensating controls."
    }

    return report
