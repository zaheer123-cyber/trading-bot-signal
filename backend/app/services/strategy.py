import pandas as pd
from app.services.indicators import Indicators
from app.services.support_resistance import SupportResistance
from app.services.candle_patterns import CandlePatterns
from app.config import settings

class Strategy:
    @staticmethod
    def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
        """
        Enriches the dataframe with all necessary indicators for the strategy.
        """
        # Indicators
        df = Indicators.add_ema(df, period=settings.EMA_FAST)
        df = Indicators.add_ema(df, period=settings.EMA_SLOW)
        df = Indicators.add_rsi(df, period=settings.RSI_PERIOD)
        df = Indicators.add_atr(df, period=settings.ATR_PERIOD)
        
        # Support / Resistance
        df = SupportResistance.identify_sr(df, window=5)
        
        # Candle Patterns
        df = CandlePatterns.detect_patterns(df)
        
        # Calculate EMA distance percentage
        ema_fast_col = f'ema_{settings.EMA_FAST}'
        ema_slow_col = f'ema_{settings.EMA_SLOW}'
        
        df['ema_distance_pct'] = (abs(df[ema_fast_col] - df[ema_slow_col]) / df['close']) * 100
        
        return df
