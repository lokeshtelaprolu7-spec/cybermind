'use client';

import React, { useState, useEffect } from 'react';
import Sidebar from '../../components/Sidebar';
import { BookOpen, ExternalLink, Plus, Layers, Database } from 'lucide-react';
import { apiRequest } from '../../lib/api';

export default function KnowledgePage() {
  const [docs, setDocs] = useState<any[]>([]);

  useEffect(() => {
    loadDocs();
  }, []);

  const loadDocs = async () => {
    try {
      const data = await apiRequest('/knowledge');
      setDocs(data);
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
                RETRIEVAL AUGMENTED GENERATION
              </span>
            </div>
            <h1 className="text-2xl font-bold text-slate-100 mt-1">Authoritative Knowledge Base</h1>
          </div>
        </div>

        <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4">
          {docs.map((d) => (
            <div key={d.id} className="p-5 bg-slate-900 border border-slate-800 rounded-xl text-xs space-y-3">
              <div className="flex items-center justify-between">
                <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-cyan-500/15 text-cyan-400 border border-cyan-500/30">
                  {d.source}
                </span>
                <span className="text-[10px] font-mono text-slate-500">v{d.version}</span>
              </div>

              <div>
                <h3 className="font-bold text-sm text-slate-100">{d.title}</h3>
                <div className="text-[11px] text-slate-400 mt-1">Domain: {d.domain}</div>
              </div>

              <div className="flex items-center justify-between pt-3 border-t border-slate-800/80 font-mono text-[10px] text-slate-400">
                <span>{d.chunks_count} Vector Chunks</span>
                {d.url && (
                  <a
                    href={d.url}
                    target="_blank"
                    rel="noreferrer"
                    className="flex items-center gap-1 text-cyan-400 hover:underline"
                  >
                    <span>Official Spec</span>
                    <ExternalLink className="w-3 h-3" />
                  </a>
                )}
              </div>
            </div>
          ))}
        </div>
      </main>
    </div>
  );
}
