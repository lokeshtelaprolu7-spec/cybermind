'use client';

import React, { useState, useEffect } from 'react';
import Sidebar from '../../components/Sidebar';
import { AlertTriangle, CheckCircle, Shield, Search } from 'lucide-react';
import { apiRequest } from '../../lib/api';

export default function FindingsPage() {
  const [findings, setFindings] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadFindings();
  }, []);

  const loadFindings = async () => {
    try {
      const data = await apiRequest('/findings');
      setFindings(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen bg-slate-950">
      <Sidebar />

      <main className="flex-1 ml-64 p-8 overflow-y-auto">
        <div className="flex items-center justify-between pb-6 border-b border-slate-800">
          <div>
            <div className="flex items-center gap-2">
              <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-rose-500/10 text-rose-400 border border-rose-500/20">
                SECURITY TRIAGE QUEUE
              </span>
            </div>
            <h1 className="text-2xl font-bold text-slate-100 mt-1">Vulnerabilities & Findings</h1>
          </div>
        </div>

        <div className="mt-6 space-y-3">
          {findings.map((f) => (
            <div key={f.id} className="p-4 rounded-xl bg-slate-900 border border-slate-800 text-xs">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2.5">
                  <AlertTriangle
                    className={`w-4 h-4 ${f.severity === 'CRITICAL' ? 'text-rose-400' : 'text-amber-400'}`}
                  />
                  <span className="font-bold text-slate-100 text-sm">{f.title}</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-rose-500/20 text-rose-400 border border-rose-500/30">
                    {f.severity}
                  </span>
                  <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-cyan-500/10 text-cyan-400 border border-cyan-500/30">
                    Confidence: {(f.confidence * 100).toFixed(0)}%
                  </span>
                </div>
              </div>

              <p className="text-slate-300 mt-2 leading-relaxed">{f.description}</p>

              <div className="mt-3 p-3 bg-slate-950 rounded-lg border border-slate-800/80">
                <span className="text-cyan-400 font-semibold font-mono text-[11px]">Recommended Remediation:</span>
                <p className="text-slate-300 mt-0.5 text-[11px]">{f.remediation}</p>
              </div>

              <div className="mt-3 flex items-center justify-between text-[10px] text-slate-500 font-mono">
                <span>Source: {f.source}</span>
                <span>MITRE Technique: {f.mitre_technique || 'N/A'}</span>
                <span>Status: {f.status}</span>
              </div>
            </div>
          ))}
        </div>
      </main>
    </div>
  );
}
