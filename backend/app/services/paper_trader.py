from app.config import settings
from app.services.risk_manager import RiskManager
import datetime
from typing import Dict, Any

class PaperTrader:
    def __init__(self):
        self.risk_manager = RiskManager()
        self.active_trades = []
        self.trade_history = []
        
    def execute_signal(self, signal: Dict[str, Any], current_price: float, timestamp: datetime.datetime):
        if signal['signal'] not in ['CALL', 'PUT']:
            return {"status": "ignored", "reason": "No actionable signal"}
            
        if not self.risk_manager.can_trade():
            return {"status": "rejected", "reason": "Risk limits reached"}
            
        trade = {
            "id": len(self.trade_history) + len(self.active_trades) + 1,
            "signal": signal['signal'],
            "entry_price": current_price,
            "entry_time": timestamp,
            "stake": self.risk_manager.trade_amount,
            "status": "OPEN",
            "score": signal['score']
        }
        
        self.active_trades.append(trade)
        return {"status": "executed", "trade": trade}
        
    def check_expiries(self, current_price: float, timestamp: datetime.datetime):
        # Simplified: close all open trades on next call (assuming 1-candle expiry)
        closed = []
        for trade in self.active_trades:
            trade['exit_price'] = current_price
            trade['exit_time'] = timestamp
            trade['status'] = "CLOSED"
            
            # Determine result
            if trade['signal'] == 'CALL':
                if current_price > trade['entry_price']:
                    trade['result'] = 'WIN'
                    trade['profit'] = trade['stake'] * settings.PAYOUT
                else:
                    trade['result'] = 'LOSS'
                    trade['profit'] = -trade['stake']
            elif trade['signal'] == 'PUT':
                if current_price < trade['entry_price']:
                    trade['result'] = 'WIN'
                    trade['profit'] = trade['stake'] * settings.PAYOUT
                else:
                    trade['result'] = 'LOSS'
                    trade['profit'] = -trade['stake']
            else:
                trade['result'] = 'TIE'
                trade['profit'] = 0
                
            self.risk_manager.record_result(trade['profit'])
            self.trade_history.append(trade)
            closed.append(trade)
            
        self.active_trades = []
        return closed
