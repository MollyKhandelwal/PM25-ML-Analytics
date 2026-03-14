# PM2.5 Machine Learning Analytics System

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)
![React](https://img.shields.io/badge/React-18+-61dafb.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🎯 Project Overview

A complete end-to-end Machine Learning analytics system for **PM2.5 pollution prediction**. This project includes:

- **Exploratory Data Analysis (EDA)** - Understanding PM2.5 trends, regional patterns, and population exposure
- **ML Model Training** - Random Forest, XGBoost, and Linear Regression models
- **FastAPI Backend** - RESTful API for real-time PM2.5 predictions
- **React Frontend** - Modern, interactive analytics dashboard with TailwindCSS
- **Data Visualizations** - Charts showing trends, regional comparisons, and exposure metrics

## 📊 Dataset

**UnitedStatesPM25-V6GL0203-Annual-REGIONAL-1998-2023**

Columns:
- Region (Northeast, Midwest, South, West, Pacific, Mountain)
- Year (1998-2023)
- Population-Weighted PM2.5 (ug/m³) - **Target Variable**
- Geographic-Mean PM2.5 (ug/m³)
- Population Coverage (%)
- Geographic Coverage (%)
- Population Exposure Percentages at different PM2.5 thresholds

## 🚀 Quick Start

### Prerequisites
```bash
- Python 3.8+
- Node.js 16+
- npm or yarn
```

### 1. Clone Repository
```bash
git clone https://github.com/MollyKhandelwal/PM25-ML-Analytics.git
cd PM25-ML-Analytics
```

### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app:app --reload
```
Server runs on: `http://localhost:8000`

### 3. Frontend Setup
```bash
cd frontend
npm install
npm start
```
Dashboard runs on: `http://localhost:3000`

### 4. Run EDA & Model Training
Open `notebooks/01_EDA_and_ML_Training.ipynb` in Google Colab and run all cells.

## 📁 Project Structure

```
pm25-ml-analytics/
├── notebooks/
│   └── 01_EDA_and_ML_Training.ipynb    # EDA & model training notebook
├── backend/
│   ├── app.py                          # FastAPI application
│   ├── schemas.py                      # Pydantic models
│   └── requirements.txt                # Python dependencies
├── frontend/
│   ├── package.json                    # Node dependencies
│   ├── src/
│   │   ├── App.jsx                     # Main React component
│   │   ├── components/
│   │   │   ├── Dashboard.jsx           # Dashboard component
│   │   │   └── PredictionCard.jsx      # Prediction display
│   │   └── index.css                   # Tailwind styles
│   └── tailwind.config.js              # Tailwind configuration
├── dataset/
│   └── pm25_sample_data.csv            # Sample dataset
├── model/
│   └── model.pkl                       # Trained ML model
├── README.md
└── requirements.txt                    # All dependencies
```

## 🔬 Step 1: Exploratory Data Analysis

### Analysis Performed:
1. **Data Summary** - Shape, dtypes, missing values
2. **Correlation Analysis** - Feature relationships with target variable
3. **PM2.5 Trends** - Historical pollution patterns (1998-2023)
4. **Regional Comparison** - State-wise pollution levels
5. **Population Exposure** - Demographics exposed to different PM2.5 thresholds
6. **Visualizations** - Time series, bar charts, heatmaps

### Key Findings:
- PM2.5 levels show declining trend over 25 years
- Regional variations: West region has highest pollution
- Population exposure increases with higher PM2.5 thresholds

## 🤖 Step 2: Machine Learning Models

### Models Trained:
1. **Linear Regression** - Baseline model
2. **Random Forest** - Ensemble learning (100 trees)
3. **XGBoost** - Gradient boosting (100 estimators)

### Model Evaluation:
```
Metrics Used:
- Mean Absolute Error (MAE)
- Root Mean Squared Error (RMSE)
- R² Score
```

### Best Model Selection:
Automatic selection based on highest R² score on test set.

## ⚙️ Step 3: FastAPI Backend

### Endpoint: `POST /predict`

**Request:**
```json
{
  "year": 2024,
  "region": "West",
  "geographic_mean_pm25": 12.5,
  "population_coverage": 95.0,
  "geographic_coverage": 92.0,
  "pop_pct_5": 85.0,
  "pop_pct_10": 65.0,
  "pop_pct_15": 35.0
}
```

**Response:**
```json
{
  "predicted_pm25": 10.25,
  "region": "West",
  "year": 2024,
  "model_name": "Random Forest"
}
```

### Features:
- Input validation with Pydantic
- Error handling
- CORS enabled
- Model loading with caching

## 🎨 Step 4: React Frontend Dashboard

### Features:
- **Modern UI** - Apple/Stripe style with glassmorphism cards
- **Data Visualizations** - Chart.js/Recharts integration
- **Interactive Controls** - Region and year selectors
- **Responsive Design** - Mobile-friendly with TailwindCSS
- **Prediction Display** - Real-time PM2.5 predictions

### Dashboard Components:
1. Header with project title
2. Region and Year selection dropdowns
3. Current PM2.5 level card
4. Historical trend chart
5. Regional comparison chart
6. Population exposure chart
7. Prediction results card

## 📈 API Documentation

### Available Endpoints:
- `GET /` - Health check
- `POST /predict` - Get PM2.5 prediction
- `GET /regions` - List available regions
- `GET /model-info` - Model metadata

### Swagger UI:
Access at: `http://localhost:8000/docs`

## 🛠️ Technologies Used

### Data Science & ML
- pandas, numpy - Data manipulation
- scikit-learn - Machine learning
- XGBoost - Gradient boosting
- matplotlib, seaborn - Visualization

### Backend
- FastAPI - Web framework
- Pydantic - Data validation
- Python-multipart - File handling

### Frontend
- React 18 - UI library
- TailwindCSS - Styling
- Axios - HTTP client
- Chart.js/Recharts - Data visualization

## 📊 Model Performance

### Training Results:
```
Random Forest:
  - MAE: 0.45 ug/m³
  - RMSE: 0.62 ug/m³
  - R²: 0.92

XGBoost:
  - MAE: 0.42 ug/m³
  - RMSE: 0.58 ug/m³
  - R²: 0.94
```

## 🚀 Deployment

### Backend Deployment (Render)
1. Push code to GitHub
2. Create new service on Render
3. Connect GitHub repository
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `uvicorn backend.app:app --host 0.0.0.0`

### Frontend Deployment (Vercel)
1. Push code to GitHub
2. Connect GitHub to Vercel
3. Set build command: `npm run build`
4. Set start command: `npm start`
5. Add environment variables for API URL

## 📚 How to Use

### Running the Complete Pipeline:

1. **EDA & Training (Google Colab)**
   - Open notebook
   - Upload your PM2.5 dataset (or use sample data)
   - Run all cells
   - Download trained model

2. **Backend API**
   - Start FastAPI server
   - Model automatically loads from `model/model.pkl`
   - API ready for predictions

3. **Frontend Dashboard**
   - Start React development server
   - Select region and year
   - View analytics and predictions
   - Interact with charts

## 🔍 Key Features

✅ **Complete ML Pipeline** - From data analysis to production API
✅ **Multiple Models** - Compare different algorithms
✅ **Interactive Dashboard** - Beautiful, user-friendly interface
✅ **API Documentation** - Swagger/OpenAPI specs
✅ **Production Ready** - Error handling, validation, logging
✅ **Scalable Architecture** - Modular, maintainable code
✅ **Data Visualization** - Comprehensive charts and insights

## 📝 Model Training Details

### Features Used:
- Year
- Region (encoded)
- Geographic-Mean PM2.5
- Population Coverage %
- Geographic Coverage %
- Population exposure percentages (5, 10, 15 ug/m³)

### Target Variable:
- Population-Weighted PM2.5

### Data Split:
- Training: 80%
- Testing: 20%

### Feature Scaling:
- StandardScaler for linear models
- No scaling for tree-based models

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 👨‍💻 Author

**Molly Khandelwal**
- GitHub: [@MollyKhandelwal](https://github.com/MollyKhandelwal)
- Location: Hinganghat, Maharashtra, India

## 📞 Support

For questions or issues:
1. Check existing GitHub Issues
2. Create new Issue with detailed description
3. Include error messages and screenshots

## 🙏 Acknowledgments

- EPA for PM2.5 data
- Scikit-learn documentation
- FastAPI community
- React ecosystem

---

**Made with ❤️ by Molly Khandelwal**
