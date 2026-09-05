import axios from 'axios';
import type { MarketData, SignalData } from '../types/api';

const BASE_URL = 'http://127.0.0.1:8000/api';

const api = axios.create({
  baseURL: BASE_URL,
  timeout: 5000,
});

export async function fetchCandles(): Promise<MarketData> {
  const res = await api.get<MarketData>('/market/candles');
  return res.data;
}

export async function fetchLatestSignal(): Promise<SignalData> {
  const res = await api.get<SignalData>('/signals/latest');
  return res.data;
}

export async function fetchHealth(): Promise<{ status: string }> {
  const res = await api.get<{ status: string }>('/health');
  return res.data;
}
