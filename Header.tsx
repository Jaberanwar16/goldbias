'use client';

import { Clock } from 'lucide-react';

interface HeaderProps {
  timeUntilNext: number;
}

function formatTime(seconds: number) {
  const mins = Math.floor(seconds / 60);
  const secs = seconds % 60;
  return `${mins}:${secs.toString().padStart(2, '0')}`;
}

export default function Header({ timeUntilNext }: HeaderProps) {
  return (
    <header className="flex items-center justify-between border-b border-white/10 pb-6 mb-8">
      <div className="flex items-center gap-3">
        <span className="text-3xl">🥇</span>
        <div>
          <h1 className="text-2xl font-bold text-white">Gold &amp; Dollar Bias</h1>
          <p className="text-sm text-gray-400">Analyse macroeconomique en temps reel</p>
        </div>
      </div>
      <div className="flex items-center gap-2 text-sm text-gray-400 bg-white/5 px-3 py-2 rounded-full border border-white/10">
        <Clock size={16} />
        <span>Prochaine analyse : {formatTime(timeUntilNext)}</span>
      </div>
    </header>
  );
}
