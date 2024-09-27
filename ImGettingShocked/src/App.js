import React, { useEffect, useState } from 'react';
import './App.css';

function App() {
  const [data, setData] = useState({ temperature: null, redLED: null, irLED: null });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://<REPLACEWITHPIRASBERRYIPADRESS>:5000/data');
        const result = await response.json();
        setData(result);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 5000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Sensor Data</h1>
        <p>Temperature: {data.temperature !== null ? `${data.temperature} °C` : 'Loading...'}</p>
        <p>Red LED: {data.redLED !== null ? data.redLED : 'Loading...'}</p>
        <p>IR LED: {data.irLED !== null ? data.irLED : 'Loading...'}</p>
      </header>
    </div>
  );
}

export default App;
