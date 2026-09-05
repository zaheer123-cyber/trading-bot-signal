import pandas as pd

class CandlePatterns:
    @staticmethod
    def detect_patterns(df: pd.DataFrame) -> pd.DataFrame:
        """
        Detects basic candlestick patterns:
        - Bullish/Bearish Engulfing
        - Hammer
        - Shooting Star
        - Strong Bullish/Bearish Candle
        """
        # Calculate candle components
        df['body'] = df['close'] - df['open']
        df['abs_body'] = df['body'].abs()
        df['upper_shadow'] = df['high'] - df[['open', 'close']].max(axis=1)
        df['lower_shadow'] = df[['open', 'close']].min(axis=1) - df['low']
        df['range'] = df['high'] - df['low']
        
        # Previous candle components
        df['prev_body'] = df['body'].shift(1)
        df['prev_close'] = df['close'].shift(1)
        df['prev_open'] = df['open'].shift(1)
        
        # Bullish Engulfing
        df['bullish_engulfing'] = (
            (df['prev_body'] < 0) & 
            (df['body'] > 0) & 
            (df['close'] > df['prev_open']) & 
            (df['open'] < df['prev_close'])
        )
        
        # Bearish Engulfing
        df['bearish_engulfing'] = (
            (df['prev_body'] > 0) & 
            (df['body'] < 0) & 
            (df['close'] < df['prev_open']) & 
            (df['open'] > df['prev_close'])
        )
        
        # Hammer (small body, long lower shadow, little to no upper shadow)
        df['hammer'] = (
            (df['lower_shadow'] > 2 * df['abs_body']) & 
            (df['upper_shadow'] < 0.2 * df['abs_body']) &
            (df['body'] > 0) # Preferably bullish
        )
        
        # Shooting Star (small body, long upper shadow, little to no lower shadow)
        df['shooting_star'] = (
            (df['upper_shadow'] > 2 * df['abs_body']) & 
            (df['lower_shadow'] < 0.2 * df['abs_body']) &
            (df['body'] < 0) # Preferably bearish
        )
        
        # Strong Bullish Candle
        df['strong_bullish'] = (
            (df['body'] > 0.7 * df['range']) & 
            (df['range'] > df['range'].rolling(10).mean())
        )
        
        # Strong Bearish Candle
        df['strong_bearish'] = (
            (df['abs_body'] > 0.7 * df['range']) & 
            (df['body'] < 0) &
            (df['range'] > df['range'].rolling(10).mean())
        )
        
        return df
