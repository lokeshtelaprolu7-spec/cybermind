export type UserRole = 'ADMIN' | 'ANALYST' | 'VIEWER';

export interface User {
  id: string;
  email: string;
  username: string;
  full_name?: string;
  role: UserRole;
  is_active: boolean;
  created_at: string;
}

export interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
}

export interface Asset {
  id: string;
  name: string;
  asset_type: 'Server' | 'Application' | 'API' | 'Database' | 'Cloud Resource' | 'Container' | 'Network' | 'Device';
  ip_address?: string;
  hostname?: string;
  environment: string;
  is_internet_facing: boolean;
  criticality: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  owner?: string;
  technologies: string[];
  risk_score: number;
  created_at: string;
}

export interface Vulnerability {
  id: string;
  asset_id: string;
  cve_id?: string;
  title: string;
  description?: string;
  severity: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  cvss_score: number;
  exploit_available: boolean;
  remediation?: string;
  status: 'OPEN' | 'MITIGATED' | 'RESOLVED';
}

export interface Finding {
  id: string;
  title: string;
  description: string;
  severity: 'INFO' | 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  confidence: number;
  asset_id?: string;
  mitre_technique?: string;
  source: string;
  status: 'OPEN' | 'IN_REVIEW' | 'RESOLVED' | 'FALSE_POSITIVE';
  remediation?: string;
  created_at: string;
}

export interface Incident {
  id: string;
  title: string;
  description: string;
  severity: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  status: 'OPEN' | 'INVESTIGATING' | 'CONTAINED' | 'RESOLVED';
  affected_assets: string[];
  indicators: string[];
  mitre_techniques: string[];
  timeline: { time: string; event: string }[];
  recommendations: string[];
  created_at: string;
}

export interface EvidenceRecord {
  id: string;
  investigation_id?: string;
  evidence_type: string;
  name: string;
  description?: string;
  sha256_hash: string;
  blockchain_tx_hash?: string;
  blockchain_status: 'PENDING' | 'ANCHORED' | 'VERIFIED' | 'MISMATCH';
  provenance_chain: { step: string; timestamp: string; actor: string }[];
  created_at: string;
}

export interface AgentStep {
  agent: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  action: string;
  timestamp: string;
  output?: any;
}

export interface ChatMessage {
  id: string;
  sender: 'user' | 'assistant' | 'agent';
  content: string;
  domain?: string;
  sources?: { title: string; url: string }[];
  agent_trace?: AgentStep[];
  created_at: string;
}
