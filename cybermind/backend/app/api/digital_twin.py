from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
import networkx as nx
from app.database.session import get_db
from app.models.entities import Asset, AssetRelationship, Vulnerability, Scenario

router = APIRouter(prefix="/digital-twin", tags=["Digital Twin"])

class ScenarioRequest(BaseModel):
    name: str = "Make API-01 Public"
    target_asset_name: str = "API-01"
    action: str = "EXPOSE_TO_INTERNET"  # EXPOSE_TO_INTERNET, DISABLE_MFA, INJECT_CVE

class ScenarioResponse(BaseModel):
    scenario_id: str
    name: str
    description: str
    before_metrics: Dict[str, Any]
    after_metrics: Dict[str, Any]
    delta: Dict[str, Any]
    new_attack_paths: List[Dict[str, Any]]
    attacker_perspective: str
    defender_recommendations: List[str]

@router.get("")
def get_digital_twin_topology(db: Session = Depends(get_db)):
    assets = db.query(Asset).all()
    relationships = db.query(AssetRelationship).all()
    vulns = db.query(Vulnerability).all()

    # Map vulnerabilities by asset
    vuln_map = {}
    for v in vulns:
        vuln_map.setdefault(v.asset_id, []).append({
            "cve_id": v.cve_id,
            "title": v.title,
            "severity": v.severity,
            "cvss": v.cvss_score
        })

    # Prepare React Flow nodes
    nodes = []
    # Grid layout coordinates
    pos_x = 100
    pos_y = 100
    for idx, a in enumerate(assets):
        nodes.append({
            "id": a.id,
            "data": {
                "label": a.name,
                "assetType": a.asset_type,
                "hostname": a.hostname,
                "ip": a.ip_address,
                "isInternetFacing": a.is_internet_facing,
                "criticality": a.criticality,
                "riskScore": a.risk_score,
                "technologies": a.technologies or [],
                "vulnerabilities": vuln_map.get(a.id, [])
            },
            "position": {"x": (idx % 4) * 260 + 50, "y": (idx // 4) * 180 + 50}
        })

    # Prepare React Flow edges
    edges = []
    for r in relationships:
        edges.append({
            "id": f"e-{r.source_asset_id}-{r.target_asset_id}",
            "source": r.source_asset_id,
            "target": r.target_asset_id,
            "label": f"{r.relationship_type} ({r.protocol}:{r.port})" if r.port else r.relationship_type,
            "animated": True if r.relationship_type == "CONNECTS_TO" else False
        })

    return {
        "nodes": nodes,
        "edges": edges,
        "summary": {
            "total_assets": len(assets),
            "internet_facing": len([a for a in assets if a.is_internet_facing]),
            "high_risk": len([a for a in assets if a.risk_score >= 7.0])
        }
    }

@router.post("/scenario", response_model=ScenarioResponse)
def simulate_scenario(req: ScenarioRequest, db: Session = Depends(get_db)):
    assets = db.query(Asset).all()
    relationships = db.query(AssetRelationship).all()

    target = db.query(Asset).filter(Asset.name == req.target_asset_name).first()
    if not target:
        raise HTTPException(status_code=404, detail=f"Asset {req.target_asset_name} not found.")

    # Calculate BEFORE state
    before_internet_facing = len([a for a in assets if a.is_internet_facing])
    before_high_risk = len([a for a in assets if a.risk_score >= 7.0])
    before_attack_surface = before_internet_facing * 10 + before_high_risk * 5

    # Simulate AFTER state in-memory (strictly non-destructive)
    after_internet_facing = before_internet_facing + 1
    after_high_risk = before_high_risk + 1
    after_attack_surface = after_internet_facing * 10 + after_high_risk * 5 + 8

    new_paths = [
        {
            "path_id": "SIM-PATH-NEW",
            "name": f"Direct Internet Access to {target.name} via Port 8080",
            "hops": ["Untrusted Internet (0.0.0.0/0)", f"{target.name} (FastAPI/Port 8080)", "DB-01 (Customer Data)"],
            "risk": "CRITICAL (8.9)",
            "mitre_techniques": ["T1190 - Exploit Public-Facing Application", "T1005 - Data from Local System"]
        }
    ]

    response_data = ScenarioResponse(
        scenario_id=f"SCENARIO-{req.target_asset_name}",
        name=req.name,
        description=f"Simulated what-if scenario: Exposing internal asset {req.target_asset_name} directly to the public internet.",
        before_metrics={
            "attack_surface_score": before_attack_surface,
            "internet_facing_count": before_internet_facing,
            "high_risk_assets": before_high_risk,
            "active_attack_paths": 3
        },
        after_metrics={
            "attack_surface_score": after_attack_surface,
            "internet_facing_count": after_internet_facing,
            "high_risk_assets": after_high_risk,
            "active_attack_paths": 4
        },
        delta={
            "attack_surface_increase": f"+{after_attack_surface - before_attack_surface} pts",
            "new_exposure_vectors": 1,
            "critical_path_added": True
        },
        new_attack_paths=new_paths,
        attacker_perspective=f"Adversary can bypass perimeter WAF on WEB-01 and directly probe {target.name} endpoints for unauthenticated object references (IDOR) and SQL injection into DB-01.",
        defender_recommendations=[
            "Do NOT expose API-01 directly to 0.0.0.0/0. Route all ingress traffic exclusively through an API Gateway with mTLS.",
            "Deploy Web Application Firewall (WAF) rate limiting and OAuth2 introspection.",
            "Isolate API-01 in private security group allowing egress only to specified database ports."
        ]
    )

    return response_data
