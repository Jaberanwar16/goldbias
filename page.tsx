'use client';

import { useCallback, useEffect, useState } from 'react';
import BiasCard from '@/components/BiasCard';
import Header from '@/components/Header';
import Timeline from '@/components/Timeline';

interface SentimentData {
  timestamp: string;
  gold: { bias: string; confidence: number; summary: string; key_drivers: string[] };
  dollar: { bias: string; confidence: number; summary: string; key_drivers: string[] };
  overall_comment: string;
  articles_analyzed: number;
}

const REFRESH_INTERVAL_SECONDS = 35 * 60;

export default function Home() {
  const [latest, setLatest] = useState<SentimentData | null>(null);
  const [history, setHistory] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [timeUntilNext, setTimeUntilNext] = useState(REFRESH_INTERVAL_SECONDS);

  const fetchData = useCallback(async () => {
    try {
      const [latestRes, historyRes] = await Promise.all([
        fetch('/api/latest'),
        fetch('/api/history?hours=24'),
      ]);

      if (!latestRes.ok) {
        throw new Error('Pas encore de donnees - le backend n\'a peut-etre pas encore fait son premier cycle');
      }

      const latestData = await latestRes.json();
      const historyData = await historyRes.json();

      setLatest(latestData);
      setHistory(historyData.data || []);
      setError(null);
    } catch (err: any) {
      setError(err.message || 'Impossible de charger les donnees');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 30000);
    return () => clearInterval(interval);
  }, [fetchData]);

  useEffect(() => {
    const timer = setInterval(() => {
      setTimeUntilNext((prev) => (prev > 0 ? prev - 1 : REFRESH_INTERVAL_SECONDS));
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  if (loading) {
    return (
      <main className="max-w-5xl mx-auto px-4 py-10">
        <div className="flex flex-col items-center justify-center h-64 gap-3 loading-pulse">
          <span className="text-4xl">🥇</span>
          <p className="text-gray-400">Chargement de l'analyse...</p>
        </div>
      </main>
    );
  }

  return (
    <main className="max-w-5xl mx-auto px-4 py-10">
      <Header timeUntilNext={timeUntilNext} />

      {error && (
        <div className="rounded-xl border border-yellow-500/30 bg-yellow-500/10 text-yellow-200 text-sm px-4 py-3 mb-6">
          {error}
        </div>
      )}

      {latest && (
        <div className="space-y-8">
          <div className="grid md:grid-cols-2 gap-6">
            <BiasCard
              emoji="🟡"
              label="Gold (XAUUSD)"
              sublabel="Or"
              bias={latest.gold.bias}
              confidence={latest.gold.confidence}
              summary={latest.gold.summary}
              drivers={latest.gold.key_drivers}
            />
            <BiasCard
              emoji="💵"
              label="Dollar (DXY)"
              sublabel="US Dollar Index"
              bias={latest.dollar.bias}
              confidence={latest.dollar.confidence}
              summary={latest.dollar.summary}
              drivers={latest.dollar.key_drivers}
            />
          </div>

          <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-6">
            <h3 className="text-lg font-semibold text-white mb-2">📊 Vue Macro</h3>
            <p className="text-gray-300 mb-4">{latest.overall_comment}</p>
            <div className="flex gap-4 text-xs text-gray-500">
              <span>📰 {latest.articles_analyzed} articles analyses</span>
              <span>
                🕐{' '}
                {new Date(latest.timestamp).toLocaleTimeString('fr-FR', {
                  timeZone: 'UTC',
                })}{' '}
                UTC
              </span>
            </div>
          </div>

          <Timeline history={history} />
        </div>
      )}

      <footer className="text-center text-xs text-gray-600 mt-10 pb-4">
        Donnees mises a jour toutes les 35 minutes • Source : FXStreet
      </footer>
    </main>
  );
}
