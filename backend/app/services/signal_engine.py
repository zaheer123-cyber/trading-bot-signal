import pandas as pd
from typing import Dict, Any, Tuple
from app.config import settings

class SignalEngine:
    @staticmethod
    def generate_signal(row: pd.Series) -> Dict[str, Any]:
        """
        Generates a signal and score based on multi-confirmation logic.
        """
        ema_fast = row.get(f'ema_{settings.EMA_FAST}', 0)
        ema_slow = row.get(f'ema_{settings.EMA_SLOW}', 0)
        rsi = row.get(f'rsi_{settings.RSI_PERIOD}', 50)
        atr = row.get(f'atr_{settings.ATR_PERIOD}', 0)
        close = row.get('close', 0)
        
        reasons = []
        
        # Volatility Filter
        if atr < settings.ATR_MIN_VOLATILITY:
            return {
                "signal": "NO_TRADE",
                "score": 0,
                "confidence_label": "NONE",
                "reasons": ["Volatility too low (ATR)"]
            }
            
        # EMA Separation Filter
        ema_distance = row.get('ema_distance_pct', 0)
        if ema_distance < settings.EMA_DISTANCE_PERCENT_MIN:
            return {
                "signal": "NO_TRADE",
                "score": 0,
                "confidence_label": "NONE",
                "reasons": ["EMA distance too small (flat market)"]
            }
            
        # --- Evaluate CALL (Bullish) ---
        call_score, call_reasons = SignalEngine._evaluate_call(row, ema_fast, ema_slow, rsi, close)
        
        # --- Evaluate PUT (Bearish) ---
        put_score, put_reasons = SignalEngine._evaluate_put(row, ema_fast, ema_slow, rsi, close)
        
        # Determine final signal
        if call_score > put_score and call_score >= settings.SIGNAL_THRESHOLD:
            return {
                "signal": "CALL",
                "score": call_score,
                "confidence_label": SignalEngine._get_confidence(call_score),
                "reasons": call_reasons
            }
        elif put_score > call_score and put_score >= settings.SIGNAL_THRESHOLD:
            return {
                "signal": "PUT",
                "score": put_score,
                "confidence_label": SignalEngine._get_confidence(put_score),
                "reasons": put_reasons
            }
            
        return {
            "signal": "NO_TRADE",
            "score": max(call_score, put_score),
            "confidence_label": "NONE",
            "reasons": ["Score did not meet minimum threshold"]
        }

    @staticmethod
    def _evaluate_call(row: pd.Series, ema_fast: float, ema_slow: float, rsi: float, close: float) -> Tuple[int, list]:
        score = 0
        reasons = []
        
        # 1. Trend Confirmation (25 pts)
        if ema_fast > ema_slow:
            score += 25
            reasons.append("EMA20 above EMA50")
            
        # 2. RSI Momentum (20 pts)
        if 50 <= rsi <= settings.RSI_OVERBOUGHT:
            score += 20
            reasons.append("RSI momentum bullish")
        elif rsi > settings.RSI_OVERBOUGHT:
            # Overbought penalty
            reasons.append("RSI overbought")
            
        # 3. Support/Resistance (15 pts)
        support = row.get('support', 0)
        if support > 0 and (close - support) / close < 0.01:
            score += 15
            reasons.append("Price near support")
            
        # 4. Candlestick Confirmation (20 pts)
        if row.get('bullish_engulfing') or row.get('hammer') or row.get('strong_bullish'):
            score += 20
            reasons.append("Bullish candle confirmation")
            
        # 5. Volatility / ATR (10 pts)
        score += 10
        reasons.append("ATR volatility acceptable")
        
        # 6. Price/EMA structure (10 pts)
        if close > ema_fast:
            score += 10
            reasons.append("Price above short-term EMA")
            
        return score, reasons

    @staticmethod
    def _evaluate_put(row: pd.Series, ema_fast: float, ema_slow: float, rsi: float, close: float) -> Tuple[int, list]:
        score = 0
        reasons = []
        
        # 1. Trend Confirmation (25 pts)
        if ema_fast < ema_slow:
            score += 25
            reasons.append("EMA20 below EMA50")
            
        # 2. RSI Momentum (20 pts)
        if settings.RSI_OVERSOLD <= rsi <= 50:
            score += 20
            reasons.append("RSI momentum bearish")
        elif rsi < settings.RSI_OVERSOLD:
            # Oversold penalty
            reasons.append("RSI oversold")
            
        # 3. Support/Resistance (15 pts)
        resistance = row.get('resistance', 0)
        if resistance > 0 and (resistance - close) / close < 0.01:
            score += 15
            reasons.append("Price near resistance")
            
        # 4. Candlestick Confirmation (20 pts)
        if row.get('bearish_engulfing') or row.get('shooting_star') or row.get('strong_bearish'):
            score += 20
            reasons.append("Bearish candle confirmation")
            
        # 5. Volatility / ATR (10 pts)
        score += 10
        reasons.append("ATR volatility acceptable")
        
        # 6. Price/EMA structure (10 pts)
        if close < ema_fast:
            score += 10
            reasons.append("Price below short-term EMA")
            
        return score, reasons

    @staticmethod
    def _get_confidence(score: int) -> str:
        if score >= 90: return "VERY HIGH"
        if score >= 80: return "HIGH"
        if score >= 70: return "MEDIUM"
        return "LOW"
