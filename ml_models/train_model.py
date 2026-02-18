import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import joblib
import os

def generate_synthetic_data(n_samples=1000):
    # Features: current_stock, avg_daily_sales, lead_time
    # Target: days_until_stockout = current_stock / avg_daily_sales
    np.random.seed(42)
    current_stock = np.random.randint(10, 500, n_samples)
    avg_daily_sales = np.random.randint(1, 50, n_samples)
    lead_time = np.random.randint(1, 14, n_samples)
    
    # Simple linear relationship for synthetic data
    # days_until_stockout decreases as sales increase and increases as stock increases
    days_until_stockout = current_stock / avg_daily_sales
    
    df = pd.DataFrame({
        'current_stock': current_stock,
        'avg_daily_sales': avg_daily_sales,
        'lead_time': lead_time,
        'days_until_stockout': days_until_stockout
    })
    return df

def train():
    print("Generating synthetic data...")
    df = generate_synthetic_data()
    
    X = df[['current_stock', 'avg_daily_sales', 'lead_time']]
    y = df['days_until_stockout']
    
    print("Training Random Forest model...")
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    # Evaluation
    from sklearn.metrics import mean_absolute_error, r2_score
    y_pred = model.predict(X)
    mae = mean_absolute_error(y, y_pred)
    r2 = r2_score(y, y_pred)
    print(f"Model trained. MAE: {mae:.4f}, R2 Score: {r2:.4f}")
    
    model_path = os.path.join(os.path.dirname(__file__), 'supply_chain_model.joblib')
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    train()
