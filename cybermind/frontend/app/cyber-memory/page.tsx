'use client';

import React, { useState, useEffect } from 'react';
import Sidebar from '../../components/Sidebar';
import { Brain, History, BookOpen, Sparkles, CheckCircle } from 'lucide-react';
import { apiRequest } from '../../lib/api';

export default function CyberMemoryPage() {
  const [summary, setSummary] = useState<any>(null);
  const [query, setQuery] = useState('Credential stuffing bursts against authentication portal');
  const [matchResult, setMatchResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadSummary();
  }, []);

  const loadSummary = async () => {
    try {
      const data = await apiRequest('/cyber-memory/summary');
      setSummary(data);
    } catch (e) {
      console.error(e);
    }
  };

  const handleSearchSimilar = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    try {
      setLoading(true);
      const res = await apiRequest('/cyber-memory/similar-incidents', {
        method: 'POST',
        body: JSON.stringify({ query: query.trim() }),
      });
      setMatchResult(res);
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
              <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-purple-500/10 text-purple-400 border border-purple-500/20">
                ORGANIZATIONAL KNOWLEDGE STORE
              </span>
            </div>
            <h1 className="text-2xl font-bold text-slate-100 mt-1">Cyber Memory & Historical Incidents</h1>
          </div>
        </div>

        {/* Similar Incident Search Engine */}
        <div className="mt-6 bg-slate-900 border border-slate-800 rounded-xl p-5">
          <h2 className="text-sm font-semibold text-slate-200 mb-2 flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-purple-400" /> Similar Incident Vector Retrieval
          </h2>
          <p className="text-xs text-slate-400 mb-4">
            Search historical security episodes using entity correlation and semantic embeddings.
          </p>

          <form onSubmit={handleSearchSimilar} className="flex gap-3">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Describe incoming anomaly or incident characteristics..."
              className="flex-1 bg-slate-950 border border-slate-800 rounded-lg px-4 py-2.5 text-xs text-slate-100 focus:outline-none focus:border-purple-500"
            />
            <button
              type="submit"
              disabled={loading}
              className="px-5 py-2.5 bg-purple-500 hover:bg-purple-400 text-slate-950 font-semibold text-xs rounded-lg transition"
            >
              {loading ? 'Matching...' : 'Query Memory'}
            </button>
          </form>

          {matchResult && (
            <div className="mt-5 space-y-3">
              <div className="text-xs font-semibold text-purple-400 font-mono">
                Matched Historical Episodes ({matchResult.matched_incidents?.length})
              </div>

              {matchResult.matched_incidents?.map((m: any, idx: number) => (
                <div key={idx} className="p-4 bg-slate-950 border border-slate-800 rounded-xl text-xs space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-slate-100">{m.title}</span>
                    <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-purple-500/20 text-purple-300 border border-purple-500/30">
                      Similarity: {(m.similarity_score * 100).toFixed(0)}%
                    </span>
                  </div>

                  <div className="text-slate-400 text-[11px]">
                    <span className="text-slate-500">Proven Remediation:</span> {m.proven_remediation}
                  </div>

                  <div className="text-emerald-400 text-[11px] font-mono flex items-center gap-1.5">
                    <CheckCircle className="w-3.5 h-3.5" /> Historical Outcome: {m.outcome}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* 4 Pillars of Cyber Memory */}
        {summary && (
          <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="p-5 bg-slate-900 border border-slate-800 rounded-xl">
              <div className="text-xs font-bold text-cyan-400 uppercase tracking-wider font-mono">
                1. Episodic Memory (What happened?)
              </div>
              <div className="mt-3 text-xs space-y-1 text-slate-300">
                <div>Total Incidents Recorded: {summary.episodic_memory.total_incidents_recorded}</div>
                <div>Last Incident: {summary.episodic_memory.last_incident}</div>
                <div>Average Triage Dwell Time: {summary.episodic_memory.average_dwell_time}</div>
              </div>
            </div>

            <div className="p-5 bg-slate-900 border border-slate-800 rounded-xl">
              <div className="text-xs font-bold text-emerald-400 uppercase tracking-wider font-mono">
                2. Semantic Memory (What do we know?)
              </div>
              <div className="mt-3 text-xs space-y-1 text-slate-300">
                <div>Critical Assets Mapped: {summary.semantic_memory.critical_asset_inventory}</div>
                <div>Crown Jewel: {summary.semantic_memory.crown_jewel_designation}</div>
                <div>Protected Subnets: {summary.semantic_memory.monitored_subnets.join(', ')}</div>
              </div>
            </div>

            <div className="p-5 bg-slate-900 border border-slate-800 rounded-xl">
              <div className="text-xs font-bold text-amber-400 uppercase tracking-wider font-mono">
                3. Procedural Memory (What should we do?)
              </div>
              <ul className="mt-3 text-xs space-y-1 text-slate-300 list-disc list-inside">
                {summary.procedural_memory.active_playbooks.map((pb: string, i: number) => (
                  <li key={i}>{pb}</li>
                ))}
              </ul>
            </div>

            <div className="p-5 bg-slate-900 border border-slate-800 rounded-xl">
              <div className="text-xs font-bold text-rose-400 uppercase tracking-wider font-mono">
                4. Historical Memory (What happened previously?)
              </div>
              <div className="mt-3 text-xs space-y-1 text-slate-300">
                <div>Detection Blindspot Closures: {summary.historical_memory.detection_gap_closures}</div>
                <div>
                  Repeat Vulnerabilities: {summary.historical_memory.repeated_root_causes.join('; ')}
                </div>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
