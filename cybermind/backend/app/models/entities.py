import uuid
from datetime import datetime, timezone
from sqlalchemy import (
    Column, String, Integer, Float, Boolean, DateTime, ForeignKey, Text, JSON
)
from sqlalchemy.orm import relationship
from app.database.session import Base

def generate_uuid():
    return str(uuid.uuid4())

def utc_now():
    return datetime.now(timezone.utc)

class User(Base):
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    role = Column(String(50), default="ANALYST", nullable=False)  # ADMIN, ANALYST, VIEWER
    is_active = Column(Boolean, default=True)
    organization_id = Column(String(36), ForeignKey("organizations.id"), nullable=True)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

    organization = relationship("Organization", back_populates="users")

class Organization(Base):
    __tablename__ = "organizations"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), unique=True, nullable=False)
    domain = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=utc_now)
    
    users = relationship("User", back_populates="organization")
    assets = relationship("Asset", back_populates="organization")

class Asset(Base):
    __tablename__ = "assets"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    organization_id = Column(String(36), ForeignKey("organizations.id"), nullable=True)
    name = Column(String(255), index=True, nullable=False)
    asset_type = Column(String(100), nullable=False)  # Server, Application, API, Database, Cloud Resource, Container, Network, Device
    ip_address = Column(String(100), nullable=True)
    hostname = Column(String(255), nullable=True)
    environment = Column(String(100), default="Production")  # Production, Staging, Development
    is_internet_facing = Column(Boolean, default=False)
    criticality = Column(String(50), default="MEDIUM")  # LOW, MEDIUM, HIGH, CRITICAL
    owner = Column(String(255), nullable=True)
    technologies = Column(JSON, default=list)  # ["nginx", "python", "postgresql"]
    properties = Column(JSON, default=dict)
    risk_score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

    organization = relationship("Organization", back_populates="assets")
    vulnerabilities = relationship("Vulnerability", back_populates="asset", cascade="all, delete-orphan")
    findings = relationship("Finding", back_populates="asset")

class AssetRelationship(Base):
    __tablename__ = "asset_relationships"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    source_asset_id = Column(String(36), ForeignKey("assets.id", ondelete="CASCADE"), nullable=False)
    target_asset_id = Column(String(36), ForeignKey("assets.id", ondelete="CASCADE"), nullable=False)
    relationship_type = Column(String(100), nullable=False)  # CONNECTS_TO, RUNS, USES, EXPOSED_TO, HAS_ACCESS
    protocol = Column(String(50), nullable=True)
    port = Column(Integer, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=utc_now)

class Vulnerability(Base):
    __tablename__ = "vulnerabilities"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    asset_id = Column(String(36), ForeignKey("assets.id", ondelete="CASCADE"), nullable=False)
    cve_id = Column(String(100), index=True, nullable=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    severity = Column(String(50), nullable=False)  # CRITICAL, HIGH, MEDIUM, LOW
    cvss_score = Column(Float, default=0.0)
    exploit_available = Column(Boolean, default=False)
    remediation = Column(Text, nullable=True)
    status = Column(String(50), default="OPEN")  # OPEN, MITIGATED, RESOLVED
    created_at = Column(DateTime, default=utc_now)

    asset = relationship("Asset", back_populates="vulnerabilities")

class SecurityControl(Base):
    __tablename__ = "security_controls"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    control_type = Column(String(100), nullable=False)  # WAF, EDR, MFA, FIREWALL, IDS, ENCRYPTION
    asset_id = Column(String(36), ForeignKey("assets.id"), nullable=True)
    status = Column(String(50), default="ACTIVE")  # ACTIVE, DEGRADED, DISABLED
    effectiveness_score = Column(Float, default=1.0)
    configuration = Column(JSON, default=dict)
    created_at = Column(DateTime, default=utc_now)

class Finding(Base):
    __tablename__ = "findings"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    severity = Column(String(50), default="MEDIUM")  # CRITICAL, HIGH, MEDIUM, LOW, INFO
    confidence = Column(Float, default=0.9)
    asset_id = Column(String(36), ForeignKey("assets.id"), nullable=True)
    mitre_technique = Column(String(100), nullable=True)
    source = Column(String(100), default="CyberMIND AI")
    status = Column(String(50), default="OPEN")  # OPEN, IN_REVIEW, RESOLVED, FALSE_POSITIVE
    remediation = Column(Text, nullable=True)
    evidence_id = Column(String(36), nullable=True)
    created_at = Column(DateTime, default=utc_now)

    asset = relationship("Asset", back_populates="findings")

class Incident(Base):
    __tablename__ = "incidents"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    severity = Column(String(50), default="HIGH")  # CRITICAL, HIGH, MEDIUM, LOW
    status = Column(String(50), default="OPEN")  # OPEN, INVESTIGATING, CONTAINED, RESOLVED
    affected_assets = Column(JSON, default=list)
    indicators = Column(JSON, default=list)
    mitre_techniques = Column(JSON, default=list)
    timeline = Column(JSON, default=list)
    recommendations = Column(JSON, default=list)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

class ThreatIndicator(Base):
    __tablename__ = "threat_indicators"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    indicator_type = Column(String(50), nullable=False)  # IP, DOMAIN, HASH, URL, CVE
    value = Column(String(255), unique=True, index=True, nullable=False)
    threat_actor = Column(String(255), nullable=True)
    malware_family = Column(String(255), nullable=True)
    confidence = Column(Float, default=0.8)
    reputation_score = Column(Float, default=0.0)  # 0.0 to 100.0 (high is malicious)
    tags = Column(JSON, default=list)
    source = Column(String(100), default="OSINT")
    last_seen = Column(DateTime, default=utc_now)

class Evidence(Base):
    __tablename__ = "evidence"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    investigation_id = Column(String(36), nullable=True)
    evidence_type = Column(String(100), nullable=False)  # LOG, SCAN, PACKET, FILE, SCREENSHOT
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    raw_content = Column(Text, nullable=True)
    sha256_hash = Column(String(64), nullable=False)
    blockchain_tx_hash = Column(String(100), nullable=True)
    blockchain_status = Column(String(50), default="PENDING")  # PENDING, ANCHORED, VERIFIED, MISMATCH
    provenance_chain = Column(JSON, default=list)  # list of history entries
    created_at = Column(DateTime, default=utc_now)

class Investigation(Base):
    __tablename__ = "investigations"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    title = Column(String(255), nullable=False)
    query = Column(Text, nullable=False)
    status = Column(String(50), default="RUNNING")  # RUNNING, COMPLETED, FAILED
    plan = Column(JSON, default=list)
    agents_involved = Column(JSON, default=list)
    findings = Column(JSON, default=list)
    summary = Column(Text, nullable=True)
    created_at = Column(DateTime, default=utc_now)
    completed_at = Column(DateTime, nullable=True)

class AgentRun(Base):
    __tablename__ = "agent_runs"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    investigation_id = Column(String(36), ForeignKey("investigations.id"), nullable=True)
    agent_name = Column(String(100), nullable=False)
    status = Column(String(50), default="PENDING")  # PENDING, RUNNING, COMPLETED, FAILED
    input_data = Column(JSON, default=dict)
    output_data = Column(JSON, default=dict)
    confidence = Column(Float, default=1.0)
    latency_ms = Column(Integer, default=0)
    created_at = Column(DateTime, default=utc_now)

class ChatSession(Base):
    __tablename__ = "chat_sessions"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    title = Column(String(255), default="Security Investigation")
    created_at = Column(DateTime, default=utc_now)
    
    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    session_id = Column(String(36), ForeignKey("chat_sessions.id"), nullable=False)
    sender = Column(String(50), nullable=False)  # user, assistant, agent
    content = Column(Text, nullable=False)
    domain = Column(String(100), nullable=True)
    sources = Column(JSON, default=list)
    agent_trace = Column(JSON, default=list)
    created_at = Column(DateTime, default=utc_now)

    session = relationship("ChatSession", back_populates="messages")

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    title = Column(String(255), nullable=False)
    source = Column(String(100), nullable=False)  # OWASP, MITRE, NIST, CISA, CVE
    url = Column(String(500), nullable=True)
    domain = Column(String(100), nullable=False)  # Web Security, API Security, etc.
    version = Column(String(50), nullable=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=utc_now)
    
    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")

class DocumentChunk(Base):
    __tablename__ = "document_chunks"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    document_id = Column(String(36), ForeignKey("documents.id"), nullable=False)
    chunk_index = Column(Integer, nullable=False)
    chunk_text = Column(Text, nullable=False)
    metadata_json = Column(JSON, default=dict)
    embedding = Column(JSON, nullable=True)  # vector representation
    created_at = Column(DateTime, default=utc_now)

    document = relationship("Document", back_populates="chunks")

class AttackPath(Base):
    __tablename__ = "attack_paths"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    entry_point_id = Column(String(36), nullable=False)
    target_asset_id = Column(String(36), nullable=False)
    path_nodes = Column(JSON, default=list)  # list of asset IDs in order
    steps = Column(JSON, default=list)  # descriptions of each hop and technique
    risk_score = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=utc_now)

class Scenario(Base):
    __tablename__ = "scenarios"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    changes = Column(JSON, default=dict)  # modified assets/connections
    before_metrics = Column(JSON, default=dict)
    after_metrics = Column(JSON, default=dict)
    created_at = Column(DateTime, default=utc_now)

class Report(Base):
    __tablename__ = "reports"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    title = Column(String(255), nullable=False)
    report_type = Column(String(100), nullable=False)  # Incident, Vulnerability, Executive, Attack Surface
    content = Column(JSON, default=dict)
    created_at = Column(DateTime, default=utc_now)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), nullable=True)
    action = Column(String(100), nullable=False)
    resource = Column(String(100), nullable=False)
    details = Column(JSON, default=dict)
    ip_address = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=utc_now)
