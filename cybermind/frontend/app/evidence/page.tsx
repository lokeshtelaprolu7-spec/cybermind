'use client';

import React, { useState, useEffect } from 'react';
import Sidebar from '../../components/Sidebar';
import {
  Lock,
  ShieldCheck,
  CheckCircle,
  AlertTriangle,
  RefreshCw,
  Plus,
  ExternalLink,
  Clock,
  Key
} from 'lucide-react';
import { apiRequest } from '../../lib/api';

export default function EvidencePage() {
  const [evidenceList, setEvidenceList] = useState<any[]>([]);
  const [verificationResult, setVerificationResult] = useState<any>(null);
  const [verifyingId, setVerifyingId] = useState<string | null>(null);
  const [newEvidenceName, setNewEvidenceName] = useState('');
  const [newContent, setNewContent] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadEvidence();
  }, []);

  const loadEvidence = async () => {
    try {
      const data = await apiRequest('/evidence');
      setEvidenceList(data);
    } catch (e) {
      console.error('Failed to load evidence', e);
    }
  };

  const handleVerify = async (id: string) => {
    try {
      setVerifyingId(id);
      const res = await apiRequest(`/evidence/${id}/verify`, { method: 'POST' });
      setVerificationResult(res);
    } catch (e) {
      console.error('Verification failed', e);
    } finally {
      setVerifyingId(null);
    }
  };

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newEvidenceName.trim() || !newContent.trim()) return;

    try {
      setLoading(true);
      await apiRequest('/evidence', {
        method: 'POST',
        body: JSON.stringify({
          name: newEvidenceName,
          evidence_type: 'LOG',
          raw_content: newContent,
          description: 'Forensics evidence acquired by CyberMIND analyst',
        }),
      });
      setNewEvidenceName('');
      setNewContent('');
      loadEvidence();
    } catch (e) {
      console.error('Failed to create evidence', e);
    } finally {
      setLoading(false);
    }
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
                BLOCKCHAIN LEDGER PROVENANCE
              </span>
              <span className="text-xs text-slate-400 font-mono">EVM Cryptographic Hash Anchoring</span>
            </div>
            <h1 className="text-2xl font-bold text-slate-100 mt-1">Evidence Integrity & Provenance</h1>
          </div>
        </div>

        {/* Verification Status Modal / Toast */}
        {verificationResult && (
          <div
            className={`mt-6 p-4 rounded-xl border flex items-center justify-between transition-all ${
              verificationResult.is_valid
                ? 'bg-emerald-950/40 border-emerald-500/40 text-emerald-300'
                : 'bg-rose-950/40 border-rose-500/40 text-rose-300'
            }`}
          >
            <div className="flex items-center gap-3">
              {verificationResult.is_valid ? (
                <CheckCircle className="w-5 h-5 text-emerald-400 flex-shrink-0" />
              ) : (
                <AlertTriangle className="w-5 h-5 text-rose-400 flex-shrink-0" />
              )}
              <div>
                <div className="font-bold text-xs">
                  {verificationResult.integrity_status === 'INTEGRITY_VERIFIED'
                    ? '✓ CRYPTOGRAPHIC INTEGRITY VERIFIED'
                    : '⚠ INTEGRITY MISMATCH DETECTED'}
                </div>
                <div className="text-[11px] font-mono mt-0.5 opacity-90">
                  Target: {verificationResult.name} | SHA-256: {verificationResult.current_sha256}
                </div>
              </div>
            </div>
            <button
              onClick={() => setVerificationResult(null)}
              className="text-xs font-mono underline hover:opacity-80"
            >
              Dismiss
            </button>
          </div>
        )}

        {/* Grid Layout: Table & Add Form */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-6">
          {/* Evidence List */}
          <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-xl p-5">
            <h2 className="text-sm font-semibold text-slate-200 pb-3 border-b border-slate-800/80">
              Anchored Evidence Records
            </h2>

            <div className="mt-4 space-y-3">
              {evidenceList.map((e) => (
                <div
                  key={e.id}
                  className="p-4 rounded-lg bg-slate-950 border border-slate-800 text-xs flex flex-col justify-between space-y-3"
                >
                  <div className="flex items-center justify-between">
                    <div>
                      <span className="font-bold text-slate-100">{e.name}</span>
                      <span className="ml-2 px-1.5 py-0.5 rounded text-[10px] font-mono bg-cyan-500/10 text-cyan-400 border border-cyan-500/30">
                        {e.evidence_type}
                      </span>
                    </div>

                    <button
                      onClick={() => handleVerify(e.id)}
                      disabled={verifyingId === e.id}
                      className="flex items-center gap-1.5 px-3 py-1 bg-cyan-500/10 hover:bg-cyan-500/20 text-cyan-400 border border-cyan-500/30 rounded text-xs font-medium transition"
                    >
                      <ShieldCheck className="w-3.5 h-3.5" />
                      <span>{verifyingId === e.id ? 'Checking...' : 'Verify Integrity'}</span>
                    </button>
                  </div>

                  <div className="space-y-1 font-mono text-[11px] text-slate-400 bg-slate-900/60 p-2.5 rounded border border-slate-800/80">
                    <div className="truncate">
                      <span className="text-slate-500">SHA-256:</span> {e.sha256_hash}
                    </div>
                    {e.blockchain_tx_hash && (
                      <div className="truncate">
                        <span className="text-slate-500">Anchor TX:</span> {e.blockchain_tx_hash}
                      </div>
                    )}
                  </div>

                  {/* Provenance Steps */}
                  <div className="flex items-center gap-2 text-[10px] text-slate-400 font-mono pt-1">
                    <Clock className="w-3 h-3 text-cyan-400" />
                    <span>Provenance Chain:</span>
                    {e.provenance_chain?.map((p: any, i: number) => (
                      <span key={i} className="flex items-center gap-1">
                        <span className="text-slate-200">{p.step}</span>
                        {i < e.provenance_chain.length - 1 && <span>→</span>}
                      </span>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Add Evidence Form */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
            <h2 className="text-sm font-semibold text-slate-200 pb-3 border-b border-slate-800/80 flex items-center gap-2">
              <Plus className="w-4 h-4 text-cyan-400" /> Ingest & Anchor Evidence
            </h2>

            <form onSubmit={handleCreate} className="mt-4 space-y-4">
              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">Evidence Label</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Syslog Dump / Memory Dump"
                  value={newEvidenceName}
                  onChange={(e) => setNewEvidenceName(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-100 focus:outline-none focus:border-cyan-500"
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">
                  Raw Content / Diagnostic Telemetry
                </label>
                <textarea
                  rows={6}
                  required
                  placeholder="Paste raw log lines, packet dump or scan output..."
                  value={newContent}
                  onChange={(e) => setNewContent(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-100 font-mono focus:outline-none focus:border-cyan-500"
                />
              </div>

              <div className="p-3 rounded bg-slate-950 border border-slate-800 text-[11px] text-slate-400">
                <span className="text-amber-400 font-semibold">Security Note:</span> Raw evidence is stored securely
                in-database. Only the cryptographic SHA-256 hash is anchored onto the immutable ledger.
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full py-2.5 bg-cyan-500 hover:bg-cyan-400 disabled:opacity-50 text-slate-950 font-semibold rounded-lg text-xs flex items-center justify-center gap-2 transition"
              >
                <Lock className="w-4 h-4" />
                <span>{loading ? 'Hashing & Anchoring...' : 'Anchor to Blockchain'}</span>
              </button>
            </form>
          </div>
        </div>
      </main>
    </div>
  );
}
