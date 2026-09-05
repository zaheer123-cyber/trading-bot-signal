import pandas as pd
import numpy as np

class Indicators:
    @staticmethod
    def add_ema(df: pd.DataFrame, column: str = 'close', period: int = 20) -> pd.DataFrame:
        """
        Adds Exponential Moving Average to the DataFrame.
        """
        df[f'ema_{period}'] = df[column].ewm(span=period, adjust=False).mean()
        return df
        
    @staticmethod
    def add_rsi(df: pd.DataFrame, column: str = 'close', period: int = 14) -> pd.DataFrame:
        """
        Adds Relative Strength Index to the DataFrame.
        """
        delta = df[column].diff()
        gain = (delta.where(delta > 0, 0)).fillna(0)
        loss = (-delta.where(delta < 0, 0)).fillna(0)
        
        avg_gain = gain.rolling(window=period, min_periods=period).mean()
        avg_loss = loss.rolling(window=period, min_periods=period).mean()
        
        # Smoothing (Wilder's smoothing)
        for i in range(period, len(df)):
            avg_gain.iloc[i] = (avg_gain.iloc[i-1] * (period - 1) + gain.iloc[i]) / period
            avg_loss.iloc[i] = (avg_loss.iloc[i-1] * (period - 1) + loss.iloc[i]) / period
            
        rs = avg_gain / avg_loss
        df[f'rsi_{period}'] = 100 - (100 / (1 + rs))
        
        # Handle division by zero for avg_loss = 0
        df.loc[avg_loss == 0, f'rsi_{period}'] = 100
        
        return df
        
    @staticmethod
    def add_atr(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
        """
        Adds Average True Range to the DataFrame.
        """
        high_low = df['high'] - df['low']
        high_close = np.abs(df['high'] - df['close'].shift())
        low_close = np.abs(df['low'] - df['close'].shift())
        
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = np.max(ranges, axis=1)
        
        # Simple moving average of True Range for ATR
        df[f'atr_{period}'] = true_range.rolling(window=period, min_periods=period).mean()
        return df
