'use client';

import React, { useState, useEffect } from 'react';
import Sidebar from '../../components/Sidebar';
import {
  Network,
  Shield,
  Server,
  AlertTriangle,
  Play,
  ArrowRight,
  RefreshCw,
  Cpu,
  Layers,
  Lock,
  Globe,
  Database
} from 'lucide-react';
import { apiRequest } from '../../lib/api';

export default function DigitalTwinPage() {
  const [topology, setTopology] = useState<any>(null);
  const [selectedNode, setSelectedNode] = useState<any>(null);
  const [simulationActive, setSimulationActive] = useState(false);
  const [scenarioResult, setScenarioResult] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadTopology();
  }, []);

  const loadTopology = async () => {
    try {
      setLoading(true);
      const data = await apiRequest('/digital-twin');
      setTopology(data);
      if (data.nodes && data.nodes.length > 0) {
        setSelectedNode(data.nodes[0]);
      }
    } catch (e) {
      console.error('Failed to load topology', e);
    } finally {
      setLoading(false);
    }
  };

  const runScenario = async () => {
    try {
      setSimulationActive(true);
      const res = await apiRequest('/digital-twin/scenario', {
        method: 'POST',
        body: JSON.stringify({
          name: 'Make API-01 Public',
          target_asset_name: 'API-01',
          action: 'EXPOSE_TO_INTERNET',
        }),
      });
      setScenarioResult(res);
    } catch (e) {
      console.error('Scenario failed', e);
    }
  };

  const resetScenario = () => {
    setSimulationActive(false);
    setScenarioResult(null);
  };

  return (
    <div className="flex min-h-screen bg-slate-950">
      <Sidebar />

      <main className="flex-1 ml-64 p-8 flex flex-col h-screen overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between pb-4 border-b border-slate-800">
          <div>
            <div className="flex items-center gap-2">
              <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
                CYBERNETIC TWIN GRAPH
              </span>
              <span className="text-xs text-slate-400 font-mono">Org: CyberMIND Demo Organization</span>
            </div>
            <h1 className="text-xl font-bold text-slate-100 mt-1">Infrastructure Graph & Simulation</h1>
          </div>

          <div className="flex items-center gap-3">
            {!simulationActive ? (
              <button
                onClick={runScenario}
                className="flex items-center gap-2 px-3 py-1.5 bg-rose-500 hover:bg-rose-400 text-slate-950 font-semibold text-xs rounded-lg transition shadow-[0_0_15px_rgba(244,63,94,0.3)]"
              >
                <Play className="w-3.5 h-3.5" />
                <span>Simulate Scenario: "Make API-01 Public"</span>
              </button>
            ) : (
              <button
                onClick={resetScenario}
                className="flex items-center gap-2 px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold text-xs rounded-lg border border-slate-700 transition"
              >
                <RefreshCw className="w-3.5 h-3.5" />
                <span>Reset Simulation</span>
              </button>
            )}
          </div>
        </div>

        {/* Content Layout */}
        <div className="flex-1 grid grid-cols-1 lg:grid-cols-3 gap-6 mt-4 overflow-hidden">
          {/* Interactive Graph Canvas */}
          <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-xl p-5 flex flex-col relative overflow-hidden">
            <div className="flex items-center justify-between pb-3 border-b border-slate-800/80">
              <span className="text-xs font-semibold text-slate-300">Live Infrastructure Topology</span>
              <div className="flex items-center gap-3 text-[11px] font-mono text-slate-400">
                <span className="flex items-center gap-1">
                  <span className="w-2.5 h-2.5 rounded-full bg-cyan-400" /> Internet Facing
                </span>
                <span className="flex items-center gap-1">
                  <span className="w-2.5 h-2.5 rounded-full bg-slate-600" /> Internal
                </span>
                <span className="flex items-center gap-1">
                  <span className="w-2.5 h-2.5 rounded-full bg-rose-500" /> Crown Jewel
                </span>
              </div>
            </div>

            {/* Simulated Delta Alert Banner */}
            {simulationActive && scenarioResult && (
              <div className="my-2 p-3 rounded-lg bg-rose-950/40 border border-rose-500/40 text-rose-300 text-xs flex items-center justify-between animate-pulse">
                <div className="flex items-center gap-2">
                  <AlertTriangle className="w-4 h-4 text-rose-400" />
                  <span>
                    <strong>SIMULATION ACTIVE:</strong> API-01 exposed to 0.0.0.0/0. Attack surface increased by{' '}
                    {scenarioResult.delta.attack_surface_increase}!
                  </span>
                </div>
              </div>
            )}

            {/* Grid of Nodes */}
            <div className="flex-1 overflow-y-auto p-4 grid grid-cols-2 md:grid-cols-4 gap-4">
              {topology &&
                topology.nodes.map((node: any) => {
                  const isSelected = selectedNode?.id === node.id;
                  const isExposed = node.data.isInternetFacing || (simulationActive && node.data.label === 'API-01');
                  const isCrownJewel = node.data.criticality === 'CRITICAL';

                  return (
                    <div
                      key={node.id}
                      onClick={() => setSelectedNode(node)}
                      className={`cursor-pointer p-4 rounded-xl border transition-all text-xs flex flex-col justify-between ${
                        isSelected
                          ? 'border-cyan-400 bg-cyan-950/20 shadow-[0_0_15px_rgba(6,182,212,0.2)]'
                          : 'border-slate-800 bg-slate-950 hover:border-slate-700'
                      }`}
                    >
                      <div>
                        <div className="flex items-center justify-between">
                          <span
                            className={`px-1.5 py-0.5 rounded text-[9px] font-mono font-medium ${
                              isExposed
                                ? 'bg-cyan-500/20 text-cyan-400 border border-cyan-500/30'
                                : 'bg-slate-800 text-slate-400'
                            }`}
                          >
                            {isExposed ? 'PUBLIC' : 'INTERNAL'}
                          </span>
                          {isCrownJewel && (
                            <span className="px-1.5 py-0.5 rounded text-[9px] font-mono bg-rose-500/20 text-rose-400 border border-rose-500/30">
                              CROWN JEWEL
                            </span>
                          )}
                        </div>

                        <div className="mt-3 font-bold text-slate-100 flex items-center gap-1.5">
                          {node.data.assetType === 'Database' ? (
                            <Database className="w-3.5 h-3.5 text-rose-400" />
                          ) : node.data.isInternetFacing ? (
                            <Globe className="w-3.5 h-3.5 text-cyan-400" />
                          ) : (
                            <Server className="w-3.5 h-3.5 text-slate-400" />
                          )}
                          <span>{node.data.label}</span>
                        </div>
                        <div className="text-[10px] text-slate-400 mt-0.5 font-mono">{node.data.ip || 'No IP'}</div>
                      </div>

                      <div className="mt-4 pt-2 border-t border-slate-800/80 flex items-center justify-between text-[10px] font-mono">
                        <span className="text-slate-500">{node.data.assetType}</span>
                        <span className="text-rose-400 font-semibold">Risk: {node.data.riskScore}/10</span>
                      </div>
                    </div>
                  );
                })}
            </div>
          </div>

          {/* Node Inspector & Scenario Comparison Sidebar */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 flex flex-col overflow-y-auto">
            {!simulationActive ? (
              // Selected Node Inspector
              selectedNode ? (
                <div>
                  <div className="flex items-center justify-between pb-3 border-b border-slate-800">
                    <div>
                      <h2 className="text-sm font-bold text-slate-100">{selectedNode.data.label}</h2>
                      <p className="text-[11px] text-slate-400 font-mono">{selectedNode.data.hostname}</p>
                    </div>
                    <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-cyan-500/10 text-cyan-400 border border-cyan-500/30">
                      {selectedNode.data.criticality} CRITICALITY
                    </span>
                  </div>

                  <div className="mt-4 space-y-3 text-xs">
                    <div>
                      <span className="text-slate-400 text-[11px]">Type & Environment:</span>
                      <p className="text-slate-200 font-medium">
                        {selectedNode.data.assetType} — Production
                      </p>
                    </div>

                    <div>
                      <span className="text-slate-400 text-[11px]">Installed Technologies:</span>
                      <div className="flex flex-wrap gap-1 mt-1">
                        {selectedNode.data.technologies?.map((tech: string, i: number) => (
                          <span
                            key={i}
                            className="px-2 py-0.5 bg-slate-950 border border-slate-800 rounded text-[10px] text-slate-300 font-mono"
                          >
                            {tech}
                          </span>
                        ))}
                      </div>
                    </div>

                    <div className="pt-3 border-t border-slate-800">
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-slate-300 font-semibold text-[11px] flex items-center gap-1.5">
                          <AlertTriangle className="w-3.5 h-3.5 text-rose-400" /> Correlated CVEs
                        </span>
                        <span className="text-[10px] font-mono text-rose-400">
                          {selectedNode.data.vulnerabilities?.length || 0} active
                        </span>
                      </div>

                      {selectedNode.data.vulnerabilities && selectedNode.data.vulnerabilities.length > 0 ? (
                        <div className="space-y-2">
                          {selectedNode.data.vulnerabilities.map((v: any, idx: number) => (
                            <div key={idx} className="p-2.5 rounded bg-slate-950 border border-slate-800 text-[11px]">
                              <div className="flex items-center justify-between text-rose-400 font-semibold">
                                <span>{v.cve_id}</span>
                                <span>CVSS {v.cvss}</span>
                              </div>
                              <p className="text-slate-300 mt-1">{v.title}</p>
                            </div>
                          ))}
                        </div>
                      ) : (
                        <p className="text-slate-500 text-[11px]">No critical CVEs directly bound to this asset.</p>
                      )}
                    </div>
                  </div>
                </div>
              ) : (
                <p className="text-slate-500 text-xs">Select an asset from the graph to inspect configuration.</p>
              )
            ) : (
              // Scenario Before / After Comparison
              scenarioResult && (
                <div className="space-y-4">
                  <div className="pb-3 border-b border-slate-800">
                    <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-rose-500/20 text-rose-400 border border-rose-500/30">
                      DELTA ANALYSIS
                    </span>
                    <h2 className="text-sm font-bold text-slate-100 mt-1">{scenarioResult.name}</h2>
                    <p className="text-[11px] text-slate-400 mt-0.5">{scenarioResult.description}</p>
                  </div>

                  {/* Before vs After Cards */}
                  <div className="grid grid-cols-2 gap-3 text-xs font-mono">
                    <div className="p-3 rounded-lg bg-slate-950 border border-slate-800">
                      <div className="text-slate-400 font-semibold pb-1 border-b border-slate-800">BEFORE</div>
                      <div className="mt-2 space-y-1 text-[11px]">
                        <div>Score: {scenarioResult.before_metrics.attack_surface_score}</div>
                        <div>Public Assets: {scenarioResult.before_metrics.internet_facing_count}</div>
                        <div>Paths: {scenarioResult.before_metrics.active_attack_paths}</div>
                      </div>
                    </div>

                    <div className="p-3 rounded-lg bg-rose-950/30 border border-rose-500/30 text-rose-300">
                      <div className="font-semibold pb-1 border-b border-rose-500/30 text-rose-400">AFTER SCENARIO</div>
                      <div className="mt-2 space-y-1 text-[11px]">
                        <div>Score: {scenarioResult.after_metrics.attack_surface_score}</div>
                        <div>Public Assets: {scenarioResult.after_metrics.internet_facing_count}</div>
                        <div>Paths: {scenarioResult.after_metrics.active_attack_paths}</div>
                      </div>
                    </div>
                  </div>

                  {/* Attacker Perspective */}
                  <div className="p-3 rounded-lg bg-slate-950 border border-slate-800 text-[11px]">
                    <div className="text-rose-400 font-semibold mb-1 flex items-center gap-1.5">
                      <Cpu className="w-3.5 h-3.5" /> Attacker Agent Insight
                    </div>
                    <p className="text-slate-300 leading-relaxed">{scenarioResult.attacker_perspective}</p>
                  </div>

                  {/* Defender Recommendations */}
                  <div className="p-3 rounded-lg bg-slate-950 border border-slate-800 text-[11px]">
                    <div className="text-cyan-400 font-semibold mb-1.5 flex items-center gap-1.5">
                      <Shield className="w-3.5 h-3.5" /> Defender Agent Recommendations
                    </div>
                    <ul className="space-y-1 text-slate-300 list-disc list-inside">
                      {scenarioResult.defender_recommendations.map((rec: string, i: number) => (
                        <li key={i}>{rec}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              )
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
