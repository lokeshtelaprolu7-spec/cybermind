'use client';

import React, { useState, useEffect } from 'react';
import Sidebar from '../../components/Sidebar';
import { Flame, Clock, Shield, AlertCircle, CheckCircle } from 'lucide-react';
import { apiRequest } from '../../lib/api';

export default function IncidentsPage() {
  const [incidents, setIncidents] = useState<any[]>([]);

  useEffect(() => {
    loadIncidents();
  }, []);

  const loadIncidents = async () => {
    try {
      const data = await apiRequest('/incidents');
      setIncidents(data);
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
              <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-rose-500/10 text-rose-400 border border-rose-500/20">
                INCIDENT RESPONSE
              </span>
            </div>
            <h1 className="text-2xl font-bold text-slate-100 mt-1">Active Security Incidents</h1>
          </div>
        </div>

        <div className="mt-6 space-y-4">
          {incidents.map((inc) => (
            <div key={inc.id} className="p-6 rounded-2xl bg-slate-900 border border-slate-800 text-xs">
              <div className="flex items-center justify-between pb-3 border-b border-slate-800">
                <div className="flex items-center gap-2.5">
                  <Flame className="w-5 h-5 text-rose-400" />
                  <span className="font-bold text-base text-slate-100">{inc.title}</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="px-2.5 py-0.5 rounded text-[10px] font-mono bg-rose-500/20 text-rose-400 border border-rose-500/30">
                    {inc.severity}
                  </span>
                  <span className="px-2.5 py-0.5 rounded text-[10px] font-mono bg-cyan-500/10 text-cyan-400 border border-cyan-500/30">
                    STATUS: {inc.status}
                  </span>
                </div>
              </div>

              <p className="text-slate-300 mt-3 leading-relaxed">{inc.description}</p>

              {/* Affected Assets & Indicators */}
              <div className="mt-4 grid grid-cols-2 gap-4">
                <div className="p-3 bg-slate-950 rounded-lg border border-slate-800 font-mono">
                  <span className="text-slate-400 text-[11px]">Affected Assets:</span>
                  <div className="flex flex-wrap gap-1.5 mt-1">
                    {inc.affected_assets?.map((a: string, i: number) => (
                      <span key={i} className="px-2 py-0.5 bg-slate-900 rounded text-cyan-400 border border-slate-700">
                        {a}
                      </span>
                    ))}
                  </div>
                </div>

                <div className="p-3 bg-slate-950 rounded-lg border border-slate-800 font-mono">
                  <span className="text-slate-400 text-[11px]">Correlated Indicators (IOCs):</span>
                  <div className="flex flex-wrap gap-1.5 mt-1">
                    {inc.indicators?.map((ioc: string, i: number) => (
                      <span key={i} className="px-2 py-0.5 bg-slate-900 rounded text-rose-300 border border-slate-700">
                        {ioc}
                      </span>
                    ))}
                  </div>
                </div>
              </div>

              {/* Timeline */}
              <div className="mt-4 pt-3 border-t border-slate-800">
                <span className="text-slate-400 font-semibold font-mono text-[11px] flex items-center gap-1.5 mb-2">
                  <Clock className="w-3.5 h-3.5 text-cyan-400" /> Investigation Incident Timeline
                </span>
                <div className="space-y-1.5 font-mono text-[11px]">
                  {inc.timeline?.map((t: any, i: number) => (
                    <div key={i} className="flex items-center gap-3 text-slate-300">
                      <span className="text-slate-500">{t.time}</span>
                      <span>● {t.event}</span>
                    </div>
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
