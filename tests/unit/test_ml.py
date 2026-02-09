from unittest.mock import MagicMock
from app.services.ml_service import MLService
import pytest

def test_ml_service_mock_mode():
    service = MLService()
    # Ensure it falls back to mock if no model exists
    prediction = service.predict_stockout(100, 10, 5)
    assert prediction == 10.0 # 100 / 10

def test_ml_service_with_mock_model():
    service = MLService()
    mock_model = MagicMock()
    mock_model.predict.return_value = [5.5]
    service.model = mock_model
    
    prediction = service.predict_stockout(100, 10, 5)
    assert prediction == 5.5
    mock_model.predict.assert_called_once()
