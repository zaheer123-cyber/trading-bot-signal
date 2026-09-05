import pandas as pd
import numpy as np

class SupportResistance:
    @staticmethod
    def identify_sr(df: pd.DataFrame, window: int = 5) -> pd.DataFrame:
        """
        Identifies recent swing highs (resistance) and swing lows (support).
        window: number of candles before and after to consider a point a local extrema.
        """
        df['support'] = np.nan
        df['resistance'] = np.nan
        
        for i in range(window, len(df) - window):
            # Check for swing high
            if df['high'].iloc[i] == max(df['high'].iloc[i-window:i+window+1]):
                df.at[df.index[i], 'resistance'] = df['high'].iloc[i]
                
            # Check for swing low
            if df['low'].iloc[i] == min(df['low'].iloc[i-window:i+window+1]):
                df.at[df.index[i], 'support'] = df['low'].iloc[i]
                
        # Forward fill the support and resistance levels so we know the most recent ones
        df['support'] = df['support'].ffill()
        df['resistance'] = df['resistance'].ffill()
        
        return df
