import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_seeded_assets():
    resp = client.get("/api/assets")
    assert resp.status_code == 200
    assets = resp.json()
    assert len(assets) >= 8
    names = [a["name"] for a in assets]
    assert "WEB-01" in names
    assert "API-01" in names
    assert "DB-01" in names
    assert "AWS-S3-01" in names

def test_findings_and_incidents():
    f_resp = client.get("/api/findings")
    assert f_resp.status_code == 200
    findings = f_resp.json()
    assert len(findings) >= 2

    i_resp = client.get("/api/incidents")
    assert i_resp.status_code == 200
    incidents = i_resp.json()
    assert len(incidents) >= 1
    assert "INC-2026-001" in incidents[0]["title"]

def test_digital_twin_topology_and_scenario():
    # 1. Topology
    top_resp = client.get("/api/digital-twin")
    assert top_resp.status_code == 200
    data = top_resp.json()
    assert "nodes" in data
    assert "edges" in data
    assert len(data["nodes"]) >= 8
    assert len(data["edges"]) >= 5

    # 2. Scenario Simulation
    sim_resp = client.post("/api/digital-twin/scenario", json={
        "name": "Make API-01 Public",
        "target_asset_name": "API-01",
        "action": "EXPOSE_TO_INTERNET"
    })
    assert sim_resp.status_code == 200
    sim = sim_resp.json()
    assert sim["name"] == "Make API-01 Public"
    assert sim["after_metrics"]["attack_surface_score"] > sim["before_metrics"]["attack_surface_score"]
    assert len(sim["new_attack_paths"]) > 0
    assert len(sim["defender_recommendations"]) > 0

def test_attack_surface_and_paths():
    as_resp = client.get("/api/attack-surface")
    assert as_resp.status_code == 200
    as_data = as_resp.json()
    assert as_data["overall_attack_surface_index"] > 0
    assert len(as_data["internet_facing_assets"]) >= 2

    ap_resp = client.get("/api/attack-paths")
    assert ap_resp.status_code == 200
    paths = ap_resp.json()["paths"]
    assert len(paths) >= 3
    assert paths[0]["target"] == "DB-01 (Crown Jewel Database)"

def test_threat_intel():
    lookup = client.get("/api/threat-intel/198.51.100.88")
    assert lookup.status_code == 200
    data = lookup.json()
    assert data["verdict"] == "MALICIOUS"
    assert "APT29" in data["threat_actor"]

def test_cyber_memory():
    sum_resp = client.get("/api/cyber-memory/summary")
    assert sum_resp.status_code == 200
    summary = sum_resp.json()
    assert "episodic_memory" in summary
    assert "procedural_memory" in summary

    sim_resp = client.post("/api/cyber-memory/similar-incidents", json={
        "query": "Multiple failed auth login bursts on gateway"
    })
    assert sim_resp.status_code == 200
    match = sim_resp.json()
    assert len(match["matched_incidents"]) >= 1
    assert match["matched_incidents"][0]["similarity_score"] > 0.7

def test_evidence_provenance_and_verification():
    # 1. Create Evidence
    ev_create = client.post("/api/evidence", json={
        "name": "Nginx TLS Handshake Trace",
        "evidence_type": "LOG",
        "raw_content": "TLS 1.3 ClientHello from client 198.51.100.88 with cipher suite TLS_AES_256_GCM_SHA384",
        "description": "PCAP/Log export from WEB-01 ingress boundary"
    })
    assert ev_create.status_code == 201
    ev_data = ev_create.json()
    ev_id = ev_data["id"]
    assert ev_data["blockchain_status"] == "ANCHORED"
    assert ev_data["blockchain_tx_hash"].startswith("0x")

    # 2. Verify Evidence Integrity
    v_resp = client.post(f"/api/evidence/{ev_id}/verify")
    assert v_resp.status_code == 200
    v_data = v_resp.json()
    assert v_data["is_valid"] is True
    assert v_data["integrity_status"] == "INTEGRITY_VERIFIED"
    assert v_data["current_sha256"] == v_data["anchored_sha256"]

def test_security_report_generation():
    rep_resp = client.post("/api/reports/generate", json={
        "report_type": "Executive Security Report"
    })
    assert rep_resp.status_code == 200
    rep = rep_resp.json()
    assert "executive_summary" in rep
    assert "scope" in rep
    assert "mitre_mapping" in rep
    assert len(rep["recommendations"]) >= 5
