'use client';

import React, { useState } from 'react';
import Sidebar from '../../components/Sidebar';
import {
  FileText,
  Download,
  Shield,
  AlertTriangle,
  GitFork,
  CheckCircle,
  Clock,
  Printer
} from 'lucide-react';
import { apiRequest } from '../../lib/api';

export default function ReportsPage() {
  const [report, setReport] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [reportType, setReportType] = useState('Executive Security Report');

  const handleGenerate = async () => {
    try {
      setLoading(true);
      const data = await apiRequest('/reports/generate', {
        method: 'POST',
        body: JSON.stringify({ report_type: reportType }),
      });
      setReport(data);
    } catch (e) {
      console.error('Failed to generate report', e);
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = () => {
    if (!report) return;
    const blob = new Blob([JSON.stringify(report, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `CyberMIND_${reportType.replace(/\s+/g, '_')}_${Date.now()}.json`;
    a.click();
  };

  return (
    <div className="flex min-h-screen bg-slate-950">
      <Sidebar />

      <main className="flex-1 ml-64 p-8 overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between pb-6 border-b border-slate-800">
          <div>
            <div className="flex items-center gap-2">
              <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
                AUDIT & COMPLIANCE
              </span>
              <span className="text-xs text-slate-400 font-mono">Autonomous Evidence-Based Reporting</span>
            </div>
            <h1 className="text-2xl font-bold text-slate-100 mt-1">Security Reports Engine</h1>
          </div>

          <div className="flex items-center gap-3">
            <select
              value={reportType}
              onChange={(e) => setReportType(e.target.value)}
              className="bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-100 focus:outline-none focus:border-cyan-500"
            >
              <option value="Executive Security Report">Executive Security Report</option>
              <option value="Vulnerability Assessment">Vulnerability Assessment</option>
              <option value="Attack Surface Assessment">Attack Surface Assessment</option>
              <option value="Digital Twin Audit">Digital Twin Audit</option>
            </select>

            <button
              onClick={handleGenerate}
              disabled={loading}
              className="px-4 py-2 bg-cyan-500 hover:bg-cyan-400 disabled:opacity-50 text-slate-950 font-semibold rounded-lg text-xs flex items-center gap-2 transition"
            >
              <FileText className="w-4 h-4" />
              <span>{loading ? 'Synthesizing...' : 'Generate Report'}</span>
            </button>
          </div>
        </div>

        {/* Report View */}
        {report ? (
          <div className="mt-6 bg-slate-900 border border-slate-800 rounded-2xl p-8 space-y-6">
            <div className="flex items-center justify-between pb-4 border-b border-slate-800">
              <div>
                <h2 className="text-xl font-bold text-slate-100">{report.title}</h2>
                <div className="flex items-center gap-3 text-xs text-slate-400 mt-1 font-mono">
                  <span>Organization: {report.organization}</span>
                  <span>•</span>
                  <span>Generated: {report.generated_at}</span>
                </div>
              </div>

              <button
                onClick={handleDownload}
                className="flex items-center gap-2 px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 rounded-lg text-xs font-medium transition"
              >
                <Download className="w-4 h-4" />
                <span>Export JSON</span>
              </button>
            </div>

            {/* Executive Summary */}
            <div className="space-y-2">
              <h3 className="text-xs font-bold text-cyan-400 uppercase tracking-wider font-mono">
                1. Executive Summary
              </h3>
              <p className="text-xs text-slate-300 leading-relaxed bg-slate-950 p-4 rounded-xl border border-slate-800">
                {report.executive_summary}
              </p>
            </div>

            {/* Environment Scope */}
            <div className="space-y-2">
              <h3 className="text-xs font-bold text-cyan-400 uppercase tracking-wider font-mono">
                2. Infrastructure Scope
              </h3>
              <div className="grid grid-cols-4 gap-4 text-xs font-mono">
                <div className="p-3 bg-slate-950 rounded-lg border border-slate-800">
                  <span className="text-slate-400">Monitored Assets:</span>
                  <div className="text-lg font-bold text-slate-100">{report.scope.monitored_assets}</div>
                </div>
                <div className="p-3 bg-slate-950 rounded-lg border border-slate-800">
                  <span className="text-slate-400">Critical CVEs:</span>
                  <div className="text-lg font-bold text-rose-400">{report.scope.critical_vulnerabilities}</div>
                </div>
                <div className="p-3 bg-slate-950 rounded-lg border border-slate-800">
                  <span className="text-slate-400">Open Findings:</span>
                  <div className="text-lg font-bold text-amber-400">{report.scope.open_findings}</div>
                </div>
                <div className="p-3 bg-slate-950 rounded-lg border border-slate-800">
                  <span className="text-slate-400">Incidents:</span>
                  <div className="text-lg font-bold text-slate-100">{report.scope.investigated_incidents}</div>
                </div>
              </div>
            </div>

            {/* Key Findings */}
            <div className="space-y-3">
              <h3 className="text-xs font-bold text-cyan-400 uppercase tracking-wider font-mono">
                3. Prioritized Findings
              </h3>
              <div className="space-y-2">
                {report.key_findings.map((f: any, idx: number) => (
                  <div key={idx} className="p-3.5 bg-slate-950 rounded-lg border border-slate-800 text-xs">
                    <div className="flex items-center justify-between">
                      <span className="font-bold text-slate-100">{f.title}</span>
                      <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-rose-500/20 text-rose-400 border border-rose-500/30">
                        {f.severity}
                      </span>
                    </div>
                    <p className="text-slate-300 mt-1">{f.remediation}</p>
                    <div className="mt-2 text-[10px] text-slate-500 font-mono">MITRE: {f.mitre}</div>
                  </div>
                ))}
              </div>
            </div>

            {/* Recommendations */}
            <div className="space-y-2">
              <h3 className="text-xs font-bold text-cyan-400 uppercase tracking-wider font-mono">
                4. Strategic Defender Recommendations
              </h3>
              <div className="p-4 bg-slate-950 rounded-xl border border-slate-800 space-y-2 text-xs">
                {report.recommendations.map((rec: string, idx: number) => (
                  <div key={idx} className="text-slate-300 flex items-start gap-2">
                    <CheckCircle className="w-4 h-4 text-cyan-400 flex-shrink-0 mt-0.5" />
                    <span>{rec}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        ) : (
          <div className="mt-12 flex flex-col items-center justify-center p-12 border border-dashed border-slate-800 rounded-2xl text-center">
            <FileText className="w-12 h-12 text-slate-600 mb-3" />
            <h3 className="text-sm font-semibold text-slate-300">No report generated yet</h3>
            <p className="text-xs text-slate-500 mt-1 max-w-sm">
              Select a report type and click "Generate Report" to synthesize telemetry, findings, and digital twin analysis into a structured security report.
            </p>
          </div>
        )}
      </main>
    </div>
  );
}
