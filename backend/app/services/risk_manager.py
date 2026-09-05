from app.config import settings

class RiskManager:
    def __init__(self, initial_balance: float = settings.INITIAL_BALANCE):
        self.initial_balance = initial_balance
        self.current_balance = initial_balance
        self.daily_loss = 0.0
        self.trade_amount = settings.TRADE_AMOUNT
        self.max_daily_loss = settings.MAX_DAILY_LOSS
        self.consecutive_losses = 0
        
    def reset_daily_loss(self):
        self.daily_loss = 0.0
        
    def can_trade(self) -> bool:
        """
        Checks if a trade can be executed based on risk parameters.
        """
        if self.current_balance < self.trade_amount:
            return False
            
        if self.daily_loss >= self.max_daily_loss:
            return False
            
        if self.consecutive_losses >= 3:
            # Simple cooldown logic: require manual reset or waiting for next period (mocked)
            # In a real system, you might track time since last trade.
            return False
            
        return True
        
    def record_result(self, profit: float):
        """
        Updates balance and risk metrics after a trade.
        """
        self.current_balance += profit
        
        if profit < 0:
            self.daily_loss += abs(profit)
            self.consecutive_losses += 1
        else:
            self.consecutive_losses = 0
