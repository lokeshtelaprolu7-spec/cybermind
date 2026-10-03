'use client';

import React, { useState, useEffect } from 'react';
import Sidebar from '../../components/Sidebar';
import { Globe, Search, ShieldAlert, CheckCircle, AlertTriangle } from 'lucide-react';
import { apiRequest } from '../../lib/api';

export default function ThreatIntelligencePage() {
  const [indicators, setIndicators] = useState<any[]>([]);
  const [searchVal, setSearchVal] = useState('198.51.100.88');
  const [lookupResult, setLookupResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadIndicators();
  }, []);

  const loadIndicators = async () => {
    try {
      const data = await apiRequest('/threat-intel');
      setIndicators(data);
    } catch (e) {
      console.error(e);
    }
  };

  const handleLookup = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!searchVal.trim()) return;

    try {
      setLoading(true);
      const res = await apiRequest(`/threat-intel/${searchVal.trim()}`);
      setLookupResult(res);
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
              <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
                GLOBAL THREAT RADAR
              </span>
            </div>
            <h1 className="text-2xl font-bold text-slate-100 mt-1">Threat Intelligence & IOCs</h1>
          </div>
        </div>

        {/* Search Bar */}
        <div className="mt-6 bg-slate-900 border border-slate-800 rounded-xl p-5">
          <form onSubmit={handleLookup} className="flex gap-3">
            <div className="relative flex-1">
              <Search className="w-4 h-4 text-slate-500 absolute left-3.5 top-3" />
              <input
                type="text"
                placeholder="Search indicator by IP, domain, sha256 hash or CVE..."
                value={searchVal}
                onChange={(e) => setSearchVal(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-lg pl-10 pr-4 py-2.5 text-xs text-slate-100 focus:outline-none focus:border-cyan-500 font-mono"
              />
            </div>
            <button
              type="submit"
              disabled={loading}
              className="px-5 py-2.5 bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-semibold text-xs rounded-lg transition"
            >
              {loading ? 'Searching...' : 'Correlate IOC'}
            </button>
          </form>

          {/* Lookup Result Box */}
          {lookupResult && (
            <div className="mt-4 p-4 rounded-xl bg-slate-950 border border-slate-800 text-xs font-mono">
              <div className="flex items-center justify-between">
                <span className="font-bold text-slate-100 text-sm">{lookupResult.indicator}</span>
                <span
                  className={`px-2 py-0.5 rounded text-[10px] ${
                    lookupResult.verdict === 'MALICIOUS'
                      ? 'bg-rose-500/20 text-rose-400 border border-rose-500/30'
                      : 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                  }`}
                >
                  {lookupResult.verdict}
                </span>
              </div>
              <div className="mt-2 text-slate-400">
                Threat Actor: <span className="text-slate-200">{lookupResult.threat_actor}</span>
              </div>
              <div className="text-slate-400 mt-1">
                Reputation Score: <span className="text-rose-400">{lookupResult.reputation_score} / 100</span>
              </div>
            </div>
          )}
        </div>

        {/* Indicators Table */}
        <div className="mt-6 bg-slate-900 border border-slate-800 rounded-xl p-5">
          <h2 className="text-sm font-semibold text-slate-200 pb-3 border-b border-slate-800">
            Known Monitored Indicators
          </h2>

          <div className="mt-4 space-y-3">
            {indicators.map((ind) => (
              <div
                key={ind.id}
                className="p-3.5 bg-slate-950 border border-slate-800 rounded-lg text-xs font-mono flex items-center justify-between"
              >
                <div>
                  <div className="font-bold text-slate-100">{ind.value}</div>
                  <div className="text-[10px] text-slate-500 mt-0.5">
                    {ind.type} • Actor: {ind.threat_actor || 'Unknown'}
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <span className="px-2 py-0.5 rounded text-[10px] bg-rose-500/20 text-rose-400 border border-rose-500/30">
                    Reputation: {ind.reputation_score}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </main>
    </div>
  );
}
