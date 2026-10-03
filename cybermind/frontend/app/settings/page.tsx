'use client';

import React, { useState } from 'react';
import Sidebar from '../../components/Sidebar';
import { Settings, Save, Shield, Cpu, Key, Database } from 'lucide-react';

export default function SettingsPage() {
  const [llmProvider, setLlmProvider] = useState('mock');
  const [apiKey, setApiKey] = useState('');
  const [demoMode, setDemoMode] = useState(true);
  const [saved, setSaved] = useState(false);

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  };

  return (
    <div className="flex min-h-screen bg-slate-950">
      <Sidebar />

      <main className="flex-1 ml-64 p-8 overflow-y-auto">
        <div className="flex items-center justify-between pb-6 border-b border-slate-800">
          <div>
            <div className="flex items-center gap-2">
              <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
                SYSTEM CONFIGURATION
              </span>
            </div>
            <h1 className="text-2xl font-bold text-slate-100 mt-1">Platform Settings</h1>
          </div>
        </div>

        {saved && (
          <div className="mt-4 p-3 rounded-lg bg-emerald-950/40 border border-emerald-500/40 text-emerald-300 text-xs">
            Settings updated successfully.
          </div>
        )}

        <form onSubmit={handleSave} className="mt-6 max-w-2xl space-y-6">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
            <h2 className="text-sm font-semibold text-slate-200 pb-2 border-b border-slate-800 flex items-center gap-2">
              <Cpu className="w-4 h-4 text-cyan-400" /> AI & LLM Provider Configuration
            </h2>

            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1">Active AI Provider</label>
              <select
                value={llmProvider}
                onChange={(e) => setLlmProvider(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-100 focus:outline-none focus:border-cyan-500"
              >
                <option value="mock">Local Deterministic Provider (Offline / No API Key required)</option>
                <option value="openai">OpenAI (GPT-4o)</option>
                <option value="compatible">OpenAI-Compatible Local Endpoint (Ollama / vLLM)</option>
              </select>
            </div>

            {llmProvider !== 'mock' && (
              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">API Key</label>
                <input
                  type="password"
                  value={apiKey}
                  onChange={(e) => setApiKey(e.target.value)}
                  placeholder="sk-..."
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-100 focus:outline-none focus:border-cyan-500 font-mono"
                />
              </div>
            )}
          </div>

          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
            <h2 className="text-sm font-semibold text-slate-200 pb-2 border-b border-slate-800 flex items-center gap-2">
              <Shield className="w-4 h-4 text-cyan-400" /> Operational Modes
            </h2>

            <div className="flex items-center justify-between">
              <div>
                <div className="text-xs font-medium text-slate-200">Demonstration Mode (`DEMO_MODE=true`)</div>
                <div className="text-[11px] text-slate-400">
                  Pre-loads synthetic assets, vulnerabilities, and digital twin simulation topology.
                </div>
              </div>
              <input
                type="checkbox"
                checked={demoMode}
                onChange={(e) => setDemoMode(e.target.checked)}
                className="w-4 h-4 rounded text-cyan-500 focus:ring-cyan-500"
              />
            </div>
          </div>

          <button
            type="submit"
            className="px-6 py-2.5 bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-semibold rounded-lg text-xs flex items-center gap-2 transition"
          >
            <Save className="w-4 h-4" />
            <span>Save Configuration</span>
          </button>
        </form>
      </main>
    </div>
  );
}
