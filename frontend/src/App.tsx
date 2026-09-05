import { useState } from 'react';
import { Activity, BarChart2, TrendingUp, Settings, Wifi, WifiOff } from 'lucide-react';
import { CandlestickChart } from './components/CandlestickChart';
import { SignalCard } from './components/SignalCard';
import { ChartSkeleton, SignalCardSkeleton } from './components/Skeleton';
import { useDashboard } from './hooks/useDashboard';

type Tab = 'dashboard' | 'backtest' | 'paper' | 'settings';

function Header({ activeTab, setActiveTab, backendOnline, lastUpdated }: {
  activeTab: Tab;
  setActiveTab: (tab: Tab) => void;
  backendOnline: boolean;
  lastUpdated: Date | null;
}) {
  const navItems: { id: Tab; label: string; icon: React.ReactNode }[] = [
    { id: 'dashboard', label: 'Dashboard', icon: <Activity size={14} /> },
    { id: 'backtest', label: 'Backtest', icon: <BarChart2 size={14} /> },
    { id: 'paper', label: 'Paper Trading', icon: <TrendingUp size={14} /> },
    { id: 'settings', label: 'Settings', icon: <Settings size={14} /> },
  ];

  return (
    <nav className="sticky top-0 z-50 bg-slate-900/80 backdrop-blur border-b border-slate-800 px-6 py-3">
      <div className="max-w-7xl mx-auto flex items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="w-7 h-7 rounded-lg bg-gradient-to-br from-indigo-500 to-blue-600 flex items-center justify-center">
            <TrendingUp size={14} className="text-white" />
          </div>
          <span className="text-base font-bold bg-gradient-to-r from-indigo-400 to-blue-400 bg-clip-text text-transparent whitespace-nowrap">
            Signal Platform
          </span>
        </div>

        <div className="flex items-center gap-1">
          {navItems.map(({ id, label, icon }) => (
            <button
              key={id}
              id={`nav-${id}`}
              onClick={() => setActiveTab(id)}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-medium transition-all ${
                activeTab === id
                  ? 'bg-indigo-600 text-white'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'
              }`}
            >
              {icon}
              <span className="hidden sm:inline">{label}</span>
            </button>
          ))}
        </div>

        <div className="flex items-center gap-3 shrink-0">
          <div className={`flex items-center gap-1.5 text-xs font-medium ${backendOnline ? 'text-green-400' : 'text-red-400'}`}>
            {backendOnline ? <Wifi size={13} /> : <WifiOff size={13} />}
            <span className="hidden sm:inline">{backendOnline ? 'Connected' : 'Offline'}</span>
          </div>
          {lastUpdated && (
            <span className="hidden md:inline text-xs text-slate-600">
              Updated {lastUpdated.toLocaleTimeString()}
            </span>
          )}
        </div>
      </div>
    </nav>
  );
}

function ErrorBanner({ message }: { message: string }) {
  return (
    <div className="bg-red-900/30 border border-red-800/50 rounded-xl p-4 flex items-start gap-3">
      <WifiOff size={16} className="text-red-400 mt-0.5 shrink-0" />
      <div>
        <p className="text-red-300 text-sm font-medium">Connection Error</p>
        <p className="text-red-400/80 text-xs mt-0.5">{message}</p>
      </div>
    </div>
  );
}

function StatBadge({ label, value, color = 'text-slate-200' }: { label: string; value: string | number; color?: string }) {
  return (
    <div className="bg-slate-800/60 rounded-xl p-4 border border-slate-700/50">
      <p className="text-slate-500 text-xs uppercase tracking-wide">{label}</p>
      <p className={`text-xl font-bold mt-1 ${color}`}>{value}</p>
    </div>
  );
}

function DashboardTab() {
  const { candles, signal, loading, error, lastUpdated, backendOnline } = useDashboard();

  return (
    <div className="space-y-6">
      {/* Status & Error */}
      {error && <ErrorBanner message={error} />}

      {/* Market Overview Stats */}
      {signal && !loading && (
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          <StatBadge label="Signal" value={signal.signal === 'NO_TRADE' ? 'NO TRADE' : signal.signal}
            color={signal.signal === 'CALL' ? 'text-green-400' : signal.signal === 'PUT' ? 'text-red-400' : 'text-yellow-400'} />
          <StatBadge label="Strategy Score" value={`${signal.score}/100`}
            color={signal.score >= 80 ? 'text-green-400' : signal.score >= 70 ? 'text-indigo-400' : 'text-slate-300'} />
          <StatBadge label="Trend" value={signal.trend}
            color={signal.trend === 'BULLISH' ? 'text-green-400' : signal.trend === 'BEARISH' ? 'text-red-400' : 'text-yellow-400'} />
          <StatBadge label="RSI 14" value={signal.rsi.toFixed(1)}
            color={signal.rsi > 70 ? 'text-red-400' : signal.rsi < 30 ? 'text-green-400' : 'text-slate-200'} />
        </div>
      )}

      {/* Main Grid: Chart + Signal Card */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Candlestick Chart */}
        <div className="lg:col-span-2">
          {loading ? (
            <ChartSkeleton />
          ) : candles.length > 0 ? (
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4 shadow-xl">
              <div className="flex items-center justify-between mb-3">
                <div>
                  <h2 className="text-sm font-semibold text-slate-200">OHLC Chart</h2>
                  <p className="text-xs text-slate-500">sample.csv · 5-min bars · Last {candles.length} candles</p>
                </div>
                <div className="flex items-center gap-2 text-xs text-slate-500">
                  <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-sm bg-green-500 inline-block" />Bull</span>
                  <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-sm bg-red-500 inline-block" />Bear</span>
                </div>
              </div>
              <CandlestickChart candles={candles} />
            </div>
          ) : (
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-12 shadow-xl text-center">
              <BarChart2 size={40} className="mx-auto text-slate-700 mb-3" />
              <p className="text-slate-400 text-sm">No candle data available.</p>
              <p className="text-slate-600 text-xs mt-1">Add a CSV file to <code>data/raw/sample.csv</code></p>
            </div>
          )}
        </div>

        {/* Signal Card */}
        <div className="lg:col-span-1">
          {loading ? (
            <SignalCardSkeleton />
          ) : signal ? (
            <SignalCard
              signal={signal.signal}
              score={signal.score}
              trend={signal.trend}
              rsi={signal.rsi}
              emaFast={signal.ema_fast}
              emaSlow={signal.ema_slow}
              atr={signal.atr}
              timestamp={signal.timestamp}
              reasons={signal.reasons}
            />
          ) : (
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8 text-center shadow-xl">
              <Activity size={32} className="mx-auto text-slate-700 mb-3" />
              <p className="text-slate-400 text-sm">No signal data available.</p>
            </div>
          )}
        </div>
      </div>

      {/* Disclaimer */}
      <div className="text-xs text-slate-600 text-center px-4 pt-2 border-t border-slate-800/50">
        ⚠ This is an educational research tool. Scores are not win probabilities.
        Past performance does not guarantee future results. No real orders are placed.
        Auto-refreshing every 5 seconds.
      </div>
    </div>
  );
}

function BacktestTab() {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8 shadow-xl space-y-4">
      <h2 className="text-lg font-semibold text-slate-200 flex items-center gap-2">
        <BarChart2 size={18} className="text-indigo-400" />
        Backtest Engine
      </h2>
      <p className="text-slate-500 text-sm">
        Run a historical backtest using your CSV dataset. Submit the file path and configuration via the API.
      </p>
      <div className="rounded-xl bg-slate-800 p-4 text-xs font-mono text-slate-400 space-y-1">
        <p>POST /api/backtest/run</p>
        <p className="text-slate-600">{'{ "filepath": "data/raw/sample.csv" }'}</p>
      </div>
      <p className="text-slate-600 text-xs">Full UI controls coming in the next phase.</p>
    </div>
  );
}

function PaperTab() {
  return (
    <div className="space-y-6">
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        <StatBadge label="Balance" value="$1,000.00" />
        <StatBadge label="Today's P/L" value="+$0.00" color="text-green-400" />
        <StatBadge label="Trades Today" value="0" />
        <StatBadge label="Win Rate" value="—" />
      </div>
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8 text-center shadow-xl">
        <TrendingUp size={40} className="mx-auto text-slate-700 mb-3" />
        <p className="text-slate-400 text-sm">No active paper trading session.</p>
        <p className="text-slate-600 text-xs mt-1">
          This page simulates trades without placing real orders.
        </p>
      </div>
    </div>
  );
}

function SettingsTab() {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8 shadow-xl space-y-4">
      <h2 className="text-lg font-semibold text-slate-200 flex items-center gap-2">
        <Settings size={18} className="text-indigo-400" />
        Platform Settings
      </h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-sm">
        {[
          ['EMA Fast', '20'],
          ['EMA Slow', '50'],
          ['RSI Period', '14'],
          ['ATR Period', '14'],
          ['Signal Threshold', '70'],
          ['Payout', '0.80'],
          ['Trade Amount', '$10'],
          ['Max Daily Loss', '$50'],
        ].map(([label, val]) => (
          <div key={label} className="flex justify-between bg-slate-800 rounded-lg px-4 py-3">
            <span className="text-slate-400">{label}</span>
            <span className="text-slate-200 font-medium">{val}</span>
          </div>
        ))}
      </div>
      <p className="text-xs text-slate-600">
        Modify these values in <code className="text-indigo-400">.env</code> and restart the backend.
      </p>
    </div>
  );
}

function App() {
  const [activeTab, setActiveTab] = useState<Tab>('dashboard');
  const { backendOnline, lastUpdated } = useDashboard();

  return (
    <div className="min-h-screen bg-slate-950 text-slate-200">
      <Header activeTab={activeTab} setActiveTab={setActiveTab} backendOnline={backendOnline} lastUpdated={lastUpdated} />
      <main className="max-w-7xl mx-auto px-4 sm:px-6 py-6 space-y-6">
        {activeTab === 'dashboard' && <DashboardTab />}
        {activeTab === 'backtest' && <BacktestTab />}
        {activeTab === 'paper' && <PaperTab />}
        {activeTab === 'settings' && <SettingsTab />}
      </main>
    </div>
  );
}

export default App;
