'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import {
  Shield,
  Activity,
  Bot,
  Network,
  Crosshair,
  GitFork,
  Server,
  AlertTriangle,
  Flame,
  Globe,
  Brain,
  BookOpen,
  Lock,
  FileText,
  Settings,
  LogOut
} from 'lucide-react';
import { removeAuthToken } from '../lib/api';

const navItems = [
  { name: 'Dashboard', href: '/dashboard', icon: Activity },
  { name: 'AI Security Analyst', href: '/chat', icon: Bot },
  { name: 'Digital Twin', href: '/digital-twin', icon: Network },
  { name: 'Attack Surface', href: '/attack-surface', icon: Crosshair },
  { name: 'Attack Paths', href: '/attack-paths', icon: GitFork },
  { name: 'Assets', href: '/assets', icon: Server },
  { name: 'Findings', href: '/findings', icon: AlertTriangle },
  { name: 'Incidents', href: '/incidents', icon: Flame },
  { name: 'Threat Intelligence', href: '/threat-intelligence', icon: Globe },
  { name: 'Cyber Memory', href: '/cyber-memory', icon: Brain },
  { name: 'Knowledge Base', href: '/knowledge', icon: BookOpen },
  { name: 'Evidence Provenance', href: '/evidence', icon: Lock },
  { name: 'Security Reports', href: '/reports', icon: FileText },
  { name: 'Settings', href: '/settings', icon: Settings },
];

export default function Sidebar() {
  const pathname = usePathname();
  const router = useRouter();

  const handleLogout = () => {
    removeAuthToken();
    router.push('/login');
  };

  return (
    <aside className="w-64 bg-slate-900 border-r border-slate-800 flex flex-col h-screen fixed left-0 top-0 select-none z-40">
      {/* Brand Header */}
      <div className="p-5 border-b border-slate-800 flex items-center space-x-3">
        <div className="w-10 h-10 rounded-lg bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center text-cyan-400">
          <Shield className="w-6 h-6 animate-pulse" />
        </div>
        <div>
          <h1 className="font-bold text-lg text-slate-100 tracking-wider flex items-center gap-1.5">
            Cyber<span className="text-cyan-400">MIND</span>
          </h1>
          <p className="text-[10px] text-slate-400 uppercase tracking-widest font-mono">Digital Twin SOC</p>
        </div>
      </div>

      {/* Navigation Links */}
      <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = pathname === item.href;
          return (
            <Link
              key={item.name}
              href={item.href}
              className={`flex items-center space-x-3 px-3 py-2.5 rounded-lg text-xs font-medium transition-all ${
                isActive
                  ? 'bg-cyan-500/15 text-cyan-400 border border-cyan-500/30 shadow-[0_0_12px_rgba(6,182,212,0.15)]'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
              }`}
            >
              <Icon className={`w-4 h-4 ${isActive ? 'text-cyan-400' : 'text-slate-400'}`} />
              <span>{item.name}</span>
            </Link>
          );
        })}
      </nav>

      {/* Footer Profile & Logout */}
      <div className="p-4 border-t border-slate-800 bg-slate-950/40">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2 text-xs">
            <div className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-ping" />
            <span className="text-slate-300 font-medium">SecOps Node 1</span>
          </div>
          <button
            onClick={handleLogout}
            title="Log Out"
            className="p-1.5 text-slate-400 hover:text-red-400 hover:bg-slate-800 rounded transition"
          >
            <LogOut className="w-4 h-4" />
          </button>
        </div>
      </div>
    </aside>
  );
}
