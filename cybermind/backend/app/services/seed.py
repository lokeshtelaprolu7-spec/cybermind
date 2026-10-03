from sqlalchemy.orm import Session
from app.models.entities import (
    Organization, Asset, AssetRelationship, Vulnerability,
    SecurityControl, Finding, Incident, ThreatIndicator, Evidence,
    Document, DocumentChunk
)
from app.core.security import get_password_hash

def seed_demo_organization(db: Session):
    org = db.query(Organization).filter(Organization.name == "CyberMIND Demo Organization").first()
    if not org:
        org = Organization(
            name="CyberMIND Demo Organization",
            domain="cybermind.local",
            description="Autonomous cybersecurity digital twin synthetic demo organization"
        )
        db.add(org)
        db.commit()
        db.refresh(org)

    existing_assets_count = db.query(Asset).filter(Asset.organization_id == org.id).count()
    if existing_assets_count > 0:
        seed_knowledge_base(db)
        return

    # 2. Assets
    web01 = Asset(
        organization_id=org.id,
        name="WEB-01",
        asset_type="Application",
        ip_address="198.51.100.10",
        hostname="web.cybermind.local",
        environment="Production",
        is_internet_facing=True,
        criticality="HIGH",
        owner="Web Platform Team",
        technologies=["Nginx 1.24", "React 18", "Node.js"],
        risk_score=8.5
    )
    
    api01 = Asset(
        organization_id=org.id,
        name="API-01",
        asset_type="API",
        ip_address="10.0.1.20",
        hostname="api.internal.cybermind.local",
        environment="Production",
        is_internet_facing=False,
        criticality="HIGH",
        owner="Backend Engineering",
        technologies=["FastAPI", "Python 3.11", "Uvicorn"],
        risk_score=7.8
    )

    db01 = Asset(
        organization_id=org.id,
        name="DB-01",
        asset_type="Database",
        ip_address="10.0.2.30",
        hostname="db-primary.internal.cybermind.local",
        environment="Production",
        is_internet_facing=False,
        criticality="CRITICAL",
        owner="Data Platform",
        technologies=["PostgreSQL 16", "pgvector"],
        risk_score=9.2
    )

    auth01 = Asset(
        organization_id=org.id,
        name="AUTH-01",
        asset_type="Application",
        ip_address="10.0.1.50",
        hostname="auth.cybermind.local",
        environment="Production",
        is_internet_facing=False,
        criticality="HIGH",
        owner="IAM Team",
        technologies=["Keycloak", "OAuth2", "OIDC"],
        risk_score=7.0
    )

    app01 = Asset(
        organization_id=org.id,
        name="APP-01",
        asset_type="Application",
        ip_address="10.0.1.60",
        hostname="app-core.internal.cybermind.local",
        environment="Production",
        is_internet_facing=False,
        criticality="HIGH",
        owner="Core Ops",
        technologies=["Java 21", "Spring Boot"],
        risk_score=6.8
    )

    s301 = Asset(
        organization_id=org.id,
        name="AWS-S3-01",
        asset_type="Cloud Resource",
        ip_address="s3.us-east-1.amazonaws.com",
        hostname="cybermind-prod-backups",
        environment="Production",
        is_internet_facing=False,
        criticality="HIGH",
        owner="Cloud Infrastructure",
        technologies=["AWS S3", "KMS Encryption"],
        risk_score=6.2
    )

    container01 = Asset(
        organization_id=org.id,
        name="CONTAINER-01",
        asset_type="Container",
        ip_address="10.244.1.15",
        hostname="worker-node-pod-4a",
        environment="Production",
        is_internet_facing=False,
        criticality="MEDIUM",
        owner="DevOps",
        technologies=["Docker", "Kubernetes", "Alpine Linux"],
        risk_score=5.5
    )

    vpn01 = Asset(
        organization_id=org.id,
        name="VPN-01",
        asset_type="Network",
        ip_address="198.51.100.1",
        hostname="vpn.cybermind.local",
        environment="Production",
        is_internet_facing=True,
        criticality="CRITICAL",
        owner="Network Security",
        technologies=["WireGuard", "OpenVPN"],
        risk_score=8.0
    )

    assets = [web01, api01, db01, auth01, app01, s301, container01, vpn01]
    db.add_all(assets)
    db.commit()
    for a in assets:
        db.refresh(a)

    # 3. Asset Relationships (Graph Topology)
    relationships = [
        AssetRelationship(source_asset_id=web01.id, target_asset_id=app01.id, relationship_type="CONNECTS_TO", protocol="HTTPS", port=443),
        AssetRelationship(source_asset_id=app01.id, target_asset_id=api01.id, relationship_type="CONNECTS_TO", protocol="HTTP", port=8080),
        AssetRelationship(source_asset_id=api01.id, target_asset_id=db01.id, relationship_type="CONNECTS_TO", protocol="TCP", port=5432),
        AssetRelationship(source_asset_id=web01.id, target_asset_id=auth01.id, relationship_type="USES", protocol="HTTPS", port=8443),
        AssetRelationship(source_asset_id=auth01.id, target_asset_id=s301.id, relationship_type="HAS_ACCESS", protocol="HTTPS", port=443),
        AssetRelationship(source_asset_id=container01.id, target_asset_id=app01.id, relationship_type="RUNS", protocol="Internal", port=80),
        AssetRelationship(source_asset_id=vpn01.id, target_asset_id=auth01.id, relationship_type="CONNECTS_TO", protocol="UDP", port=1194),
    ]
    db.add_all(relationships)

    # 4. Vulnerabilities
    vulns = [
        Vulnerability(
            asset_id=web01.id,
            cve_id="CVE-2023-44487",
            title="HTTP/2 Rapid Reset Attack",
            severity="HIGH",
            cvss_score=7.5,
            exploit_available=True,
            remediation="Update Nginx reverse proxy to version 1.25.3 or apply stream limit configurations."
        ),
        Vulnerability(
            asset_id=api01.id,
            cve_id="CVE-2024-21626",
            title="Container RunC Privilege Boundary Escapes",
            severity="CRITICAL",
            cvss_score=8.6,
            exploit_available=True,
            remediation="Patch runc binary and restrict host file descriptor leaks."
        ),
        Vulnerability(
            asset_id=db01.id,
            cve_id="CVE-2024-0985",
            title="PostgreSQL Non-Owner Privilege Escalation in REFRESH MATERIALIZED VIEW",
            severity="HIGH",
            cvss_score=8.0,
            exploit_available=False,
            remediation="Upgrade PostgreSQL to version 16.2."
        )
    ]
    db.add_all(vulns)

    # 5. Security Findings
    findings = [
        Finding(
            title="Unauthenticated Internal API Endpoint Accessible via Reverse Proxy",
            description="API-01 path /api/v1/customers has no valid token verification requirement.",
            severity="CRITICAL",
            confidence=0.96,
            asset_id=api01.id,
            mitre_technique="T1190",
            source="VAPT Agent",
            remediation="Enforce OAuth2 Bearer token middleware on all API-01 routes."
        ),
        Finding(
            title="Potential Data Exfiltration via S3 Bucket Bucket Policy Permissiveness",
            description="AWS-S3-01 backup bucket allows Principal * Read without explicit IP restriction.",
            severity="HIGH",
            confidence=0.88,
            asset_id=s301.id,
            mitre_technique="T1530",
            source="Cloud Agent",
            remediation="Enable S3 Block Public Access and attach VPC Endpoint condition."
        )
    ]
    db.add_all(findings)

    # 6. Incident
    incident = Incident(
        title="INC-2026-001: Anomalous Lateral Traversal & Credential Spraying",
        description="Multiple failed login spikes detected on AUTH-01 followed by unauthorized query to API-01 customer endpoint.",
        severity="HIGH",
        status="INVESTIGATING",
        affected_assets=["AUTH-01", "API-01", "DB-01"],
        indicators=["198.51.100.88", "tor-exit-node-04.net", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"],
        mitre_techniques=["T1110.004", "T1078", "T1190"],
        timeline=[
            {"time": "2026-09-29 22:15:00 UTC", "event": "500 failed authentication events against AUTH-01"},
            {"time": "2026-09-29 22:17:30 UTC", "event": "Single successful login from anomalous IP 198.51.100.88"},
            {"time": "2026-09-29 22:20:10 UTC", "event": "Outbound probe request to API-01 /customers"}
        ],
        recommendations=[
            "Revoke active token session for compromised service account.",
            "Apply temporary perimeter block on source IP 198.51.100.88.",
            "Trigger automated database query log snapshot on DB-01."
        ]
    )
    db.add(incident)

    # 7. Threat Indicators
    indicators = [
        ThreatIndicator(
            indicator_type="IP",
            value="198.51.100.88",
            threat_actor="APT29 / Cozy Bear Affiliate",
            confidence=0.92,
            reputation_score=94.5,
            tags=["Brute Force", "Tor Exit", "Known Malicious"]
        ),
        ThreatIndicator(
            indicator_type="DOMAIN",
            value="c2-secure-gateway.xyz",
            threat_actor="Lazarus Group",
            confidence=0.85,
            reputation_score=89.0,
            tags=["Command and Control", "Phishing"]
        )
    ]
    db.add_all(indicators)

    # 8. Evidence
    evidence1 = Evidence(
        evidence_type="LOG",
        name="AUTH-01 Brute Force Audit Log",
        description="Syslog export showing 500+ failed Kerberos/OAuth attempts within 120s window.",
        raw_content="2026-09-29T22:15:00Z auth-01 keycloak: [WARN] Failed login user=admin ip=198.51.100.88 code=INVALID_CREDENTIALS\n2026-09-29T22:15:01Z auth-01 keycloak: [WARN] Failed login user=root ip=198.51.100.88",
        sha256_hash="5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",
        blockchain_status="ANCHORED",
        blockchain_tx_hash="0x7f9fad1c0d57a7af66d400452d6c9745a4a5893a4369a03f4a3be0bb9bb1a1bc",
        provenance_chain=[
            {"step": "Acquisition", "timestamp": "2026-09-29 22:25:00 UTC", "actor": "SOC Agent"},
            {"step": "Hashing (SHA-256)", "timestamp": "2026-09-29 22:25:02 UTC", "actor": "Evidence Engine"},
            {"step": "Blockchain Anchor", "timestamp": "2026-09-29 22:25:05 UTC", "actor": "EVM Anchor Provider"}
        ]
    )
    db.add(evidence1)

    db.commit()
    seed_knowledge_base(db)

def seed_knowledge_base(db: Session):
    if db.query(Document).count() > 0:
        return

    doc1 = Document(
        title="OWASP Top 10:2021 - A03: Injection",
        source="OWASP",
        domain="Web Security",
        url="https://owasp.org/Top10/A03_2021-Injection/",
        version="2021",
        content="SQL Injection (SQLi) is a critical web security vulnerability that allows an attacker to interfere with the queries that an application makes to its database. Attackers supply hostile data to manipulate interpreter commands. Countermeasures mandate the use of parameterized queries (prepared statements), object relational mapping (ORM), and strict input allowlists."
    )
    db.add(doc1)
    db.commit()
    db.refresh(doc1)

    chunk1 = DocumentChunk(
        document_id=doc1.id,
        chunk_index=0,
        chunk_text="SQL Injection occurs when untrusted user input is directly concatenated into SQL queries. Defense in depth requires prepared statements, parameterized queries, and least privilege service accounts.",
        metadata_json={"source": "OWASP", "domain": "Web Security", "title": doc1.title, "url": doc1.url}
    )
    db.add(chunk1)

    doc2 = Document(
        title="OWASP API Security Top 10:2023 - API3: Broken Object Property Level Authorization",
        source="OWASP",
        domain="API Security",
        url="https://owasp.org/API-Security/",
        version="2023",
        content="API exposure risks occur when internal endpoints like API-01 are routed without proper API gateway reverse proxies or OAuth2 validation. When endpoints bypass authorization layers, adversaries can access sensitive database schemas directly."
    )
    db.add(doc2)
    db.commit()
    db.refresh(doc2)

    chunk2 = DocumentChunk(
        document_id=doc2.id,
        chunk_index=0,
        chunk_text="Microservice API exposure directly onto public network CIDRs expands organizational attack surfaces. Mitigation mandates API Gateway mTLS reverse proxy, rate limiting, and schema validation.",
        metadata_json={"source": "OWASP", "domain": "API Security", "title": doc2.title, "url": doc2.url}
    )
    db.add(chunk2)

    doc3 = Document(
        title="MITRE ATT&CK T1110.004 - Credential Stuffing",
        source="MITRE ATT&CK",
        domain="SOC / Incident Response",
        url="https://attack.mitre.org/techniques/T1110/004/",
        version="v14.1",
        content="Credential Stuffing (T1110.004) involves automated authentication attempts against identity services (Keycloak, OAuth2). SOC triage relies on detecting abnormal authentication failure spikes (AUTH-4625), automated bot user-agents, and geographical velocity mismatches."
    )
    db.add(doc3)
    db.commit()
    db.refresh(doc3)

    chunk3 = DocumentChunk(
        document_id=doc3.id,
        chunk_index=0,
        chunk_text="T1110.004 detection involves correlation of repeated failed login attempts followed by anomalous lateral traversal. Mitigation requires Multi-Factor Authentication (MFA) and adaptive rate limiting.",
        metadata_json={"source": "MITRE ATT&CK", "domain": "SOC / Incident Response", "title": doc3.title, "url": doc3.url}
    )
    db.add(chunk3)

    doc4 = Document(
        title="MITRE ATT&CK T1190 - Exploit Public-Facing Application",
        source="MITRE ATT&CK",
        domain="Threat Intelligence",
        url="https://attack.mitre.org/techniques/T1190/",
        version="v14.1",
        content="Exploit Public-Facing Application (T1190) is used by adversaries to gain initial access via externally reachable services. Remediation requires network segmentation, DMZ isolation, and continuous vulnerability scanning."
    )
    db.add(doc4)
    db.commit()
    db.refresh(doc4)

    chunk4 = DocumentChunk(
        document_id=doc4.id,
        chunk_index=0,
        chunk_text="T1190 targets perimeter web servers and reverse proxies. Defenses include Web Application Firewalls (WAF), rapid patch management, and strict egress filtering.",
        metadata_json={"source": "MITRE ATT&CK", "domain": "Threat Intelligence", "title": doc4.title, "url": doc4.url}
    )
    db.add(chunk4)

    doc5 = Document(
        title="NIST Cybersecurity Framework (CSF 2.0) - Detect & Respond",
        source="NIST",
        domain="SOC",
        url="https://www.nist.gov/cyberframework",
        version="2.0",
        content="NIST CSF 2.0 Detect (DE) and Respond (RS) categories provide guidelines for autonomous incident containment, continuous baseline telemetry monitoring, and post-incident forensic evidence anchoring."
    )
    db.add(doc5)
    db.commit()
    db.refresh(doc5)

    chunk5 = DocumentChunk(
        document_id=doc5.id,
        chunk_index=0,
        chunk_text="NIST CSF 2.0 DE.CM requires continuous monitoring of organizational networks and physical perimeter assets to identify anomalies and suspicious events.",
        metadata_json={"source": "NIST", "domain": "SOC", "title": doc5.title, "url": doc5.url}
    )
    db.add(chunk5)

    db.commit()
