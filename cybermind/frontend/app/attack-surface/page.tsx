'use client';

import React, { useState, useEffect } from 'react';
import Sidebar from '../../components/Sidebar';
import { Crosshair, Globe, Shield, AlertTriangle, Server, Database } from 'lucide-react';
import { apiRequest } from '../../lib/api';

export default function AttackSurfacePage() {
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    loadAttackSurface();
  }, []);

  const loadAttackSurface = async () => {
    try {
      const res = await apiRequest('/attack-surface');
      setData(res);
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="flex min-h-screen bg-slate-950">
      <Sidebar />

      <main className="flex-1 ml-64 p-8 overflow-y-auto">
        <div className="flex items-center justify-between pb-6 border-b border-slate-800">
          <div>
            <div className="flex items-center gap-2">
              <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
                PERIMETER TELEMETRY
              </span>
            </div>
            <h1 className="text-2xl font-bold text-slate-100 mt-1">Attack Surface Analysis</h1>
          </div>
        </div>

        {data && (
          <div className="mt-6 space-y-6">
            {/* Top Index Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="p-5 bg-slate-900 border border-slate-800 rounded-xl">
                <span className="text-slate-400 text-xs">Overall Attack Surface Index</span>
                <div className="text-3xl font-bold text-cyan-400 mt-1">{data.overall_attack_surface_index} pts</div>
                <span className="text-[10px] text-amber-400 font-mono mt-1 block">Level: {data.exposure_level}</span>
              </div>

              <div className="p-5 bg-slate-900 border border-slate-800 rounded-xl">
                <span className="text-slate-400 text-xs">Internet-Facing Ingress Nodes</span>
                <div className="text-3xl font-bold text-rose-400 mt-1">{data.internet_facing_assets?.length}</div>
                <span className="text-[10px] text-slate-500 font-mono mt-1 block">WEB-01, VPN-01</span>
              </div>

              <div className="p-5 bg-slate-900 border border-slate-800 rounded-xl">
                <span className="text-slate-400 text-xs">Active Perimeter Controls</span>
                <div className="text-3xl font-bold text-emerald-400 mt-1">{data.perimeter_controls?.length}</div>
                <span className="text-[10px] text-emerald-400 font-mono mt-1 block">WAF, WireGuard, TLS 1.3</span>
              </div>
            </div>

            {/* Exposed Assets List */}
            <div className="p-5 bg-slate-900 border border-slate-800 rounded-xl">
              <h2 className="text-sm font-semibold text-slate-200 pb-3 border-b border-slate-800">
                Internet-Facing Ingress Points
              </h2>
              <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4">
                {data.internet_facing_assets?.map((a: any) => (
                  <div key={a.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg text-xs font-mono">
                    <div className="flex items-center justify-between text-slate-100 font-bold">
                      <span className="flex items-center gap-2">
                        <Globe className="w-4 h-4 text-cyan-400" />
                        {a.name}
                      </span>
                      <span className="px-2 py-0.5 rounded text-[10px] bg-rose-500/20 text-rose-400 border border-rose-500/30">
                        Risk: {a.risk_score}
                      </span>
                    </div>
                    <div className="mt-2 text-slate-400 text-[11px]">IP Address: {a.ip}</div>
                    <div className="text-slate-500 text-[10px]">Type: {a.type} | Criticality: {a.criticality}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
