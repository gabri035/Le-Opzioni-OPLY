# Stock Analysis FastAPI Application

This FastAPI application provides REST endpoints for stock analysis, including comparative analysis, visualizations, and cointegration analysis.

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Applications

### FastAPI Server (Stock Analysis + Options APIs)
Start the FastAPI server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

### Flask Web Application (Options Frontend)
To run the Flask application with the web interface:
```bash
cd "2. Analisi delle serie storiche in python/Prog"
python app.py
```

The Flask web app will be available at `http://localhost:5000` with:
- Home page: `http://localhost:5000/`
- Company info: `http://localhost:5000/company-info`
- Option chains: `http://localhost:5000/option-chain`
- Dash options strategy tool: `http://localhost:5000/dash/`

### Running Both Simultaneously
Both applications can run simultaneously on different ports:
- FastAPI (APIs): `http://localhost:8000`
- Flask (Web UI): `http://localhost:5000`

## API Documentation

Once running, you can access:
- Interactive API docs: `http://localhost:8000/docs`
- ReDoc documentation: `http://localhost:8000/redoc`

## Available Endpoints

### 1. Comparative Analysis
**POST** `/analysis/comparative`

Performs statistical comparative analysis between two stocks.

**Request Body:**
```json
{
  "stocks1": ["MSFT"],
  "stocks2": ["TSLA"],
  "start_date": "2022-01-03",
  "end_date": "2024-12-31",
  "period": "1d"
}
```

**Response:** JSON with statistics and comparative analysis text.

### 2. Visualizations
**POST** `/analysis/visualizations`

Generates comprehensive visualizations including prices, correlations, returns, and distributions.

**Request Body:** Same as comparative analysis

**Response:** JSON with base64-encoded PNG image of the comprehensive plot.

### 3. Cointegration Analysis
**POST** `/analysis/cointegration`

Performs cointegration analysis between two stocks using ADF tests on regression residuals.

**Request Body:** Same as comparative analysis

**Response:** JSON with cointegration results, regression statistics, and ADF test results.

### 4. Cointegration Plots
**POST** `/analysis/cointegration/plots`

Generates regression and residual plots for cointegration analysis.

**Request Body:** Same as comparative analysis

**Response:** JSON with base64-encoded PNG images of regression plots.

### 5. Company Information
**POST** `/company/info`

Retrieves comprehensive company information for a given ticker.

**Request Body:**
```json
{
  "ticker": "AAPL"
}
```

**Response:** JSON with company details, financials, and executive information.

### 6. Options Chain
**POST** `/options/chain`

Gets option chain data for a specific ticker and expiry date.

**Request Body:**
```json
{
  "ticker": "AAPL",
  "expiry": "2024-12-20"
}
```

**Response:** JSON with calls and puts data, or available expiry dates if no expiry specified.

### 7. Black-Scholes Calculator
**POST** `/options/blackscholes`

Calculates Black-Scholes option price and Greeks.

**Request Body:**
```json
{
  "S": 100,
  "K": 105,
  "T": 0.25,
  "r": 0.05,
  "sigma": 0.2,
  "option_type": "call"
}
```

**Response:** JSON with option price and Greeks (delta, gamma, vega, theta, rho).

### 8. Options Strategy Simulation
**POST** `/options/strategy`

Simulates complex options strategies with multiple legs.

**Request Body:**
```json
{
  "spot_price": 100,
  "volatility": 20,
  "rate": 5,
  "days_to_expiry": 30,
  "options": [
    {
      "strike": 95,
      "premium": 6,
      "option_type": "call",
      "position": 1
    },
    {
      "strike": 105,
      "premium": 2,
      "option_type": "call",
      "position": -1
    }
  ]
}
```

**Response:** JSON with strategy details, total Greeks, payoff simulation, and P&L analysis.

## Example Usage

### Python Client Example
```python
import requests
import base64
from PIL import Image
import io

# Comparative analysis
response = requests.post(
    "http://localhost:8000/analysis/comparative",
    json={
        "stocks1": ["MSFT"],
        "stocks2": ["TSLA"],
        "start_date": "2022-01-03",
        "end_date": "2024-12-31"
    }
)
result = response.json()
print(result["comparative_analysis"])

# Get visualizations
response = requests.post(
    "http://localhost:8000/analysis/visualizations",
    json={
        "stocks1": ["MSFT"],
        "stocks2": ["TSLA"],
        "start_date": "2022-01-03",
        "end_date": "2024-12-31"
    }
)
result = response.json()

# Save the visualization
image_data = base64.b64decode(result["visualization"])
image = Image.open(io.BytesIO(image_data))
image.save("stock_analysis.png")
```

### cURL Example
```bash
curl -X POST "http://localhost:8000/analysis/comparative" \
     -H "Content-Type: application/json" \
     -d '{
       "stocks1": ["MSFT"],
       "stocks2": ["TSLA"],
       "start_date": "2022-01-03",
       "end_date": "2024-12-31"
     }'
```

## Features Preserved

All original algorithms from the Colab notebooks are preserved:
- Statistical analysis functions from `funzioni.py`
- Comparative analysis with asymmetry detection
- Moving correlations calculation
- Cointegration analysis with ADF tests
- All visualization capabilities

## Data Format

- **Date Format:** YYYY-MM-DD
- **Period Options:** "1d" (daily), "1wk" (weekly), "1mo" (monthly)
- **Images:** Returned as base64-encoded PNG strings
- **Statistics:** Returned as JSON objects with numerical values

## Error Handling

The API includes proper error handling for:
- Invalid stock symbols
- Data download failures
- Invalid date ranges
- Missing or malformed request data

All errors return appropriate HTTP status codes with descriptive messages.

## Quick Deploy to Render

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

1. **One-Click Deploy:** Click the button above or go to [render.com](https://render.com)
2. **Connect Repository:** Link your GitHub account and select this repository
3. **Automatic Setup:** Render will detect the `render.yaml` configuration
4. **Live API:** Your API will be available at `https://your-service-name.onrender.com`

### Manual Render Setup

Alternatively, you can manually configure:
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Python Version:** 3.11
- **Health Check:** `/health`

### After Deployment

- **API Documentation:** `https://your-service-name.onrender.com/docs`
- **Health Check:** `https://your-service-name.onrender.com/health`
- **API Status:** `https://your-service-name.onrender.com/`

For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md). 