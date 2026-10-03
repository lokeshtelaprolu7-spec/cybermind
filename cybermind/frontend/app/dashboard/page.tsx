'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import Sidebar from '../../components/Sidebar';
import {
  Server,
  AlertTriangle,
  Flame,
  GitFork,
  Globe,
  ShieldCheck,
  Bot,
  Lock,
  ArrowUpRight,
  TrendingUp,
  Cpu,
  ChevronRight
} from 'lucide-react';
import { apiRequest } from '../../lib/api';

export default function DashboardPage() {
  const [stats, setStats] = useState({
    totalAssets: 8,
    criticalFindings: 2,
    openIncidents: 1,
    attackPaths: 3,
    internetFacing: 2,
    highRiskAssets: 3,
    agentRuns: 14,
    anchoredEvidence: 6,
  });

  const [loading, setLoading] = useState(false);

  return (
    <div className="flex min-h-screen bg-slate-950">
      <Sidebar />

      <main className="flex-1 ml-64 p-8 overflow-y-auto">
        {/* Top Header */}
        <div className="flex items-center justify-between pb-6 border-b border-slate-800">
          <div>
            <div className="flex items-center gap-2">
              <span className="px-2.5 py-0.5 rounded text-[10px] font-mono font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                ACTIVE MONITORING
              </span>
              <span className="text-xs text-slate-400 font-mono">ORG: CyberMIND Demo Organization</span>
            </div>
            <h1 className="text-2xl font-bold text-slate-100 mt-1">Autonomous Security Operations</h1>
          </div>

          <div className="flex items-center gap-3">
            <Link
              href="/chat"
              className="flex items-center gap-2 px-3.5 py-2 bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-medium text-xs rounded-lg transition shadow-[0_0_15px_rgba(6,182,212,0.25)]"
            >
              <Bot className="w-4 h-4" />
              <span>Launch AI Analyst</span>
            </Link>
          </div>
        </div>

        {/* Metrics Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mt-6">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 hover:border-slate-700 transition">
            <div className="flex items-center justify-between text-slate-400">
              <span className="text-xs font-medium">Digital Twin Assets</span>
              <Server className="w-4 h-4 text-cyan-400" />
            </div>
            <div className="mt-2 flex items-baseline gap-2">
              <span className="text-2xl font-bold text-slate-100">{stats.totalAssets}</span>
              <span className="text-[11px] text-slate-400 font-mono">nodes mapped</span>
            </div>
            <div className="mt-2 text-[11px] text-emerald-400 flex items-center gap-1 font-mono">
              <span>● {stats.internetFacing} internet-facing</span>
            </div>
          </div>

          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 hover:border-slate-700 transition">
            <div className="flex items-center justify-between text-slate-400">
              <span className="text-xs font-medium">Critical Findings</span>
              <AlertTriangle className="w-4 h-4 text-rose-500" />
            </div>
            <div className="mt-2 flex items-baseline gap-2">
              <span className="text-2xl font-bold text-rose-400">{stats.criticalFindings}</span>
              <span className="text-[11px] text-slate-400 font-mono">action required</span>
            </div>
            <div className="mt-2 text-[11px] text-rose-400 flex items-center gap-1 font-mono">
              <span>▲ SQLi & Public API</span>
            </div>
          </div>

          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 hover:border-slate-700 transition">
            <div className="flex items-center justify-between text-slate-400">
              <span className="text-xs font-medium">Active Attack Paths</span>
              <GitFork className="w-4 h-4 text-amber-400" />
            </div>
            <div className="mt-2 flex items-baseline gap-2">
              <span className="text-2xl font-bold text-amber-300">{stats.attackPaths}</span>
              <span className="text-[11px] text-slate-400 font-mono">to Crown Jewels</span>
            </div>
            <div className="mt-2 text-[11px] text-amber-400 flex items-center gap-1 font-mono">
              <span>Target: DB-01 Customer Data</span>
            </div>
          </div>

          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 hover:border-slate-700 transition">
            <div className="flex items-center justify-between text-slate-400">
              <span className="text-xs font-medium">Evidence Anchored</span>
              <Lock className="w-4 h-4 text-emerald-400" />
            </div>
            <div className="mt-2 flex items-baseline gap-2">
              <span className="text-2xl font-bold text-emerald-300">{stats.anchoredEvidence}</span>
              <span className="text-[11px] text-slate-400 font-mono">SHA-256 proofs</span>
            </div>
            <div className="mt-2 text-[11px] text-emerald-400 flex items-center gap-1 font-mono">
              <span>✓ 100% verified integrity</span>
            </div>
          </div>
        </div>

        {/* Attack Surface & Digital Twin Quick Glance */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-6">
          <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-xl p-5">
            <div className="flex items-center justify-between pb-4 border-b border-slate-800/80">
              <div>
                <h2 className="text-sm font-semibold text-slate-200">Perimeter Attack Surface & Traversal</h2>
                <p className="text-xs text-slate-400 mt-0.5">Real-time graph model discovery from untrusted ingress to crown jewels</p>
              </div>
              <Link
                href="/digital-twin"
                className="text-xs text-cyan-400 hover:text-cyan-300 flex items-center gap-1 font-medium"
              >
                Open Visualizer <ChevronRight className="w-3.5 h-3.5" />
              </Link>
            </div>

            <div className="mt-4 p-4 rounded-lg bg-slate-950 border border-slate-800 font-mono text-xs space-y-3">
              <div className="flex items-center justify-between pb-2 border-b border-slate-800 text-slate-400 text-[11px]">
                <span>ATTACK VECTOR IDENTIFIER</span>
                <span>ENTRY POINT</span>
                <span>EXPLOITATION HOP</span>
                <span>TARGET ASSET</span>
                <span>RISK</span>
              </div>

              <div className="flex items-center justify-between text-slate-300 hover:bg-slate-900/50 p-1.5 rounded transition">
                <span className="text-cyan-400">PATH-01</span>
                <span>Internet</span>
                <span className="text-slate-400">→ WEB-01 (Nginx/React) → APP-01</span>
                <span className="text-rose-400 font-semibold">DB-01 (PostgreSQL)</span>
                <span className="px-2 py-0.5 rounded text-[10px] bg-rose-500/20 text-rose-400 border border-rose-500/30">9.2 CRITICAL</span>
              </div>

              <div className="flex items-center justify-between text-slate-300 hover:bg-slate-900/50 p-1.5 rounded transition">
                <span className="text-cyan-400">PATH-02</span>
                <span>Public Ingress</span>
                <span className="text-slate-400">→ API-01 (FastAPI) [No WAF]</span>
                <span className="text-rose-400 font-semibold">DB-01 (Customer PII)</span>
                <span className="px-2 py-0.5 rounded text-[10px] bg-amber-500/20 text-amber-400 border border-amber-500/30">7.8 HIGH</span>
              </div>

              <div className="flex items-center justify-between text-slate-300 hover:bg-slate-900/50 p-1.5 rounded transition">
                <span className="text-cyan-400">PATH-03</span>
                <span>VPN-01</span>
                <span className="text-slate-400">→ AUTH-01 (Keycloak) [Stolen Creds]</span>
                <span className="text-rose-400 font-semibold">AWS-S3-01 Backup</span>
                <span className="px-2 py-0.5 rounded text-[10px] bg-amber-500/20 text-amber-400 border border-amber-500/30">7.1 HIGH</span>
              </div>
            </div>
          </div>

          {/* AI Multi-Agent Triage Status */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
            <div className="flex items-center justify-between pb-3 border-b border-slate-800/80">
              <h2 className="text-sm font-semibold text-slate-200">Active Security Agents</h2>
              <span className="w-2 h-2 rounded-full bg-cyan-400 animate-ping" />
            </div>

            <div className="mt-4 space-y-3">
              {[
                { name: 'SOC Agent', role: 'Log & Anomaly Triage', status: 'IDLE', tech: 'MITRE T1110' },
                { name: 'VAPT Agent', role: 'Scan Correlation', status: 'ACTIVE', tech: 'CVSS 3.1' },
                { name: 'API Agent', role: 'Endpoint Auth Analysis', status: 'IDLE', tech: 'OWASP API' },
                { name: 'Cloud Agent', role: 'IAM & S3 Exposure', status: 'IDLE', tech: 'CIS Benchmark' },
                { name: 'Threat Intel Agent', role: 'IOC & Reputation Search', status: 'ACTIVE', tech: 'OSINT Feeds' },
                { name: 'Reviewer Agent', role: 'Hallucination Self-Check', status: 'ONLINE', tech: 'Verification' },
              ].map((agent) => (
                <div
                  key={agent.name}
                  className="flex items-center justify-between p-2 rounded-lg bg-slate-950/60 border border-slate-800/80 text-xs"
                >
                  <div>
                    <div className="font-medium text-slate-200">{agent.name}</div>
                    <div className="text-[10px] text-slate-500">{agent.role}</div>
                  </div>
                  <div className="text-right">
                    <span
                      className={`px-1.5 py-0.5 rounded text-[9px] font-mono ${
                        agent.status === 'ACTIVE'
                          ? 'bg-cyan-500/20 text-cyan-400 border border-cyan-500/30'
                          : 'bg-slate-800 text-slate-400'
                      }`}
                    >
                      {agent.status}
                    </span>
                    <div className="text-[9px] text-slate-500 font-mono mt-0.5">{agent.tech}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
