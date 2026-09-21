'use client';

interface HistoryItem {
  timestamp: string;
  gold: { bias: string; confidence: number };
  dollar: { bias: string; confidence: number };
}

function dot(bias: string) {
  switch (bias?.toLowerCase()) {
    case 'bullish':
      return '🟢';
    case 'bearish':
      return '🔴';
    default:
      return '⚪';
  }
}

export default function Timeline({ history }: { history: HistoryItem[] }) {
  if (history.length === 0) return null;

  return (
    <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-6">
      <h3 className="text-lg font-semibold text-white mb-4">📈 Historique (24h)</h3>
      <div className="space-y-2 max-h-80 overflow-y-auto pr-1">
        {history.slice(0, 20).map((item, i) => (
          <div
            key={i}
            className="flex items-center justify-between text-sm border-b border-white/5 pb-2 last:border-0"
          >
            <span className="text-gray-500 w-16">
              {new Date(item.timestamp).toLocaleTimeString('fr-FR', {
                hour: '2-digit',
                minute: '2-digit',
                timeZone: 'UTC',
              })}
            </span>
            <span className="flex items-center gap-1 text-gray-300">
              {dot(item.gold.bias)} {item.gold.bias} ({item.gold.confidence}%)
            </span>
            <span className="flex items-center gap-1 text-gray-300">
              {dot(item.dollar.bias)} {item.dollar.bias} ({item.dollar.confidence}%)
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
