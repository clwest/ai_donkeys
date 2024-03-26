"use client";

import { useState, useEffect } from "react";
import styles from "./ticker.module.css";

export default function Ticker() {
  const [tokens, setTokens] = useState([]);
  const [error, setError] = useState(null);

  const fetchTokens = async () => {
    try {
      const res = await fetch("/api/coingecko/coins");
      const tokenInfo = await res.json();

      if (!Array.isArray(tokenInfo)) {
        setError("Unexpected response format from API");
        return;
      }

      setTokens(tokenInfo);
    } catch (error) {
      console.error("Error fetching tokens:", error);
      setError("Failed to fetch tokens");
    }
  };

  useEffect(() => {
    fetchTokens();
  }, []);

  return (
    <div
      className={`${styles["ticker-container"]} p-4 m-2 text-center border border-cyan-500 shadow-md rounded-md`}
    >
      {error ? (
        <div>{error}</div>
      ) : (
        <div className="whitespace-nowrap overflow-x-auto">
          <h2 className={`${styles["ticker"]} inline-flex space-x-4`}>
            {tokens.map((token) => (
              <span
                key={token.symbol}
                className="inline-flex items-center space-x-2"
              >
                <span>
                  {token.symbol.toUpperCase()}: ${token.price}
                </span>
                <span>
                  {token.change24h > 0 ? (
                    <span className="text-green-500">↑</span>
                  ) : (
                    <span className="text-red-500">↓</span>
                  )}
                  {token.change24h}%
                </span>
              </span>
            ))}
          </h2>
        </div>
      )}
    </div>
  );
}
