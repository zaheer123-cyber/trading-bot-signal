import pandas as pd
from app.services.strategy import Strategy
from app.services.signal_engine import SignalEngine
from app.services.risk_manager import RiskManager
from app.config import settings
from typing import List, Dict, Any

class Backtester:
    def __init__(self, df: pd.DataFrame):
        self.df = Strategy.prepare_data(df)
        self.risk_manager = RiskManager()
        self.trades: List[Dict[str, Any]] = []
        
    def run(self) -> pd.DataFrame:
        """
        Event-driven backtest simulation.
        Iterates over the dataframe to prevent look-ahead bias.
        """
        expiry = settings.EXPIRY_CANDLES
        
        for i in range(len(self.df) - expiry):
            row = self.df.iloc[i]
            
            # Reset daily loss on new day
            if i > 0 and self.df.iloc[i]['timestamp'].date() != self.df.iloc[i-1]['timestamp'].date():
                self.risk_manager.reset_daily_loss()
                
            signal_data = SignalEngine.generate_signal(row)
            
            if signal_data['signal'] in ['CALL', 'PUT']:
                if self.risk_manager.can_trade():
                    self._execute_paper_trade(i, row, signal_data, expiry)
                    
        return pd.DataFrame(self.trades)
        
    def _execute_paper_trade(self, index: int, row: pd.Series, signal_data: Dict[str, Any], expiry: int):
        entry_price = row['close']
        exit_candle = self.df.iloc[index + expiry]
        exit_price = exit_candle['close']
        
        signal = signal_data['signal']
        
        # Determine outcome
        result = "TIE"
        profit = 0.0
        
        if signal == "CALL":
            if exit_price > entry_price:
                result = "WIN"
                profit = self.risk_manager.trade_amount * settings.PAYOUT
            elif exit_price < entry_price:
                result = "LOSS"
                profit = -self.risk_manager.trade_amount
        elif signal == "PUT":
            if exit_price < entry_price:
                result = "WIN"
                profit = self.risk_manager.trade_amount * settings.PAYOUT
            elif exit_price > entry_price:
                result = "LOSS"
                profit = -self.risk_manager.trade_amount
                
        self.risk_manager.record_result(profit)
        
        self.trades.append({
            "timestamp": row['timestamp'],
            "signal": signal,
            "score": signal_data['score'],
            "entry_price": entry_price,
            "exit_price": exit_price,
            "result": result,
            "profit": profit
        })
