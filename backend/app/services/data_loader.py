import pandas as pd
from typing import Optional

class DataLoader:
    @staticmethod
    def load_csv(filepath: str) -> pd.DataFrame:
        """
        Loads a CSV file and validates it.
        Expected format: timestamp, open, high, low, close [, volume]
        """
        try:
            df = pd.read_csv(filepath)
        except Exception as e:
            raise ValueError(f"Failed to read CSV: {str(e)}")
            
        required_cols = {'timestamp', 'open', 'high', 'low', 'close'}
        cols = {c.lower() for c in df.columns}
        
        if not required_cols.issubset(cols):
            missing = required_cols - cols
            raise ValueError(f"Dataset missing required columns: {missing}")

        # Standardize column names to lowercase
        df.columns = [c.lower() for c in df.columns]

        # Convert timestamp
        try:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        except Exception:
            raise ValueError("Invalid timestamp format in dataset.")

        # Check for missing values
        if df[['open', 'high', 'low', 'close']].isnull().any().any():
            raise ValueError("Dataset contains missing OHLC values.")

        # Ensure correct data types
        for col in ['open', 'high', 'low', 'close']:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        if df[['open', 'high', 'low', 'close']].isnull().any().any():
            raise ValueError("Dataset contains non-numeric OHLC values.")

        # Sort by timestamp to prevent look-ahead issues
        df = df.sort_values(by='timestamp').reset_index(drop=True)
        
        # Check for duplicate timestamps
        if df['timestamp'].duplicated().any():
            raise ValueError("Dataset contains duplicate timestamps.")

        return df
