import React, { useState } from 'react';
import './index.css';

function App() {
  const [selectedRegion, setSelectedRegion] = useState('West');
  const [selectedYear, setSelectedYear] = useState(2024);
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);

  const regions = ['Northeast', 'Midwest', 'South', 'West', 'Pacific', 'Mountain'];
  const years = Array.from({ length: 26 }, (_, i) => 1998 + i);

  const handlePredict = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          year: selectedYear,
          region: selectedRegion,
          geographic_mean_pm25: 12.5,
          population_coverage: 95,
          geographic_coverage: 92,
          pop_pct_5: 85,
          pop_pct_10: 65,
          pop_pct_15: 35
        })
      });
      const data = await response.json();
      setPrediction(data);
    } catch (error) {
      console.error('Error:', error);
      setPrediction({ error: 'Failed to get prediction' });
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">PM2.5 Analytics</h1>
          <p className="text-gray-600">Machine Learning Pollution Prediction System</p>
        </div>

        {/* Control Panel */}
        <div className="bg-white rounded-2xl shadow-lg p-8 mb-8 backdrop-blur-xl bg-opacity-80">
          <h2 className="text-2xl font-bold mb-6 text-gray-800">Prediction Controls</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Select Region</label>
              <select
                value={selectedRegion}
                onChange={(e) => setSelectedRegion(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
              >
                {regions.map(r => <option key={r} value={r}>{r}</option>)}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Select Year</label>
              <select
                value={selectedYear}
                onChange={(e) => setSelectedYear(parseInt(e.target.value))}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
              >
                {years.map(y => <option key={y} value={y}>{y}</option>)}
              </select>
            </div>
          </div>
          <button
            onClick={handlePredict}
            disabled={loading}
            className="mt-6 w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-bold py-3 px-6 rounded-lg transition duration-200"
          >
            {loading ? 'Predicting...' : 'Get Prediction'}
          </button>
        </div>

        {/* Results */}
        {prediction && (
          <div className="bg-white rounded-2xl shadow-lg p-8 backdrop-blur-xl bg-opacity-80">
            <h2 className="text-2xl font-bold mb-6 text-gray-800">Prediction Results</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl p-6 text-white">
                <p className="text-sm opacity-90">Predicted PM2.5</p>
                <p className="text-4xl font-bold">{prediction.predicted_pm25?.toFixed(2) || 'N/A'} μg/m³</p>
              </div>
              <div className="bg-gradient-to-br from-green-500 to-green-600 rounded-xl p-6 text-white">
                <p className="text-sm opacity-90">Air Quality</p>
                <p className="text-2xl font-bold">{prediction.confidence || 'N/A'}</p>
              </div>
            </div>
            <div className="mt-6 p-4 bg-gray-50 rounded-lg">
              <p className="text-sm text-gray-600"><strong>Region:</strong> {prediction.region}</p>
              <p className="text-sm text-gray-600"><strong>Year:</strong> {prediction.year}</p>
              <p className="text-sm text-gray-600"><strong>Model:</strong> {prediction.model_name}</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
