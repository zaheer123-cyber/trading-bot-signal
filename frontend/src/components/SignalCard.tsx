import type { SignalType, TrendType } from '../types/api';

interface SignalCardProps {
  signal: SignalType;
  score: number;
  trend: TrendType;
  rsi: number;
  emaFast: number;
  emaSlow: number;
  atr: number;
  timestamp: string;
  reasons: string[];
}

function SignalBadge({ signal }: { signal: SignalType }) {
  const styles: Record<SignalType, string> = {
    CALL: 'text-green-400 bg-green-400/10 ring-1 ring-green-400/30',
    PUT: 'text-red-400 bg-red-400/10 ring-1 ring-red-400/30',
    NO_TRADE: 'text-yellow-400 bg-yellow-400/10 ring-1 ring-yellow-400/30',
  };

  return (
    <div className={`text-5xl font-black tracking-widest rounded-xl px-6 py-4 ${styles[signal]}`}>
      {signal === 'NO_TRADE' ? 'NO TRADE' : signal}
    </div>
  );
}

function ScoreBar({ score }: { score: number }) {
  const color =
    score >= 85 ? 'bg-green-500' : score >= 70 ? 'bg-indigo-500' : 'bg-yellow-500';
  return (
    <div className="w-full">
      <div className="flex justify-between text-xs text-slate-400 mb-1">
        <span>Strategy Score</span>
        <span className="font-semibold text-slate-200">{score}/100</span>
      </div>
      <div className="h-2 bg-slate-700 rounded-full overflow-hidden">
        <div
          className={`h-full rounded-full transition-all duration-700 ${color}`}
          style={{ width: `${score}%` }}
        />
      </div>
      <p className="text-xs text-slate-500 mt-1">
        Score ≠ win probability. Scores ≥70 trigger a signal.
      </p>
    </div>
  );
}

export function SignalCard({
  signal,
  score,
  trend,
  rsi,
  emaFast,
  emaSlow,
  atr,
  timestamp,
  reasons,
}: SignalCardProps) {
  const trendColor =
    trend === 'BULLISH' ? 'text-green-400' : trend === 'BEARISH' ? 'text-red-400' : 'text-yellow-400';

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-5 shadow-xl">
      <div className="flex flex-col items-center gap-3">
        <p className="text-xs uppercase tracking-widest text-slate-500">Latest Signal</p>
        <SignalBadge signal={signal} />
        <ScoreBar score={score} />
      </div>

      <div className="border-t border-slate-800 pt-4 grid grid-cols-2 gap-3 text-sm">
        <div className="space-y-1">
          <p className="text-slate-500 text-xs uppercase tracking-wide">Trend</p>
          <p className={`font-semibold ${trendColor}`}>{trend}</p>
        </div>
        <div className="space-y-1">
          <p className="text-slate-500 text-xs uppercase tracking-wide">RSI 14</p>
          <p className="font-semibold text-slate-200">{rsi.toFixed(1)}</p>
        </div>
        <div className="space-y-1">
          <p className="text-slate-500 text-xs uppercase tracking-wide">EMA 20</p>
          <p className="font-semibold text-slate-200">{emaFast.toFixed(3)}</p>
        </div>
        <div className="space-y-1">
          <p className="text-slate-500 text-xs uppercase tracking-wide">EMA 50</p>
          <p className="font-semibold text-slate-200">{emaSlow.toFixed(3)}</p>
        </div>
        <div className="col-span-2 space-y-1">
          <p className="text-slate-500 text-xs uppercase tracking-wide">ATR 14</p>
          <p className="font-semibold text-slate-200">{atr.toFixed(4)}</p>
        </div>
      </div>

      {reasons.length > 0 && (
        <div className="border-t border-slate-800 pt-4 space-y-1">
          <p className="text-slate-500 text-xs uppercase tracking-wide mb-2">Confirmation Reasons</p>
          {reasons.map((r, i) => (
            <div key={i} className="flex items-start gap-2 text-xs text-slate-300">
              <span className="text-indigo-400 mt-0.5">✓</span>
              <span>{r}</span>
            </div>
          ))}
        </div>
      )}

      <p className="text-xs text-slate-600 text-center pt-2 border-t border-slate-800">
        {timestamp ? new Date(timestamp).toLocaleString() : '—'}
      </p>
    </div>
  );
}
