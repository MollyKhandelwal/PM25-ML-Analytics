#!/usr/bin/env python3
# PM2.5 ML Model Training Script
# Complete pipeline: EDA -> Train -> Evaluate -> Save

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import pickle, json, warnings
warnings.filterwarnings('ignore')

print("="*70)
print("PM2.5 ML TRAINING PIPELINE")
print("="*70)

# STEP 1: Create Dataset
print("\nStep 1: Generating dataset...")
np.random.seed(42)
regions = ['Northeast', 'Midwest', 'South', 'West', 'Pacific', 'Mountain']
data = []
for region in regions:
    for year in range(1998, 2024):
        base_pm25 = 12.5 - (2024 - year) * 0.05
        data.append({
            'Region': region,
            'Year': year,
            'Population-Weighted PM2.5': max(base_pm25 + np.random.normal(0, 0.8), 5),
            'Geographic-Mean PM2.5': base_pm25 + np.random.uniform(0.5, 1.5),
            'Population Coverage %': np.random.uniform(90, 100),
            'Geographic Coverage %': np.random.uniform(85, 100),
            'Pop % >= 5 ug/m3': np.random.uniform(70, 95),
            'Pop % >= 10 ug/m3': np.random.uniform(40, 75),
            'Pop % >= 15 ug/m3': np.random.uniform(10, 45),
        })
df = pd.DataFrame(data)
print(f"✓ Dataset: {df.shape[0]} samples, {df.shape[1]} columns")

# STEP 2: Data Preprocessing
print("\nStep 2: Preprocessing data...")
le_region = LabelEncoder()
df['Region_encoded'] = le_region.fit_transform(df['Region'])
target = 'Population-Weighted PM2.5'
feature_cols = ['Year', 'Region_encoded', 'Geographic-Mean PM2.5',
                'Population Coverage %', 'Geographic Coverage %',
                'Pop % >= 5 ug/m3', 'Pop % >= 10 ug/m3', 'Pop % >= 15 ug/m3']
X, y = df[feature_cols], df[target]
print(f"✓ Features: {len(feature_cols)}, Target: {target}")

# STEP 3: Train-Test Split
print("\nStep 3: Splitting data...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
print(f"✓ Train: {X_train.shape[0]}, Test: {X_test.shape[0]}")

# STEP 4: Train Models
print("\nStep 4: Training models...")
models = {
    'Linear Regression': LinearRegression(),
    'Random Forest': RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42),
    'XGBoost': XGBRegressor(n_estimators=100, max_depth=6, learning_rate=0.1, random_state=42, verbosity=0)
}

results, best_model, best_name, best_r2 = {}, None, None, -1

for name, model in models.items():
    if name == 'Linear Regression':
        model.fit(X_train_scaled, y_train)
        y_pred = model.predict(X_test_scaled)
    else:
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
    
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    
    results[name] = {'mae': mae, 'rmse': rmse, 'r2': r2}
    print(f"\n{name}:")
    print(f"  MAE: {mae:.4f}, RMSE: {rmse:.4f}, R²: {r2:.4f}")
    
    if r2 > best_r2:
        best_r2, best_model, best_name = r2, model, name

print(f"\n{'='*70}")
print(f"🏆 BEST MODEL: {best_name} (R² = {best_r2:.4f})")
print(f"{'='*70}")

# STEP 5: Save Model
print("\nStep 5: Saving model...")
model_package = {
    'model': best_model,
    'scaler': scaler if best_name == 'Linear Regression' else None,
    'encoder': le_region,
    'features': feature_cols,
    'model_name': best_name
}

with open('model.pkl', 'wb') as f:
    pickle.dump(model_package, f)

with open('model_metadata.json', 'w') as f:
    json.dump({'model': best_name, 'r2': float(best_r2), 'mae': float(results[best_name]['mae'])}, f)

print(f"✓ Model saved: model.pkl")
print(f"✓ Metadata saved: model_metadata.json")

print(f"\n{'='*70}")
print(f"✅ ML TRAINING COMPLETE!")
print(f"Best Model: {best_name}")
print(f"Test R² Score: {best_r2:.4f}")
print(f"{'='*70}")
