import joblib
import os
import numpy as np
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)

class MLService:
    def __init__(self):
        self.model_path = settings.MODEL_PATH
        self.model = None
        self.load_model()

    def load_model(self):
        if os.path.exists(self.model_path):
            try:
                self.model = joblib.load(self.model_path)
                logger.info("Model loaded successfully.")
            except Exception as e:
                logger.error(f"Error loading model: {e}")
                self.model = None
        else:
            logger.warning(f"Model file not found at {self.model_path}. Running in mock mode.")

    def predict_stockout(self, current_stock: int, avg_daily_sales: float, lead_time: int) -> float:
        if self.model:
            try:
                X = np.array([[current_stock, avg_daily_sales, lead_time]])
                prediction = self.model.predict(X)
                return float(prediction[0])
            except Exception as e:
                logger.error(f"Prediction error: {e}")
                return self.mock_predict(current_stock, avg_daily_sales)
        else:
            return self.mock_predict(current_stock, avg_daily_sales)

    def mock_predict(self, current_stock: int, avg_daily_sales: float) -> float:
        # Basic logical prediction: stock / sales
        if avg_daily_sales <= 0:
            return 999.0
        return float(current_stock / avg_daily_sales)

ml_service = MLService()
