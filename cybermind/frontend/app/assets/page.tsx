'use client';

import React, { useState, useEffect } from 'react';
import Sidebar from '../../components/Sidebar';
import { Server, Globe, Database, Shield, AlertTriangle, Search, Plus } from 'lucide-react';
import { apiRequest } from '../../lib/api';

export default function AssetsPage() {
  const [assets, setAssets] = useState<any[]>([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAssets();
  }, []);

  const loadAssets = async () => {
    try {
      const data = await apiRequest('/assets');
      setAssets(data);
    } catch (e) {
      console.error('Failed to load assets', e);
    } finally {
      setLoading(false);
    }
  };

  const filtered = assets.filter(
    (a) =>
      a.name.toLowerCase().includes(search.toLowerCase()) ||
      a.asset_type.toLowerCase().includes(search.toLowerCase()) ||
      (a.ip_address && a.ip_address.includes(search))
  );

  return (
    <div className="flex min-h-screen bg-slate-950">
      <Sidebar />

      <main className="flex-1 ml-64 p-8 overflow-y-auto">
        <div className="flex items-center justify-between pb-6 border-b border-slate-800">
          <div>
            <div className="flex items-center gap-2">
              <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
                INVENTORY ASSET GRAPH
              </span>
            </div>
            <h1 className="text-2xl font-bold text-slate-100 mt-1">Infrastructure Assets</h1>
          </div>

          <div className="flex items-center gap-3">
            <div className="relative">
              <Search className="w-4 h-4 text-slate-500 absolute left-3 top-2.5" />
              <input
                type="text"
                placeholder="Search assets by name, type, IP..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="bg-slate-900 border border-slate-800 rounded-lg pl-9 pr-4 py-2 text-xs text-slate-100 focus:outline-none focus:border-cyan-500 w-64"
              />
            </div>
          </div>
        </div>

        {/* Table of Assets */}
        <div className="mt-6 bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-950/80 text-slate-400 uppercase font-mono text-[10px] border-b border-slate-800">
              <tr>
                <th className="p-3.5">Asset Name</th>
                <th className="p-3.5">Type</th>
                <th className="p-3.5">IP / Hostname</th>
                <th className="p-3.5">Exposure</th>
                <th className="p-3.5">Criticality</th>
                <th className="p-3.5">Risk Score</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 text-slate-300">
              {filtered.map((a) => (
                <tr key={a.id} className="hover:bg-slate-800/40 transition">
                  <td className="p-3.5 font-bold text-slate-100 flex items-center gap-2">
                    {a.asset_type === 'Database' ? (
                      <Database className="w-4 h-4 text-rose-400" />
                    ) : a.is_internet_facing ? (
                      <Globe className="w-4 h-4 text-cyan-400" />
                    ) : (
                      <Server className="w-4 h-4 text-slate-400" />
                    )}
                    <span>{a.name}</span>
                  </td>
                  <td className="p-3.5 text-slate-400 font-mono">{a.asset_type}</td>
                  <td className="p-3.5 font-mono text-[11px] text-slate-400">
                    <div>{a.ip_address || '—'}</div>
                    <div className="text-[10px] text-slate-600">{a.hostname}</div>
                  </td>
                  <td className="p-3.5 font-mono">
                    <span
                      className={`px-2 py-0.5 rounded text-[10px] ${
                        a.is_internet_facing
                          ? 'bg-cyan-500/15 text-cyan-400 border border-cyan-500/30'
                          : 'bg-slate-800 text-slate-400'
                      }`}
                    >
                      {a.is_internet_facing ? 'PUBLIC INGRESS' : 'INTERNAL'}
                    </span>
                  </td>
                  <td className="p-3.5 font-mono">
                    <span
                      className={`px-2 py-0.5 rounded text-[10px] ${
                        a.criticality === 'CRITICAL'
                          ? 'bg-rose-500/20 text-rose-400 border border-rose-500/30'
                          : a.criticality === 'HIGH'
                          ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
                          : 'bg-slate-800 text-slate-400'
                      }`}
                    >
                      {a.criticality}
                    </span>
                  </td>
                  <td className="p-3.5 font-mono font-bold text-rose-400">{a.risk_score} / 10</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </main>
    </div>
  );
}
