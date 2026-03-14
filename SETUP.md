# PM2.5 Analytics - Complete Setup Guide

## 🚀 Quick Start (5 Minutes)

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn
- Git

## Step 1: Clone Repository
```bash
git clone https://github.com/MollyKhandelwal/PM25-ML-Analytics.git
cd PM25-ML-Analytics
```

## Step 2: Backend Setup

### Install Backend Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Run Backend API
```bash
python -m uvicorn app:app --reload
```

✅ Backend will run at: **http://localhost:8000**

### Test API (In another terminal)
```bash
curl -X GET "http://localhost:8000/"
```

## Step 3: Frontend Setup

### Install Frontend Dependencies
```bash
cd frontend
npm install
```

### Add Tailwind CSS (if not installed)
```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

### Run Frontend
```bash
npm start
```

✅ Frontend will run at: **http://localhost:3000**

## Step 4: ML Model Training (Google Colab)

1. Open `notebooks/01_EDA_and_ML_Training.ipynb` in [Google Colab](https://colab.research.google.com)
2. Run all cells
3. Download `model.pkl` from Colab
4. Place it in `backend/` folder

## API Endpoints

### Health Check
```bash
GET /
```

### Get Prediction
```bash
POST /predict
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

### Swagger Documentation
Access: **http://localhost:8000/docs**

## Project Structure
```
pm25-ml-analytics/
├── backend/
│   ├── app.py
│   ├── schemas.py (optional)
│   └── requirements.txt
├── frontend/
│   ├── package.json
│   ├── src/
│   │   ├── App.jsx
│   │   └── index.css
│   └── public/
├── notebooks/
│   └── 01_EDA_and_ML_Training.ipynb
├── README.md
├── SETUP.md (this file)
└── requirements.txt
```

## Troubleshooting

### Port Already in Use
```bash
# For backend (change 8001 to any free port)
python -m uvicorn app:app --reload --port 8001

# For frontend (change 3001 to any free port)
PORT=3001 npm start
```

### Module Not Found Errors
```bash
# Reinstall dependencies
rm -rf node_modules
npm install

# Or for backend
pip install --upgrade -r requirements.txt
```

### CORS Errors
Backend already has CORS enabled. If you still get errors:
- Ensure backend is running
- Check that frontend is making requests to `http://localhost:8000`

## Deployment

### Deploy Backend (Render)
1. Push to GitHub
2. Create Render service
3. Set build: `pip install -r backend/requirements.txt`
4. Set start: `uvicorn backend.app:app --host 0.0.0.0`

### Deploy Frontend (Vercel)
1. Push to GitHub
2. Import in Vercel
3. Set build: `npm run build`
4. Add env: `REACT_APP_API_URL=<backend-url>`

## Next Steps

✅ Explore the dashboard at http://localhost:3000
✅ Try different regions and years
✅ Check API docs at http://localhost:8000/docs
✅ Customize models and add features

## Support

For issues:
1. Check GitHub Issues
2. Review API documentation
3. Check console logs in browser and terminal
