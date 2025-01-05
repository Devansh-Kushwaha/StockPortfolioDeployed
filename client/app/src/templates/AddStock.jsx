import React from "react";
import "./css/addstock.css";
function AddStock({ ticker, quantity, setTicker, setQuantity, addStock }) {
  return (
    <div id="addStock">
      <h1>Add Stock</h1>
      <form>
        <div id="tickerlabeldiv">
          <label htmlFor="ticker" id="tickerlabel">TICKER:</label>
        </div>
        <div>
          <input
            id="ticker"
            type="text"
            placeholder="TKR..."
            required
            value={ticker}
            onChange={(e) => setTicker(e.target.value)}
          />
        </div>
        <div id='quantitySection'>
            <div>
          <label htmlFor="quantity">Quantity:</label></div>
          <div>
          <input
            id="quantity"
            type="number"
            required
            value={quantity}
            onChange={(e) => setQuantity(e.target.value)}
          /></div>
        </div>
        <button type="submit" onClick={addStock}>
          Add Stock
        </button>
      </form>
    </div>
  );
}

export default AddStock;
