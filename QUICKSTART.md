# PM2.5 Sentinel - Quick Start Guide

## 🚀 Quick Setup (2 minutes)

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/MollyKhandelwal/PM25-ML-Analytics.git
cd PM25-ML-Analytics

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Train the ML model
python train_model.py
```

## 🎯 Run the Dashboard

```bash
# Start Streamlit app
streamlit run app.py
```

The dashboard will open at: `http://localhost:8501`

## 📊 Dashboard Features

### 1. **Dashboard Tab**
- Real-time analytics with key metrics
- Historical PM2.5 trends (1998-2023)
- Regional air quality comparison
- Population exposure data

### 2. **Predictor Tab**
- Interactive PM2.5 forecasting
- Input parameters:
  - Target year (2024-2035)
  - Region selection (6 regions)
  - Geographic mean PM2.5
  - Coverage percentages
- Real-time predictions with health guidance

### 3. **Insights Tab**
- Feature importance analysis
- Model performance metrics (R², MAE, RMSE)
- Comparison of all trained models
- Detailed evaluation results

### 4. **Hackathon Info Tab**
- Problem statement
- Solution overview
- Technology stack
- Impact metrics

## 🔧 Project Structure

```
PM25-ML-Analytics/
├── app.py                 # Streamlit dashboard
├── train_model.py         # ML training pipeline
├── requirements.txt       # Dependencies
├── models/
│   ├── pm25_model.pkl    # Trained model
│   └── model_metadata.json# Model details
├── data/
│   └── pm25_raw.csv      # Dataset
└── reports/
    ├── feature_importance.csv
    ├── feature_importance.png
    ├── actual_vs_predicted.png
    ├── pm25_trend.png
    └── pm25_by_region.png
```

## 📈 Model Performance

- **Best Model**: XGBoost/Random Forest
- **R² Score**: ~0.94 (94% accuracy)
- **MAE**: < 1.0 µg/m³
- **RMSE**: < 1.5 µg/m³
- **Training Data**: 156 samples (6 regions × 26 years)

## 🎓 How It Works

### Data Pipeline
1. **Generation**: Create realistic PM2.5 dataset with historical trends
2. **Preprocessing**: Handle missing values, encode categorical features
3. **Feature Engineering**: Create 8 key features from raw data
4. **Splitting**: 80% train / 20% test
5. **Scaling**: Standardize features for better model performance

### Model Training
- **Random Forest**: Ensemble with 100 trees
- **XGBoost**: Gradient boosting with optimized hyperparameters
- **Linear Regression**: Baseline model
- **Selection**: Best model by R² score automatically selected

### Prediction Pipeline
1. User inputs region, year, and atmospheric parameters
2. Features are encoded and scaled
3. Model predicts Population-Weighted PM2.5
4. Health guidance provided based on WHO standards

## 🌍 Health Guidelines

- **< 10 µg/m³**: Safe ✅ (WHO recommended)
- **10-15 µg/m³**: Moderate ⚠️ (Sensitive groups affected)
- **> 15 µg/m³**: Unhealthy 🔴 (General population affected)

## 🐛 Troubleshooting

**Issue**: "ModuleNotFoundError: No module named 'streamlit'`
- **Solution**: Run `pip install -r requirements.txt` again

**Issue**: "Model file not found"
- **Solution**: Run `python train_model.py` to generate model artifacts

**Issue**: Port 8501 already in use
- **Solution**: `streamlit run app.py --server.port 8502`

## 📱 Browser Compatibility

- ✅ Chrome/Chromium (Recommended)
- ✅ Firefox
- ✅ Safari
- ✅ Edge

## 📧 Support

For issues or questions, create an issue on GitHub:
https://github.com/MollyKhandelwal/PM25-ML-Analytics/issues

## 🎉 You're Ready!

The PM2.5 Sentinel dashboard is now live and ready for hackathon demo! 🎊
