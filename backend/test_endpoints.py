import urllib.request
import json

endpoints = [
    ("Health", "http://127.0.0.1:8000/api/health"),
    ("Candles", "http://127.0.0.1:8000/api/market/candles"),
    ("Signal", "http://127.0.0.1:8000/api/signals/latest"),
]

for name, url in endpoints:
    try:
        res = urllib.request.urlopen(url, timeout=5)
        data = json.loads(res.read())
        if name == "Candles":
            count = len(data.get("candles", []))
            print(f"[OK] {name}: {count} candles returned")
        elif name == "Signal":
            sig = data.get("signal")
            score = data.get("score")
            trend = data.get("trend")
            rsi = data.get("rsi")
            reasons = data.get("reasons", [])
            print(f"[OK] {name}: signal={sig}, score={score}, trend={trend}, rsi={rsi}, reasons={len(reasons)}")
        else:
            print(f"[OK] {name}: {data}")
    except Exception as e:
        print(f"[FAIL] {name}: {e}")
