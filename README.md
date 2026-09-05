# Trading Signal & Backtesting Platform

A modular, production-quality trading signal generation, backtesting, and paper trading platform.

> [!WARNING]
> This is a **research and manual decision support tool**. It does not perform automated execution, it does not connect to real brokerages, and it does not guarantee any win rate. Past performance in backtests does not guarantee future results.

## Overview

This application provides a full-stack environment to test, validate, and simulate trading strategies using technical indicators and price action patterns.

### Core Technologies
- **Backend:** Python 3.11+, FastAPI, Pandas, NumPy, SQLAlchemy, SQLite
- **Frontend:** React, TypeScript, Vite, Tailwind CSS
- **Data:** CSV file ingestion

## Strategy

The default strategy combines multiple confirmations into a score out of 100:
1. **Trend (25 pts):** EMA Fast (20) / EMA Slow (50) separation
2. **Momentum (20 pts):** RSI (14) confirmation and bounds checking
3. **Levels (15 pts):** Proximity to recent Support/Resistance swing points
4. **Patterns (20 pts):** Candlestick patterns (e.g. Bullish Engulfing)
5. **Volatility (10 pts):** ATR (14) minimum limits
6. **Structure (10 pts):** Price relation to EMA

If the final score is >= 70, a CALL or PUT signal is generated. Otherwise, NO TRADE.

## Getting Started

### 1. Backend Setup
```bash
cd backend
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
cp ../.env.example .env
uvicorn app.main:app --reload
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## Features
- **Look-Ahead Bias Prevention**: Backtesting iterates candle by candle to ensure future data is never used.
- **Risk Management**: Enforces max daily loss, fixed trade amounts, and cool-down periods.
- **Paper Trading Engine**: Real-time simulation of signals without risking actual capital.

## Data Input Format
The system accepts CSV files with the following columns (case-insensitive):
`timestamp, open, high, low, close, volume`
