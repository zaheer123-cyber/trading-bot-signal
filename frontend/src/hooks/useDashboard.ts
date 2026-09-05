import { useState, useEffect, useRef } from 'react';
import { fetchCandles, fetchLatestSignal, fetchHealth } from '../services/api';
import type { Candle, SignalData } from '../types/api';

const POLL_INTERVAL_MS = 5000;

interface UseDashboardReturn {
  candles: Candle[];
  signal: SignalData | null;
  loading: boolean;
  error: string | null;
  lastUpdated: Date | null;
  backendOnline: boolean;
}

export function useDashboard(): UseDashboardReturn {
  const [candles, setCandles] = useState<Candle[]>([]);
  const [signal, setSignal] = useState<SignalData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null);
  const [backendOnline, setBackendOnline] = useState(false);
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const fetchAll = async () => {
    try {
      const [candleData, signalData] = await Promise.all([
        fetchCandles(),
        fetchLatestSignal(),
      ]);
      setCandles(candleData.candles);
      setSignal(signalData);
      setLastUpdated(new Date());
      setError(null);
      setBackendOnline(true);
    } catch (err: unknown) {
      setBackendOnline(false);
      if (err instanceof Error) {
        const msg = err.message.includes('Network Error') || err.message.includes('ECONNREFUSED')
          ? 'Backend unavailable. Make sure FastAPI is running on port 8000.'
          : `Error: ${err.message}`;
        setError(msg);
      } else {
        setError('An unexpected error occurred.');
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // Check health first
    fetchHealth()
      .then(() => setBackendOnline(true))
      .catch(() => setBackendOnline(false));

    fetchAll();

    intervalRef.current = setInterval(fetchAll, POLL_INTERVAL_MS);

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
    };
  }, []);

  return { candles, signal, loading, error, lastUpdated, backendOnline };
}
