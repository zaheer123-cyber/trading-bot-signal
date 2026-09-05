import React, { useState } from 'react'

function App() {
  const [activeTab, setActiveTab] = useState('dashboard')

  return (
    <div className="min-h-screen bg-slate-950 text-slate-200 font-sans">
      <nav className="border-b border-slate-800 bg-slate-900 px-6 py-4 flex items-center justify-between">
        <h1 className="text-xl font-bold bg-gradient-to-r from-blue-400 to-indigo-500 bg-clip-text text-transparent">
          Trading Platform
        </h1>
        <div className="space-x-4">
          <button 
            onClick={() => setActiveTab('dashboard')}
            className={`px-3 py-1 rounded-md transition-colors ${activeTab === 'dashboard' ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'}`}
          >
            Dashboard
          </button>
          <button 
            onClick={() => setActiveTab('backtest')}
            className={`px-3 py-1 rounded-md transition-colors ${activeTab === 'backtest' ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'}`}
          >
            Backtest
          </button>
          <button 
            onClick={() => setActiveTab('paper')}
            className={`px-3 py-1 rounded-md transition-colors ${activeTab === 'paper' ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'}`}
          >
            Paper Trading
          </button>
        </div>
      </nav>

      <main className="p-6 max-w-7xl mx-auto space-y-6">
        {activeTab === 'dashboard' && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="col-span-1 md:col-span-2 bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl">
              <h2 className="text-lg font-semibold mb-4">Live Chart Placeholder</h2>
              <div className="h-64 flex items-center justify-center border border-dashed border-slate-700 rounded-lg text-slate-500">
                Chart Component Goes Here
              </div>
            </div>
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl flex flex-col items-center justify-center">
              <div className="text-sm text-slate-400 uppercase tracking-wider mb-2">Latest Signal</div>
              <div className="text-4xl font-bold text-green-400 mb-2">CALL</div>
              <div className="text-lg text-slate-300">Score: 82/100</div>
              <div className="mt-6 w-full text-sm text-slate-400 space-y-2">
                <div className="flex justify-between"><span>Trend:</span> <span className="text-green-400">Bullish</span></div>
                <div className="flex justify-between"><span>RSI:</span> <span>61</span></div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'backtest' && (
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl">
            <h2 className="text-lg font-semibold mb-4">Backtest Engine</h2>
            <div className="h-64 flex items-center justify-center border border-dashed border-slate-700 rounded-lg text-slate-500">
              Run Backtest Form & Results
            </div>
          </div>
        )}

        {activeTab === 'paper' && (
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl">
            <h2 className="text-lg font-semibold mb-4">Paper Trading Session</h2>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
               <div className="p-4 bg-slate-800 rounded-lg">
                 <div className="text-xs text-slate-400 uppercase">Balance</div>
                 <div className="text-xl font-semibold">$1,000.00</div>
               </div>
               <div className="p-4 bg-slate-800 rounded-lg">
                 <div className="text-xs text-slate-400 uppercase">Today's P/L</div>
                 <div className="text-xl font-semibold text-green-400">+$24.00</div>
               </div>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}

export default App
