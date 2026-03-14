#!/usr/bin/env python3
"""
PM2.5 ML Model Training Script
Complete pipeline: EDA -> Train -> Evaluate -> Save
With feature importance analysis and visualization
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import pickle
import json
import warnings
import os

warnings.filterwarnings('ignore')

# Create directories
os.makedirs('models', exist_ok=True)
os.makedirs('reports', exist_ok=True)
os.makedirs('data', exist_ok=True)

print("="*80)
print("PM2.5 ML TRAINING PIPELINE - HACKATHON READY")
print("="*80)

# STEP 1: Create Realistic Dataset
print("\n[1/6] Generating PM2.5 dataset...")
np.random.seed(42)

regions = ['Northeast', 'Midwest', 'South', 'West', 'Pacific', 'Mountain']
data = []

for region in regions:
    for year in range(1998, 2024):
        # Realistic trend: PM2.5 decreases over time
        base_pm25 = 14.5 - (2024 - year) * 0.08
        
        data.append({
            'Region': region,
            'Year': year,
            'Population-Weighted PM2.5': max(base_pm25 + np.random.normal(0, 0.7), 5),
            'Geographic-Mean PM2.5': base_pm25 + np.random.uniform(0.3, 1.2),
            'Population Coverage %': np.random.uniform(92, 100),
            'Geographic Coverage %': np.random.uniform(88, 100),
            'Pop % >= 5 ug/m3': np.random.uniform(75, 95),
            'Pop % >= 10 ug/m3': np.random.uniform(45, 75),
            'Pop % >= 15 ug/m3': np.random.uniform(15, 50),
        })

df = pd.DataFrame(data)
print(f"  ✓ Created {df.shape[0]} samples with {df.shape[1]} features")
print(f"  Dataset shape: {df.shape}")

# Save raw dataset
df.to_csv('data/pm25_raw.csv', index=False)

# STEP 2: Data Preprocessing
print("\n[2/6] Preprocessing data...")

# Encode categorical variable
le_region = LabelEncoder()
df['Region_encoded'] = le_region.fit_transform(df['Region'])

# Define target and features
target = 'Population-Weighted PM2.5'
feature_cols = [
    'Year', 'Region_encoded', 'Geographic-Mean PM2.5',
    'Population Coverage %', 'Geographic Coverage %',
    'Pop % >= 5 ug/m3', 'Pop % >= 10 ug/m3', 'Pop % >= 15 ug/m3'
]

X = df[feature_cols]
y = df[target]

print(f"  ✓ Features: {len(feature_cols)}")
print(f"  ✓ Target: {target}")
print(f"  ✓ Feature names: {feature_cols}")

# STEP 3: Train-Test Split
print("\n[3/6] Splitting data...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print(f"  ✓ Train samples: {X_train.shape[0]}")
print(f"  ✓ Test samples: {X_test.shape[0]}")
print(f"  ✓ Train-Test ratio: 80-20")

# STEP 4: Train Multiple Models
print("\n[4/6] Training regression models...")

models = {
    'Linear Regression': LinearRegression(),
    'Random Forest': RandomForestRegressor(
        n_estimators=100, max_depth=12, random_state=42, n_jobs=-1
    ),
    'XGBoost': XGBRegressor(
        n_estimators=100, max_depth=7, learning_rate=0.1, 
        random_state=42, verbosity=0, n_jobs=-1
    )
}

results = {}
best_model = None
best_name = None
best_r2 = -1
best_predictions = None

for name, model in models.items():
    print(f"\n  Training {name}...")
    
    if name == 'Linear Regression':
        model.fit(X_train_scaled, y_train)
        y_pred = model.predict(X_test_scaled)
    else:
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
    
    # Calculate metrics
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    
    results[name] = {'mae': float(mae), 'rmse': float(rmse), 'r2': float(r2)}
    
    print(f"    MAE:  {mae:.4f} µg/m³")
    print(f"    RMSE: {rmse:.4f} µg/m³")
    print(f"    R²:   {r2:.4f}")
    
    if r2 > best_r2:
        best_r2 = r2
        best_model = model
        best_name = name
        best_predictions = y_pred

print(f"\n{'='*80}")
print(f"🏆 BEST MODEL: {best_name} (R² = {best_r2:.4f})")
print(f"{'='*80}")

# STEP 5: Feature Importance Analysis
print("\n[5/6] Analyzing feature importance...")

if best_name == 'Random Forest':
    importances = best_model.feature_importances_
elif best_name == 'XGBoost':
    importances = best_model.feature_importances_
else:
    importances = np.abs(best_model.coef_)

feature_importance_df = pd.DataFrame({
    'Feature': feature_cols,
    'Importance': importances
}).sort_values('Importance', ascending=False)

print("\n  Top 5 Important Features:")
for idx, row in feature_importance_df.head().iterrows():
    print(f"    {row['Feature']}: {row['Importance']:.4f}")

# Save feature importance
feature_importance_df.to_csv('reports/feature_importance.csv', index=False)

# STEP 6: Save Model and Metadata
print("\n[6/6] Saving model artifacts...")

model_package = {
    'model': best_model,
    'scaler': scaler if best_name == 'Linear Regression' else None,
    'encoder': le_region,
    'features': feature_cols,
    'model_name': best_name,
    'feature_importance': feature_importance_df.to_dict()
}

with open('models/pm25_model.pkl', 'wb') as f:
    pickle.dump(model_package, f)

metadata = {
    'model': best_name,
    'r2_score': best_r2,
    'mae': float(results[best_name]['mae']),
    'rmse': float(results[best_name]['rmse']),
    'features': feature_cols,
    'regions': list(le_region.classes_),
    'all_results': results
}

with open('models/model_metadata.json', 'w') as f:
    json.dump(metadata, f, indent=2)

print(f"  ✓ Model saved: models/pm25_model.pkl")
print(f"  ✓ Metadata saved: models/model_metadata.json")
print(f"  ✓ Feature importance saved: reports/feature_importance.csv")

# Create visualizations
print("\n  Creating visualizations...")

# 1. Feature Importance Plot
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(
    data=feature_importance_df.head(8),
    x='Importance',
    y='Feature',
    palette='viridis',
    ax=ax
)
ax.set_title('Top 8 Feature Importance', fontsize=14, fontweight='bold')
ax.set_xlabel('Importance Score', fontsize=12)
plt.tight_layout()
plt.savefig('reports/feature_importance.png', dpi=300, bbox_inches='tight')
plt.close()

# 2. Actual vs Predicted
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(y_test, best_predictions, alpha=0.6, s=50, edgecolors='k')
ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
ax.set_xlabel('Actual PM2.5 (µg/m³)', fontsize=12)
ax.set_ylabel('Predicted PM2.5 (µg/m³)', fontsize=12)
ax.set_title('Actual vs Predicted PM2.5 Values', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('reports/actual_vs_predicted.png', dpi=300, bbox_inches='tight')
plt.close()

# 3. PM2.5 Trend by Year
trend_df = df.groupby('Year')['Population-Weighted PM2.5'].mean()
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(trend_df.index, trend_df.values, marker='o', linewidth=2, markersize=6, color='#2E86AB')
ax.fill_between(trend_df.index, trend_df.values, alpha=0.3, color='#2E86AB')
ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Average PM2.5 (µg/m³)', fontsize=12)
ax.set_title('PM2.5 Trend Over Years (1998-2023)', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('reports/pm25_trend.png', dpi=300, bbox_inches='tight')
plt.close()

# 4. PM2.5 by Region
region_df = df.groupby('Region')['Population-Weighted PM2.5'].mean().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=region_df.values, y=region_df.index, palette='coolwarm', ax=ax)
ax.set_xlabel('Average PM2.5 (µg/m³)', fontsize=12)
ax.set_title('PM2.5 Levels by Region', fontsize=14, fontweight='bold')
for i, v in enumerate(region_df.values):
    ax.text(v + 0.1, i, f'{v:.2f}', va='center')
plt.tight_layout()
plt.savefig('reports/pm25_by_region.png', dpi=300, bbox_inches='tight')
plt.close()

print(f"  ✓ Feature importance plot saved")
print(f"  ✓ Actual vs predicted plot saved")
print(f"  ✓ PM2.5 trend plot saved")
print(f"  ✓ PM2.5 by region plot saved")

print(f"\n{'='*80}")
print(f"✅ ML TRAINING PIPELINE COMPLETED SUCCESSFULLY!")
print(f"\nModel: {best_name}")
print(f"Test R² Score: {best_r2:.4f}")
print(f"Test RMSE: {results[best_name]['rmse']:.4f} µg/m³")
print(f"Test MAE: {results[best_name]['mae']:.4f} µg/m³")
print(f"\nAll artifacts saved to:")
print(f"  - models/pm25_model.pkl")
print(f"  - models/model_metadata.json")
print(f"  - reports/feature_importance.csv")
print(f"  - reports/*.png (visualization charts)")
print(f"  - data/pm25_raw.csv")
print(f"{'='*80}")
