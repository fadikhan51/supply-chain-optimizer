# Predictive Supply Chain Optimizer 🚀

An AI-powered supply chain management system built with Python (FastAPI), PostgreSQL, and Scikit-Learn.

## 🌟 Key Features
- **AI Stockout Prediction**: Uses a Random Forest Regressor to predict days until stockout based on sales velocity and lead times.
- **Inventory Management**: Full CRUD operations for products and inventory levels.
- **Sales Tracking**: Record sales history and automatically update stock levels.
- **JWT Authentication**: Role-based access control (Admin/Manager) with secure password hashing.
- **Dashboard Summary**: Real-time overview of total products and low-stock alerts.
- **Dockerized Infrastructure**: One-click setup for API, DB, and admin tools.

## 🏗️ Tech Stack
-   **Backend**: FastAPI, SQLAlchemy (Async), Pydantic V2
-   **Database**: PostgreSQL 15, asyncpg
-   **ML**: Scikit-Learn, Joblib, Pandas
-   **Security**: Passlib (Bcrypt), JWT (python-jose)
-   **Infrastructure**: Docker, Docker Compose
-   **Testing**: Pytest, Httpx

## ⚙️ Project Structure
```text
/app
  /api             # Controllers (Routers)
  /core            # Configuration & Security
  /db              # Database sessions & Base classes
  /helpers         # Utility functions & response formatting
  /models          # SQLAlchemy Database Models
  /repositories    # Database Logic (Repository Pattern)
  /schemas         # Pydantic validation & Serialization
  /services        # Business Logic & ML Inference (Service Pattern)
/ml_models         # ML training scripts & serialized models
/tests             # Unit & Integration tests
/deploy            # Docker & deployment configs
```

## 🚀 Getting Started

### 1. Prerequisites
- Docker & Docker Compose
- Python 3.11+ (for local development)

### 2. Setup
1.  **Clone the repository**:
    ```bash
    git clone <your-repo-url>
    cd supply-chain-optimizer
    ```
2.  **Environment Variables**:
    ```bash
    cp .env.example .env
    ```
3.  **Run with Docker**:
    ```bash
    docker-compose up --build
    ```

### 3. API Documentation
Once running, visit:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Redoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **Adminer (DB Management)**: [http://localhost:8000:8080](http://localhost:8000:8080)

### 4. Machine Learning
To train the model with synthetic data locally:
```bash
export PYTHONPATH=$PYTHONPATH:.
python3 ml_models/train_model.py
```

### 5. Running Tests
```bash
export PYTHONPATH=$PYTHONPATH:.
python3 -m pytest tests/
```

## 🤝 Contributing
1. Fork the project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License
Distributed under the MIT License.
