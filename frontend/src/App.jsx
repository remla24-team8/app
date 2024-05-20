import React, { useState, useEffect } from 'react';

function App() {
  const [version, setVersion] = useState('');
  const [prediction, setPrediction] = useState(null);
  const [inputData, setInputData] = useState('');

  useEffect(() => {
    fetch('/version')
      .then(response => response.json())
      .then(data => setVersion(data.version));
  }, []);

  const handlePredict = () => {
    fetch('/api/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ input: inputData })
    })
      .then(response => response.json())
      .then(data => setPrediction(data));
  };

  return (
    <div>
      <h1>App Version: {version}</h1>
      <input
        type="text"
        value={inputData}
        onChange={e => setInputData(e.target.value)}
        placeholder="Enter input data"
      />
      <button onClick={handlePredict}>Predict</button>
      {prediction && <pre>{JSON.stringify(prediction, null, 2)}</pre>}
    </div>
  );
}

export default App;
