'use client';

import { TrendingUp, TrendingDown, Minus } from 'lucide-react';

interface BiasCardProps {
  emoji: string;
  label: string;
  sublabel: string;
  bias: string;
  confidence: number;
  summary: string;
  drivers: string[];
}

function biasColor(bias: string) {
  switch (bias?.toLowerCase()) {
    case 'bullish':
      return 'text-bullish border-bullish/30 bg-bullish/10';
    case 'bearish':
      return 'text-bearish border-bearish/30 bg-bearish/10';
    default:
      return 'text-neutral border-neutral/30 bg-neutral/10';
  }
}

function BiasIcon({ bias }: { bias: string }) {
  const size = 22;
  switch (bias?.toLowerCase()) {
    case 'bullish':
      return <TrendingUp size={size} />;
    case 'bearish':
      return <TrendingDown size={size} />;
    default:
      return <Minus size={size} />;
  }
}

export default function BiasCard({
  emoji,
  label,
  sublabel,
  bias,
  confidence,
  summary,
  drivers,
}: BiasCardProps) {
  const colorClasses = biasColor(bias);

  return (
    <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-6 backdrop-blur-sm">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-3">
          <span className="text-2xl">{emoji}</span>
          <div>
            <h3 className="text-lg font-semibold text-white">{label}</h3>
            <p className="text-xs text-gray-400">{sublabel}</p>
          </div>
        </div>
        <div className={`p-2 rounded-full border ${colorClasses}`}>
          <BiasIcon bias={bias} />
        </div>
      </div>

      <div className={`inline-flex items-center gap-2 px-3 py-1 rounded-full border mb-3 ${colorClasses}`}>
        <span className="font-bold text-sm">{bias}</span>
      </div>

      <div className="mb-3">
        <div className="flex justify-between text-xs text-gray-400 mb-1">
          <span>Confiance</span>
          <span>{confidence}%</span>
        </div>
        <div className="h-2 rounded-full bg-white/10 overflow-hidden">
          <div
            className={`h-full rounded-full ${
              bias?.toLowerCase() === 'bullish'
                ? 'bg-bullish'
                : bias?.toLowerCase() === 'bearish'
                ? 'bg-bearish'
                : 'bg-neutral'
            }`}
            style={{ width: `${confidence}%` }}
          />
        </div>
      </div>

      <p className="text-sm text-gray-300 mb-3">{summary}</p>

      <ul className="space-y-1">
        {drivers.map((driver, i) => (
          <li key={i} className="text-xs text-gray-400 flex gap-2">
            <span>▫️</span>
            <span>{driver}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
