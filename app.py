node -v
npm -v
npm create vite@latest market-terminal -- --template react
cd market-terminal
npm install
npm install lightweight-charts react-resizable
market-terminal/src/App.jsx
import React, { useEffect, useRef, useState } from "react";
import { createChart } from "lightweight-charts";
import "./App.css";

export default function App() {
  const chartContainerRef = useRef();
  const [rightWidth, setRightWidth] = useState(300);

  useEffect(() => {
    const chart = createChart(chartContainerRef.current, {
      layout: {
        background: { color: "#0e1117" },
        textColor: "#d1d4dc",
      },
      grid: {
        vertLines: { color: "#1e222d" },
        horzLines: { color: "#1e222d" },
      },
      width: chartContainerRef.current.clientWidth,
      height: chartContainerRef.current.clientHeight,
    });

    const candleSeries = chart.addCandlestickSeries();

    const data = [];
    let price = 100;

    for (let i = 0; i < 200; i++) {
      const open = price;
      const close = open + (Math.random() - 0.5) * 4;
      const high = Math.max(open, close) + Math.random() * 2;
      const low = Math.min(open, close) - Math.random() * 2;

      data.push({
        time: i,
        open,
        high,
        low,
        close,
      });

      price = close;
    }

    candleSeries.setData(data);

    window.addEventListener("resize", () => {
      chart.applyOptions({
        width: chartContainerRef.current.clientWidth,
        height: chartContainerRef.current.clientHeight,
      });
    });

    return () => chart.remove();
  }, []);

  return (
    <div className="app">
      <div className="top-bar">
        MARKET LOGIC TERMINAL
      </div>

      <div className="main">
        <div className="chart-area" ref={chartContainerRef} />

        <div
          className="right-panel"
          style={{ width: rightWidth }}
        >
          <div className="panel-section">
            <h3>Structure</h3>
            <p>Bias: BULLISH</p>
            <p>Swings: 5 / 4</p>
          </div>

          <div className="panel-section">
            <h3>Liquidity</h3>
            <p>Equal High: ❌</p>
            <p>Equal Low: ✅</p>
          </div>

          <div className="panel-section">
            <h3>Trade Panel</h3>
            <button>BUY</button>
            <button>SELL</button>
          </div>

          <div className="panel-section">
            <h3>Positions</h3>
            <p>No open positions</p>
          </div>
        </div>
      </div>

      <div className="bottom-dock">
        <div>Positions</div>
        <div>Orders</div>
        <div>Journal</div>
        <div>Performance</div>
      </div>
    </div>
  );
}
market-terminal/src/App.css
body {
  margin: 0;
  background: #0e1117;
  color: #d1d4dc;
  font-family: Arial, sans-serif;
}

.app {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.top-bar {
  padding: 10px;
  background: #161a23;
  font-weight: bold;
  border-bottom: 1px solid #1e222d;
}

.main {
  display: flex;
  flex: 1;
}

.chart-area {
  flex: 1;
}

.right-panel {
  background: #161a23;
  border-left: 1px solid #1e222d;
  padding: 10px;
  overflow-y: auto;
}

.panel-section {
  margin-bottom: 20px;
}

.panel-section h3 {
  margin-top: 0;
}

.panel-section button {
  margin-right: 5px;
  background: #2962ff;
  border: none;
  color: white;
  padding: 6px 10px;
  cursor: pointer;
}

.bottom-dock {
  display: flex;
  background: #161a23;
  border-top: 1px solid #1e222d;
}

.bottom-dock div {
  padding: 10px;
  border-right: 1px solid #1e222d;
  cursor: pointer;
}
npm run dev
http://localhost:5173
