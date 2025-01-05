import { useState, useEffect } from "react";
import "./App.css";
import AddStock from "./templates/AddStock";
import StockTable from "./templates/StockTable";
import Header from "./templates/Header";
import HighlightCard from "./templates/HighlightCard";

function App() {
  const [stocks, setStocks] = useState([]);
  const [quantity, setQuantity] = useState(0);
  const [ticker, setTicker] = useState("");
  const calculateTotalProfit = () => {
    return stocks.reduce((total, stock) => total + ((stock.currentPrice - stock.buy_price)*stock.quantity || 0), 0);
  };
  const calculateNetProfit = () => {
    
    var totalInvestment= stocks.reduce((total, stock) => total + (stock.buy_price || 0), 0);
    var totalProfit= stocks.reduce((total, stock) => total + ((stock.currentPrice - stock.buy_price)*stock.quantity || 0), 0);
    if (totalInvestment === 0) return 0;
    const net= (totalProfit*100/totalInvestment).toFixed(2)
    return `${net}%`
  };
  const calculateTotalInvestment = () => {
    
    return stocks.reduce((total, stock) => total + ((stock.buy_price)*stock.quantity || 0), 0);}

  const calculateTotalCash = () => {
    
    return stocks.reduce((total, stock) => total + (stock.currentPrice)*stock.quantity, 0);
    
  };
  useEffect(() => {
    fetchStocks();
  }, []);

  const fetchStocks = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/api/stocks/");
      const data = await response.json();
      const updatedStocks = await Promise.all(data.map(async (stock) => {
        const prediction = await getPrediction(stock.ticker);
        return { ...stock, prediction: prediction };
        }));
      // data['prediction']=await getPrediction(data['ticker'])

      setStocks(updatedStocks);
    } catch (err) {
      console.log(err);
    }
  };

  const addStock = async (e) => {
    e.preventDefault();
    try {
      const stockData = { ticker, quantity };
      const response = await fetch("http://127.0.0.1:8000/api/stocks/create/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(stockData),
      });
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      const data = await response.json();
      setStocks((prev) => [...prev, data]);
      fetchStocks();
    } catch (err) {
      console.log(err);
    }
  };

  const getPrediction = async (tickerSymbol) => {
    const payload={
      ticker: tickerSymbol,
    }
    try {
      const response = await fetch("http://127.0.0.1:8000/api/stocks/predict/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      const data = await response.json();
      console.log(data)
      return data.predicted_price
    } catch (err) {
      console.log(err);
    }
  };

  const updateStock = async (pk, num) => {
    try {
      const stockData = { ticker, quantity: num };
      const response = await fetch(`http://127.0.0.1:8000/api/stocks/update/${pk}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(stockData),
      });
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      const data = await response.json();
      setStocks((prev) =>
        prev.map((stock) => (stock.pk === pk ? data : stock))
      );
      fetchStocks();
    } catch (err) {
      console.log(err);
    }
  };

  const deleteStock = async (pk) => {
    try {
      await fetch(`http://127.0.0.1:8000/api/stocks/delete/${pk}`, {
        method: "DELETE",
      });
      setStocks((prev) => prev.filter((stock) => stock.id !== pk));
      fetchStocks();
    } catch (err) {
      console.log(err);
    }
  };

  return (
    <>
    <div className="header">

<Header/>
</div>

    <div className="primary">
      <HighlightCard title="NET RETURN" value={calculateNetProfit()}/>
      <HighlightCard title="TOTAL PROFIT" value={calculateTotalProfit()}/>
      <HighlightCard title="TOTAL INVESTMENT" value={calculateTotalInvestment()}/>
      <HighlightCard title="TOTAL CASH" value={calculateTotalCash()}/>
      
    </div>
    <div id="main">
      
      <div id="AddStock">
      <AddStock
        ticker={ticker}
        quantity={quantity}
        setTicker={setTicker}
        setQuantity={setQuantity}
        addStock={addStock}
      /></div>
      <StockTable
        stocks={stocks}
        deleteStock={deleteStock}
        updateStock={updateStock}
        getPrediction={getPrediction}
      />
      </div>
    </>
  );
}

export default App;
