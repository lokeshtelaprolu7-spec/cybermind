from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.database.session import get_db
from app.models.entities import Asset, AssetRelationship, Vulnerability

router = APIRouter(prefix="", tags=["Attack Surface & Paths"])

@router.get("/attack-surface")
def get_attack_surface(db: Session = Depends(get_db)):
    assets = db.query(Asset).all()
    vulns = db.query(Vulnerability).all()
    
    internet_facing = [a for a in assets if a.is_internet_facing]
    critical_vulns = [v for v in vulns if v.severity == "CRITICAL"]
    high_vulns = [v for v in vulns if v.severity == "HIGH"]

    score = len(internet_facing) * 15 + len(critical_vulns) * 10 + len(high_vulns) * 5

    return {
        "overall_attack_surface_index": score,
        "exposure_level": "ELEVATED" if score > 50 else "MODERATE",
        "internet_facing_assets": [
            {
                "id": a.id,
                "name": a.name,
                "ip": a.ip_address,
                "type": a.asset_type,
                "criticality": a.criticality,
                "risk_score": a.risk_score
            }
            for a in internet_facing
        ],
        "vulnerable_services": len(vulns),
        "critical_vulnerabilities": len(critical_vulns),
        "total_infrastructure_nodes": len(assets),
        "perimeter_controls": ["WAF on WEB-01", "WireGuard VPN Gateway", "TLS 1.3 Termination"]
    }

@router.get("/attack-paths")
def get_attack_paths(db: Session = Depends(get_db)):
    return {
        "paths": [
            {
                "id": "PATH-01",
                "name": "Perimeter Web Exploitation to Primary Database",
                "entry_point": "Internet (0.0.0.0/0)",
                "hops": ["Untrusted Ingress", "WEB-01 (198.51.100.10:443)", "APP-01 (10.0.1.60:80)", "DB-01 (10.0.2.30:5432)"],
                "target": "DB-01 (Crown Jewel Database)",
                "risk_score": 9.2,
                "severity": "CRITICAL",
                "techniques": ["T1190 - Exploit Public-Facing Application", "T1059 - Command and Scripting Interpreter"],
                "mitigation": "Isolate database in private VPC subnet with strict security groups and disable direct reverse proxy chaining."
            },
            {
                "id": "PATH-02",
                "name": "Bypassed API Gateway Direct Data Access",
                "entry_point": "Internal/External Route Leak",
                "hops": ["Network Ingress", "API-01 (10.0.1.20:8080)", "DB-01 (10.0.2.30:5432)"],
                "target": "DB-01 Customer PII",
                "risk_score": 7.8,
                "severity": "HIGH",
                "techniques": ["T1190 - Exploit Public-Facing Application", "T1078 - Valid Accounts"],
                "mitigation": "Enforce API authentication middleware and restrict ingress CIDRs."
            },
            {
                "id": "PATH-03",
                "name": "Compromised VPN Credential Lateral Access to Cloud S3 Backup",
                "entry_point": "VPN-01 (198.51.100.1)",
                "hops": ["VPN-01 (198.51.100.1)", "AUTH-01 (10.0.1.50:8443)", "AWS-S3-01 (Cloud Storage)"],
                "target": "AWS-S3-01 Backup Bucket",
                "risk_score": 7.1,
                "severity": "HIGH",
                "techniques": ["T1110 - Brute Force", "T1530 - Data from Cloud Storage Object"],
                "mitigation": "Enforce FIDO2 Hardware MFA on VPN and enforce IAM bucket policy least privilege."
            }
        ]
    }
