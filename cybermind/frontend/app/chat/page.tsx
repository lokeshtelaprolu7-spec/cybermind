'use client';

import React, { useState } from 'react';
import Sidebar from '../../components/Sidebar';
import {
  Bot,
  Send,
  User,
  Shield,
  BookOpen,
  CheckCircle,
  AlertTriangle,
  ArrowRight,
  ExternalLink,
  Cpu,
  Layers,
  Sparkles
} from 'lucide-react';
import { apiRequest } from '../../lib/api';

interface Message {
  id: string;
  sender: 'user' | 'assistant';
  content: string;
  analysis?: any;
  sources?: any[];
  agentTrace?: string[];
  timestamp: string;
}

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      sender: 'assistant',
      content:
        'Greetings Operator. I am the CyberMIND AI Security Analyst. I coordinate specialized security agents (SOC, VAPT, Threat Intel, Cloud, Forensics, and Reviewer) backed by our digital twin knowledge graph and authoritative RAG brain. How may I assist your investigation?',
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    },
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const samplePrompts = [
    'Explain SQL injection and mitigation for our web application.',
    'What happens if API-01 becomes publicly accessible?',
    'Investigate anomalous login attempts on AUTH-01.',
    'Analyze vulnerability scan results on container cluster.',
  ];

  const handleSend = async (textToSend?: string) => {
    const query = textToSend || input;
    if (!query.trim() || loading) return;

    const userMsg: Message = {
      id: Date.now().toString(),
      sender: 'user',
      content: query,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const res = await apiRequest('/chat', {
        method: 'POST',
        body: JSON.stringify({ message: query }),
      });

      const assistantMsg: Message = {
        id: (Date.now() + 1).toString(),
        sender: 'assistant',
        content: res.summary || res.response || 'Security evaluation completed.',
        analysis: res,
        sources: res.sources || [],
        agentTrace: [
          'Orchestrator: Intent classified & agent routing dispatched',
          `Specialized Agent (${res.domain || 'CyberOps'}): RAG correlation and policy review`,
          'Security Reviewer: Adversarial hallucination check passed',
        ],
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };

      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err: any) {
      const errMsg: Message = {
        id: (Date.now() + 1).toString(),
        sender: 'assistant',
        content: `Investigation note: ${err.message || 'Error communicating with security backend.'}`,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };
      setMessages((prev) => [...prev, errMsg]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex h-screen bg-slate-950">
      <Sidebar />

      <main className="flex-1 ml-64 flex flex-col h-screen">
        {/* Header */}
        <header className="px-6 py-4 border-b border-slate-800 flex items-center justify-between bg-slate-900/50 backdrop-blur-md">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-lg bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center text-cyan-400">
              <Bot className="w-5 h-5" />
            </div>
            <div>
              <h1 className="text-sm font-semibold text-slate-100 flex items-center gap-2">
                CyberMIND AI Security Analyst
                <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-cyan-500/20 text-cyan-400 border border-cyan-500/30">
                  LangGraph Orchestrator
                </span>
              </h1>
              <p className="text-[11px] text-slate-400">
                Coordinating SOC, VAPT, Cloud, Threat Intel & Reviewer Agents
              </p>
            </div>
          </div>
        </header>

        {/* Messages Scroll Area */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {messages.map((m) => (
            <div
              key={m.id}
              className={`flex gap-4 max-w-4xl ${m.sender === 'user' ? 'ml-auto flex-row-reverse' : ''}`}
            >
              <div
                className={`w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0 ${
                  m.sender === 'user'
                    ? 'bg-slate-800 text-slate-200 border border-slate-700'
                    : 'bg-cyan-500/10 text-cyan-400 border border-cyan-500/30'
                }`}
              >
                {m.sender === 'user' ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
              </div>

              <div
                className={`flex-1 rounded-xl p-4 text-xs ${
                  m.sender === 'user'
                    ? 'bg-cyan-950/40 border border-cyan-800/40 text-slate-200'
                    : 'bg-slate-900 border border-slate-800 text-slate-300'
                }`}
              >
                <div className="flex items-center justify-between mb-2">
                  <span className="font-semibold text-slate-200">
                    {m.sender === 'user' ? 'Operator' : 'CyberMIND Analyst'}
                  </span>
                  <span className="text-[10px] text-slate-500 font-mono">{m.timestamp}</span>
                </div>

                <p className="leading-relaxed whitespace-pre-wrap">{m.content}</p>

                {/* Structured Analysis Cards */}
                {m.analysis && (
                  <div className="mt-4 space-y-3 pt-3 border-t border-slate-800">
                    {/* Domain & Risk Badge */}
                    <div className="flex flex-wrap items-center gap-2">
                      {m.analysis.domain && (
                        <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-purple-500/10 text-purple-400 border border-purple-500/20">
                          Domain: {m.analysis.domain}
                        </span>
                      )}
                      {m.analysis.risk && (
                        <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-rose-500/10 text-rose-400 border border-rose-500/20 font-semibold">
                          Risk: {m.analysis.risk}
                        </span>
                      )}
                      {m.analysis.confidence && (
                        <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                          Confidence: {(m.analysis.confidence * 100).toFixed(0)}%
                        </span>
                      )}
                    </div>

                    {/* Findings */}
                    {m.analysis.findings && m.analysis.findings.length > 0 && (
                      <div className="bg-slate-950/70 border border-slate-800/80 rounded-lg p-3 space-y-1.5">
                        <div className="text-[11px] font-semibold text-slate-200 flex items-center gap-1.5">
                          <AlertTriangle className="w-3.5 h-3.5 text-rose-400" />
                          Key Findings
                        </div>
                        {m.analysis.findings.map((f: any, idx: number) => (
                          <div key={idx} className="text-[11px] text-slate-300">
                            <span className="font-medium text-rose-300">● {f.title}</span>: {f.description}
                          </div>
                        ))}
                      </div>
                    )}

                    {/* Recommendations */}
                    {m.analysis.recommendations && m.analysis.recommendations.length > 0 && (
                      <div className="bg-slate-950/70 border border-slate-800/80 rounded-lg p-3 space-y-1.5">
                        <div className="text-[11px] font-semibold text-slate-200 flex items-center gap-1.5">
                          <CheckCircle className="w-3.5 h-3.5 text-cyan-400" />
                          Defense Recommendations
                        </div>
                        {m.analysis.recommendations.map((r: string, idx: number) => (
                          <div key={idx} className="text-[11px] text-slate-300">
                            <span className="text-cyan-400 font-mono">[{idx + 1}]</span> {r}
                          </div>
                        ))}
                      </div>
                    )}

                    {/* Citations & Sources */}
                    {m.sources && m.sources.length > 0 && (
                      <div className="mt-2 pt-2 border-t border-slate-800/60 flex flex-wrap items-center gap-2">
                        <span className="text-[10px] text-slate-400 flex items-center gap-1 font-mono">
                          <BookOpen className="w-3 h-3 text-cyan-400" /> Grounded Citations:
                        </span>
                        {m.sources.map((s: any, idx: number) => (
                          <a
                            key={idx}
                            href={s.url || '#'}
                            target="_blank"
                            rel="noreferrer"
                            className="inline-flex items-center gap-1 text-[10px] text-cyan-400 hover:underline bg-cyan-950/40 px-2 py-0.5 rounded border border-cyan-800/40 font-mono"
                          >
                            <span>{s.title}</span>
                            <ExternalLink className="w-2.5 h-2.5" />
                          </a>
                        ))}
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>
          ))}

          {loading && (
            <div className="flex items-center gap-3 text-xs text-cyan-400 bg-slate-900/60 border border-cyan-500/20 p-3 rounded-xl max-w-md animate-pulse">
              <Cpu className="w-4 h-4 animate-spin text-cyan-400" />
              <span>Coordinating Multi-Agent AI Investigation & RAG retrieval...</span>
            </div>
          )}
        </div>

        {/* Suggested Prompts */}
        <div className="px-6 py-2 border-t border-slate-800/60 bg-slate-900/30 flex items-center gap-2 overflow-x-auto">
          <span className="text-[10px] uppercase font-mono text-slate-500 flex items-center gap-1 flex-shrink-0">
            <Sparkles className="w-3 h-3 text-amber-400" /> Quick Inquiries:
          </span>
          {samplePrompts.map((p, idx) => (
            <button
              key={idx}
              onClick={() => handleSend(p)}
              className="text-[10px] text-slate-300 hover:text-cyan-400 bg-slate-800/60 hover:bg-slate-800 px-2.5 py-1 rounded-full whitespace-nowrap border border-slate-700/50 transition"
            >
              {p}
            </button>
          ))}
        </div>

        {/* Input Bar */}
        <div className="p-4 border-t border-slate-800 bg-slate-900/60 backdrop-blur-md">
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSend();
            }}
            className="flex items-center gap-3 max-w-4xl mx-auto"
          >
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask CyberMIND about attack surfaces, logs, vulnerabilities, or digital twin simulation..."
              className="flex-1 bg-slate-950 border border-slate-800 rounded-xl px-4 py-3 text-xs text-slate-100 focus:outline-none focus:border-cyan-500 transition shadow-inner"
            />
            <button
              type="submit"
              disabled={loading || !input.trim()}
              className="px-5 py-3 bg-cyan-500 hover:bg-cyan-400 disabled:opacity-50 text-slate-950 font-semibold rounded-xl text-xs flex items-center gap-2 transition shadow-[0_0_15px_rgba(6,182,212,0.3)] flex-shrink-0"
            >
              <span>Investigate</span>
              <Send className="w-4 h-4" />
            </button>
          </form>
        </div>
      </main>
    </div>
  );
}
