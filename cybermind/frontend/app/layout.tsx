import './globals.css';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'CyberMIND — Autonomous Cybersecurity Digital Twin',
  description: 'Agentic AI-Powered Cybersecurity Digital Twin for Autonomous Attack-Surface Analysis, Threat Investigation, Cyber Memory, and Evidence-Based Security Intelligence',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-slate-950 text-slate-100 antialiased min-h-screen">
        {children}
      </body>
    </html>
  );
}
