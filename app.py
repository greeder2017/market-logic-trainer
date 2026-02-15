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
