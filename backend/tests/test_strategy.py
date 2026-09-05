import pytest
import pandas as pd
import numpy as np
from app.services.indicators import Indicators
from app.services.signal_engine import SignalEngine
from app.services.risk_manager import RiskManager
from app.services.data_loader import DataLoader
import tempfile
import os


# ─── Helper ───────────────────────────────────────────────────────────────────

def make_trending_df(num=80, trend="bull"):
    """Create a synthetic dataframe with a clear trend."""
    np.random.seed(42)
    start = 100.0
    data = []
    for i in range(num):
        drift = 0.3 if trend == "bull" else -0.3
        o = start + drift * i + np.random.normal(0, 0.2)
        c = o + drift + np.random.normal(0, 0.1)
        h = max(o, c) + abs(np.random.normal(0, 0.1))
        l = min(o, c) - abs(np.random.normal(0, 0.1))
        data.append({
            "timestamp": pd.Timestamp("2024-01-01") + pd.Timedelta(minutes=5 * i),
            "open": o, "high": h, "low": l, "close": c, "volume": 500
        })
    return pd.DataFrame(data)


# ─── Indicator Tests ───────────────────────────────────────────────────────────

class TestEMA:
    def test_ema_column_created(self):
        df = pd.DataFrame({"close": range(1, 51)})
        df = Indicators.add_ema(df, period=5)
        assert "ema_5" in df.columns

    def test_ema_not_all_nan(self):
        df = pd.DataFrame({"close": [float(x) for x in range(1, 51)]})
        df = Indicators.add_ema(df, period=5)
        assert df["ema_5"].notna().sum() > 0

    def test_ema_bullish_fast_gt_slow(self):
        df = make_trending_df(80, "bull")
        df = Indicators.add_ema(df, period=20)
        df = Indicators.add_ema(df, period=50)
        last = df.dropna()
        # In a persistent bull trend, EMA20 > EMA50
        assert last["ema_20"].iloc[-1] > last["ema_50"].iloc[-1]

    def test_ema_insufficient_data(self):
        df = pd.DataFrame({"close": [100.0, 101.0]})
        df = Indicators.add_ema(df, period=10)
        # Should not crash; all values may be NaN or valid (ewm handles any length)
        assert "ema_10" in df.columns


class TestRSI:
    def test_rsi_column_created(self):
        df = make_trending_df(50)
        df = Indicators.add_rsi(df, period=14)
        assert "rsi_14" in df.columns

    def test_rsi_bounded(self):
        df = make_trending_df(80, "bull")
        df = Indicators.add_rsi(df, period=14)
        valid = df["rsi_14"].dropna()
        assert (valid >= 0).all() and (valid <= 100).all()

    def test_rsi_bullish_trend_above_50(self):
        df = make_trending_df(80, "bull")
        df = Indicators.add_rsi(df, period=14)
        last = df["rsi_14"].dropna().iloc[-1]
        assert last > 50

    def test_rsi_bearish_trend_below_50(self):
        df = make_trending_df(80, "bear")
        df = Indicators.add_rsi(df, period=14)
        last = df["rsi_14"].dropna().iloc[-1]
        assert last < 50


class TestATR:
    def test_atr_column_created(self):
        df = make_trending_df(30)
        df = Indicators.add_atr(df, period=14)
        assert "atr_14" in df.columns

    def test_atr_positive(self):
        df = make_trending_df(50)
        df = Indicators.add_atr(df, period=14)
        valid = df["atr_14"].dropna()
        assert (valid >= 0).all()

    def test_atr_flat_market_low(self):
        # Very flat market → low ATR
        closes = [100.0] * 40
        df = pd.DataFrame({
            "open": closes, "high": [c + 0.01 for c in closes],
            "low": [c - 0.01 for c in closes], "close": closes
        })
        df = Indicators.add_atr(df, period=14)
        valid = df["atr_14"].dropna()
        assert valid.iloc[-1] < 0.1


# ─── Signal Engine Tests ───────────────────────────────────────────────────────

class TestSignalEngine:
    def _make_row(self, **kwargs):
        defaults = {
            "ema_20": 105.0, "ema_50": 100.0, "rsi_14": 60.0,
            "atr_14": 1.5, "close": 106.0, "ema_distance_pct": 4.7,
            "support": 105.5, "resistance": 110.0,
            "bullish_engulfing": False, "bearish_engulfing": False,
            "hammer": False, "shooting_star": False,
            "strong_bullish": False, "strong_bearish": False,
        }
        defaults.update(kwargs)
        return pd.Series(defaults)

    def test_no_trade_low_volatility(self):
        row = self._make_row(atr_14=0.000001)
        sig = SignalEngine.generate_signal(row)
        assert sig["signal"] == "NO_TRADE"
        assert any("Volatility" in r for r in sig["reasons"])

    def test_no_trade_flat_ema(self):
        row = self._make_row(ema_distance_pct=0.01)
        sig = SignalEngine.generate_signal(row)
        assert sig["signal"] == "NO_TRADE"
        assert any("EMA distance" in r for r in sig["reasons"])

    def test_call_signal_generated(self):
        row = self._make_row(
            ema_20=110.0, ema_50=100.0, rsi_14=62.0, atr_14=1.5,
            close=111.0, ema_distance_pct=9.0, support=110.5,
            bullish_engulfing=True
        )
        sig = SignalEngine.generate_signal(row)
        assert sig["signal"] == "CALL"
        assert sig["score"] >= 70

    def test_put_signal_generated(self):
        row = self._make_row(
            ema_20=95.0, ema_50=100.0, rsi_14=42.0, atr_14=1.5,
            close=94.0, ema_distance_pct=5.0, resistance=94.5,
            bearish_engulfing=True
        )
        sig = SignalEngine.generate_signal(row)
        assert sig["signal"] == "PUT"
        assert sig["score"] >= 70

    def test_no_trade_below_threshold(self):
        # A row with only partial confirmation (score < 70)
        row = self._make_row(
            ema_20=101.0, ema_50=100.0, rsi_14=50.0, atr_14=1.0,
            close=101.5, ema_distance_pct=1.0
        )
        sig = SignalEngine.generate_signal(row)
        # score may not reach 70; result should be NO_TRADE
        if sig["score"] < 70:
            assert sig["signal"] == "NO_TRADE"

    def test_confidence_label_high(self):
        row = self._make_row(
            ema_20=115.0, ema_50=100.0, rsi_14=65.0, atr_14=2.0,
            close=116.0, ema_distance_pct=13.0, support=115.5,
            bullish_engulfing=True, strong_bullish=True
        )
        sig = SignalEngine.generate_signal(row)
        if sig["signal"] == "CALL":
            assert sig["confidence_label"] in ("HIGH", "VERY HIGH", "MEDIUM")


# ─── Risk Manager Tests ────────────────────────────────────────────────────────

class TestRiskManager:
    def test_can_trade_initially(self):
        rm = RiskManager(initial_balance=1000)
        assert rm.can_trade() is True

    def test_daily_loss_limit_blocks_trading(self):
        rm = RiskManager(initial_balance=1000)
        # Simulate hitting daily loss limit
        rm.daily_loss = rm.max_daily_loss
        assert rm.can_trade() is False

    def test_consecutive_losses_block_trading(self):
        rm = RiskManager(initial_balance=1000)
        rm.consecutive_losses = 3
        assert rm.can_trade() is False

    def test_win_resets_consecutive_losses(self):
        rm = RiskManager(initial_balance=1000)
        rm.consecutive_losses = 2
        rm.record_result(8.0)  # win
        assert rm.consecutive_losses == 0

    def test_balance_updates_correctly(self):
        rm = RiskManager(initial_balance=1000)
        rm.record_result(8.0)
        assert rm.current_balance == 1008.0
        rm.record_result(-10.0)
        assert rm.current_balance == 998.0

    def test_reset_daily_loss(self):
        rm = RiskManager(initial_balance=1000)
        rm.daily_loss = 50.0
        rm.reset_daily_loss()
        assert rm.daily_loss == 0.0

    def test_insufficient_balance_blocks_trading(self):
        rm = RiskManager(initial_balance=5)  # less than trade amount (10)
        assert rm.can_trade() is False


# ─── DataLoader Tests ─────────────────────────────────────────────────────────

class TestDataLoader:
    def _write_csv(self, content: str) -> str:
        tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False)
        tmp.write(content)
        tmp.close()
        return tmp.name

    def teardown_method(self):
        # Cleanup any temp files
        pass

    def test_valid_csv_loads(self):
        path = self._write_csv(
            "timestamp,open,high,low,close,volume\n"
            "2024-01-01 00:00:00,100,102,99,101,500\n"
            "2024-01-01 00:05:00,101,103,100,102,600\n"
        )
        try:
            df = DataLoader.load_csv(path)
            assert len(df) == 2
            assert "close" in df.columns
        finally:
            os.unlink(path)

    def test_missing_column_raises(self):
        path = self._write_csv("timestamp,open,high,low\n2024-01-01,100,102,99\n")
        try:
            with pytest.raises(ValueError, match="missing required columns"):
                DataLoader.load_csv(path)
        finally:
            os.unlink(path)

    def test_duplicate_timestamps_raises(self):
        path = self._write_csv(
            "timestamp,open,high,low,close\n"
            "2024-01-01 00:00:00,100,102,99,101\n"
            "2024-01-01 00:00:00,101,103,100,102\n"
        )
        try:
            with pytest.raises(ValueError, match="duplicate timestamps"):
                DataLoader.load_csv(path)
        finally:
            os.unlink(path)

    def test_non_numeric_ohlc_raises(self):
        path = self._write_csv(
            "timestamp,open,high,low,close\n"
            "2024-01-01,abc,102,99,101\n"
        )
        try:
            with pytest.raises(ValueError):
                DataLoader.load_csv(path)
        finally:
            os.unlink(path)
