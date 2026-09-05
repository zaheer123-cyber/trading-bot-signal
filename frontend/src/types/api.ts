// API types for the backend responses
export interface Candle {
  timestamp: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

export interface MarketData {
  candles: Candle[];
}

export type SignalType = 'CALL' | 'PUT' | 'NO_TRADE';
export type TrendType = 'BULLISH' | 'BEARISH' | 'NEUTRAL';

export interface SignalData {
  signal: SignalType;
  score: number;
  trend: TrendType;
  rsi: number;
  ema_fast: number;
  ema_slow: number;
  atr: number;
  timestamp: string;
  reasons: string[];
}
