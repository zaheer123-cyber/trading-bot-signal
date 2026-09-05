import pandas as pd
import numpy as np
from typing import Dict, Any

class MetricsCalculator:
    @staticmethod
    def calculate_metrics(trades: pd.DataFrame, initial_balance: float) -> Dict[str, Any]:
        """
        Calculates trading metrics from a DataFrame of trades.
        Requires columns: 'result' (WIN/LOSS), 'profit'
        """
        if trades.empty:
            return {
                "initial_balance": initial_balance,
                "final_balance": initial_balance,
                "total_trades": 0,
                "wins": 0,
                "losses": 0,
                "win_rate": 0,
                "total_pl": 0,
                "profit_factor": 0,
                "max_drawdown": 0,
                "expectancy": 0
            }
            
        wins = trades[trades['result'] == 'WIN']
        losses = trades[trades['result'] == 'LOSS']
        
        num_wins = len(wins)
        num_losses = len(losses)
        total_trades = num_wins + num_losses
        
        win_rate = num_wins / total_trades if total_trades > 0 else 0
        
        gross_profit = wins['profit'].sum()
        gross_loss = abs(losses['profit'].sum())
        total_pl = gross_profit - gross_loss
        
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else (float('inf') if gross_profit > 0 else 0)
        
        avg_win = wins['profit'].mean() if num_wins > 0 else 0
        avg_loss = abs(losses['profit'].mean()) if num_losses > 0 else 0
        
        expectancy = (win_rate * avg_win) - ((1 - win_rate) * avg_loss)
        
        # Calculate Drawdown
        trades['cumulative_profit'] = trades['profit'].cumsum()
        trades['equity'] = initial_balance + trades['cumulative_profit']
        trades['peak'] = trades['equity'].cummax()
        trades['drawdown'] = trades['peak'] - trades['equity']
        max_drawdown = trades['drawdown'].max()
        
        return {
            "initial_balance": initial_balance,
            "final_balance": initial_balance + total_pl,
            "total_trades": total_trades,
            "wins": num_wins,
            "losses": num_losses,
            "win_rate": round(win_rate * 100, 2),
            "total_pl": round(total_pl, 2),
            "profit_factor": round(profit_factor, 2),
            "max_drawdown": round(max_drawdown, 2),
            "expectancy": round(expectancy, 2)
        }
