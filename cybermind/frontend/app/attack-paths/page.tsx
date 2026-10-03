'use client';

import React, { useState, useEffect } from 'react';
import Sidebar from '../../components/Sidebar';
import { GitFork, ArrowRight, ShieldAlert, CheckCircle, Database } from 'lucide-react';
import { apiRequest } from '../../lib/api';

export default function AttackPathsPage() {
  const [paths, setPaths] = useState<any[]>([]);

  useEffect(() => {
    loadPaths();
  }, []);

  const loadPaths = async () => {
    try {
      const res = await apiRequest('/attack-paths');
      setPaths(res.paths || []);
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
              <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-amber-500/10 text-amber-400 border border-amber-500/20">
                GRAPH PATHFINDING
              </span>
            </div>
            <h1 className="text-2xl font-bold text-slate-100 mt-1">Attack Paths to Crown Jewels</h1>
          </div>
        </div>

        <div className="mt-6 space-y-4">
          {paths.map((p) => (
            <div key={p.id} className="p-6 rounded-2xl bg-slate-900 border border-slate-800 text-xs">
              <div className="flex items-center justify-between pb-3 border-b border-slate-800">
                <div className="flex items-center gap-2.5">
                  <GitFork className="w-5 h-5 text-amber-400" />
                  <span className="font-bold text-base text-slate-100">{p.name}</span>
                </div>
                <span className="px-2.5 py-0.5 rounded text-[10px] font-mono bg-rose-500/20 text-rose-400 border border-rose-500/30">
                  Risk: {p.risk_score} {p.severity}
                </span>
              </div>

              {/* Hop Sequence Flow */}
              <div className="mt-4 p-4 rounded-xl bg-slate-950 border border-slate-800/80">
                <span className="text-slate-500 text-[10px] uppercase font-mono tracking-widest block mb-2">
                  Traversal Vector:
                </span>
                <div className="flex flex-wrap items-center gap-2 text-xs font-mono">
                  {p.hops?.map((hop: string, idx: number) => (
                    <React.Fragment key={idx}>
                      <span
                        className={`px-3 py-1.5 rounded-lg border ${
                          idx === p.hops.length - 1
                            ? 'bg-rose-950/40 border-rose-500/40 text-rose-300 font-bold flex items-center gap-1.5'
                            : idx === 0
                            ? 'bg-cyan-950/40 border-cyan-500/40 text-cyan-300'
                            : 'bg-slate-900 border-slate-800 text-slate-300'
                        }`}
                      >
                        {idx === p.hops.length - 1 && <Database className="w-3.5 h-3.5 text-rose-400" />}
                        {hop}
                      </span>
                      {idx < p.hops.length - 1 && <ArrowRight className="w-4 h-4 text-slate-600 flex-shrink-0" />}
                    </React.Fragment>
                  ))}
                </div>
              </div>

              {/* Mitigation & MITRE */}
              <div className="mt-4 flex flex-col md:flex-row md:items-center justify-between gap-4 pt-3 border-t border-slate-800/80 text-[11px]">
                <div className="text-slate-300">
                  <span className="text-cyan-400 font-semibold font-mono">Mitigation Strategy:</span> {p.mitigation}
                </div>
                <div className="flex flex-wrap gap-1 font-mono text-[10px]">
                  {p.techniques?.map((tech: string, i: number) => (
                    <span key={i} className="px-2 py-0.5 bg-slate-950 border border-slate-800 rounded text-slate-400">
                      {tech}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>
      </main>
    </div>
  );
}
