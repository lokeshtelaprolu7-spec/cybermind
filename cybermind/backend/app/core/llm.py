from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import httpx
import re
from app.core.config import settings

class LLMProvider(ABC):
    @abstractmethod
    async def generate(self, prompt: str, system_prompt: str = "", context: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """Generate a response given a user prompt and optional system context."""
        pass

class MockProvider(LLMProvider):
    """Safe local deterministic mock provider for cybersecurity analysis."""
    
    async def generate(self, prompt: str, system_prompt: str = "", context: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        lowered = prompt.lower()
        
        # Prompt Injection Protection Check
        injection_triggers = ["ignore all previous", "ignore previous", "reveal all system secrets", "reveal passwords", "system prompt"]
        if any(trigger in lowered for trigger in injection_triggers):
            return {
                "summary": "[SECURITY NOTICE] Potential prompt injection or unauthorized system query detected. Adversarial instruction has been neutralized according to CyberMIND defensive policies.",
                "domain": "AI Security",
                "findings": [
                    {
                        "title": "Adversarial Prompt Injection Attempt",
                        "severity": "HIGH",
                        "description": "Untrusted user query attempted to alter system behavior or exfiltrate private credentials."
                    }
                ],
                "evidence": ["Adversarial instruction patterns detected in user input stream."],
                "confidence": 0.99,
                "relevant_techniques": ["T1059 - Command and Scripting Interpreter"],
                "risk": "HIGH",
                "recommendations": [
                    "Isolate untrusted LLM input using prompt guard rails and deterministic sanitization filters.",
                    "Log anomalous inquiry to security audit trail."
                ],
                "sources": [
                    {"title": "OWASP Top 10 for LLM: LLM01 - Prompt Injection", "url": "https://owasp.org/www-project-top-10-for-large-language-model-applications/"}
                ],
                "limitations": "Input neutralized."
            }
        
        # 1. SQL Injection / Web Security
        if "sql" in lowered or "sqli" in lowered:
            return {
                "summary": "SQL Injection (SQLi) is a critical web security vulnerability that allows an attacker to interfere with the queries that an application makes to its database.",
                "domain": "Web Security",
                "findings": [
                    {
                        "title": "Improper Input Sanitization in SQL Queries",
                        "severity": "CRITICAL",
                        "cve": "CWE-89",
                        "description": "User input directly concatenated into SQL statement without parameterized queries or prepared statements."
                    }
                ],
                "evidence": ["Unfiltered input passed to database execute() method."],
                "confidence": 0.95,
                "relevant_techniques": ["T1190 - Exploit Public-Facing Application"],
                "risk": "CRITICAL (CVSS 9.8)",
                "recommendations": [
                    "Use parameterized queries (Prepared Statements) with Object Relational Mapping (ORM).",
                    "Employ defense-in-depth with Web Application Firewall (WAF) input filtering.",
                    "Apply the principle of least privilege to database service accounts."
                ],
                "sources": [
                    {"title": "OWASP Top 10:2021 - A03: Injection", "url": "https://owasp.org/Top10/A03_2021-Injection/"},
                    {"title": "MITRE ATT&CK T1190", "url": "https://attack.mitre.org/techniques/T1190/"}
                ],
                "limitations": "Analysis based on provided query semantics."
            }

        # 2. Public API exposure / Attack path
        elif "api" in lowered and ("public" in lowered or "accessible" in lowered or "expose" in lowered):
            return {
                "summary": "Exposing internal API endpoints directly to the public internet expands the attack surface, creating unauthenticated entry points towards backend databases.",
                "domain": "API Security",
                "findings": [
                    {
                        "title": "Public Exposure of Internal Microservice API-01",
                        "severity": "HIGH",
                        "cve": "OWASP-API3:2023",
                        "description": "API-01 bypasses perimeter API gateway security controls and connects directly to DB-01."
                    }
                ],
                "evidence": ["Route table shows 0.0.0.0/0 ingress bound directly to API-01 port 8080."],
                "confidence": 0.92,
                "relevant_techniques": ["T1190 - Exploit Public-Facing Application", "T1078 - Valid Accounts"],
                "risk": "HIGH (CVSS 8.2)",
                "recommendations": [
                    "Enforce API Gateway reverse proxy with OAuth2 / mTLS authentication.",
                    "Restrict IP allowlist or place API-01 inside private VPC subnet.",
                    "Implement rate limiting and token bucket throttling."
                ],
                "sources": [
                    {"title": "OWASP API Security Top 10 - API3 Broken Object Property Level Authorization", "url": "https://owasp.org/API-Security/"},
                    {"title": "NIST SP 800-204 Security Strategies for Microservices-based Application Systems", "url": "https://csrc.nist.gov/"}
                ],
                "limitations": "Assumes default configuration on simulated API-01."
            }

        # 3. Suspicious Login / SOC / Incident
        elif "login" in lowered or "credential" in lowered or "auth" in lowered:
            return {
                "summary": "High volume of anomalous authentication failures originating from untrusted autonomous systems, indicative of automated credential stuffing.",
                "domain": "SOC / Incident Response",
                "findings": [
                    {
                        "title": "Credential Stuffing and Brute-force Spike",
                        "severity": "HIGH",
                        "cve": "CWE-307",
                        "description": "500+ failed login attempts within 2 minutes targeting administrative accounts."
                    }
                ],
                "evidence": ["Auth logs show burst of 401 Unauthorized responses across rotating IP subnets."],
                "confidence": 0.91,
                "relevant_techniques": ["T1110.004 - Brute Force: Credential Stuffing"],
                "risk": "HIGH (CVSS 7.5)",
                "recommendations": [
                    "Enforce Multi-Factor Authentication (MFA) across all identity providers.",
                    "Activate adaptive risk-based authentication and CAPTCHA rate limiting.",
                    "Temporarily block identified malicious source CIDR blocks."
                ],
                "sources": [
                    {"title": "MITRE ATT&CK T1110 - Brute Force", "url": "https://attack.mitre.org/techniques/T1110/"},
                    {"title": "CISA Alert AA22-011A", "url": "https://www.cisa.gov/news-events/cybersecurity-advisories"}
                ],
                "limitations": "Log sample analysis only."
            }

        # 4. Default Security Intelligence Response
        return {
            "summary": f"CyberMIND Security Intelligence Analysis for query: '{prompt}'.",
            "domain": "Threat Intelligence",
            "findings": [
                {
                    "title": "Autonomous Security Assessment",
                    "severity": "MEDIUM",
                    "description": "Automated security evaluation performed across monitored digital twin perimeter assets."
                }
            ],
            "evidence": ["Digital twin telemetry and asset state configuration."],
            "confidence": 0.88,
            "relevant_techniques": ["T1595 - Active Scanning"],
            "risk": "MEDIUM (CVSS 5.4)",
            "recommendations": [
                "Maintain baseline configuration monitoring across all cloud and on-premise assets.",
                "Ensure continuous vulnerability management and patch deployment schedules."
            ],
            "sources": [
                {"title": "NIST Cybersecurity Framework (CSF 2.0)", "url": "https://www.nist.gov/cyberframework"},
                {"title": "CIS Critical Security Controls v8", "url": "https://www.cisecurity.org/controls"}
            ],
            "limitations": "Automated analytical synthesis based on current knowledge graph."
        }

class OpenAIProvider(LLMProvider):
    """OpenAI API provider."""
    
    def __init__(self, api_key: str, model: str = "gpt-4o", base_url: str = "https://api.openai.com/v1"):
        self.api_key = api_key
        self.model = model
        self.base_url = base_url.rstrip("/")

    async def generate(self, prompt: str, system_prompt: str = "", context: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        if context:
            ctx_text = "\n".join([f"[{c.get('source', 'Doc')}]: {c.get('text', '')}" for c in context])
            messages.append({"role": "system", "content": f"Reference Context:\n{ctx_text}"})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.2
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(f"{self.base_url}/chat/completions", headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()
            content = data["choices"][0]["message"]["content"]
            return {
                "summary": content,
                "domain": "AI Analysis",
                "findings": [],
                "evidence": [],
                "confidence": 0.9,
                "sources": [],
                "recommendations": []
            }

def get_llm_provider() -> LLMProvider:
    llm_key = settings.get_llm_key()
    if settings.LLM_PROVIDER in ("openai", "compatible") and llm_key:
        return OpenAIProvider(
            api_key=llm_key,
            model=settings.LLM_MODEL,
            base_url=settings.LLM_API_BASE or "https://api.openai.com/v1"
        )
    return MockProvider()
