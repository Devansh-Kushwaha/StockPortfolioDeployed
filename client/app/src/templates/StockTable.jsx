import React from "react";
import "./css/stocktable.css";
function StockTable({ stocks, deleteStock, updateStock,getPrediction }) {
  return (
    <div id="stockTable">
      <table>
        <thead>
          <tr>
            <th>TICKER</th>
            <th>NAME</th>
            <th>BUY PRICE</th>
            <th>QUANTITY</th>
            <th>CURRENT PRICE</th>
            <th id="predictionhead">PREDICTED PRICE</th>
            <th>CURRENT PROFIT</th>
          </tr>
        </thead>
        <tbody>
          {stocks.map((stock) => (
            <tr key={stock.id}>
              <td>
                <button onClick={() => deleteStock(stock.id)}>DEL</button>
                {stock.ticker}
              </td>
              <td>{stock.name}</td>
              <td>${stock.buy_price}</td>
              <td>
                <button onClick={() => updateStock(stock.id, stock.quantity - 1)}>-</button>
                {stock.quantity}
                <button onClick={() => updateStock(stock.id, stock.quantity + 1)}>+</button>
              </td>
              <td>{stock.currentPrice}</td>
              <td id="predictiondata">${stock.prediction !== null
                  ? `$${stock.prediction.toFixed(2)}`
                  : "Loading..."}</td>
              <td>
                ${((stock.currentPrice - stock.buy_price) * stock.quantity).toFixed(2)}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default StockTable;
