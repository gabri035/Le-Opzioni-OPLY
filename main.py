from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller
from scipy.stats import gaussian_kde
import matplotlib.gridspec as gridspec
import base64
import io
from Colab.funzioni import analisi_comparata_completa_con_asimmetria_graduale, analisi_statistiche, analisi_statistiche_TAB

app = FastAPI(title="Stock Analysis API", description="API for stock analysis and cointegration", version="1.0.0")

class StockAnalysisRequest(BaseModel):
    stocks1: List[str]
    stocks2: List[str]
    start_date: str  # Format: "YYYY-MM-DD"
    end_date: str    # Format: "YYYY-MM-DD"
    period: Optional[str] = "1d"

class CointegrationRequest(BaseModel):
    stocks1: List[str]
    stocks2: List[str]
    start_date: str
    end_date: str
    period: Optional[str] = "1d"

def download_stock_data(stocks, start_date, end_date, period="1d"):
    """Download stock data with error handling"""
    data = yf.download(stocks, start=start_date, end=end_date, period=period)
    if data is None or data.empty:
        raise HTTPException(status_code=400, detail=f"Failed to download data for {stocks}")
    return data

def plot_to_base64(fig):
    """Convert matplotlib figure to base64 string"""
    buffer = io.BytesIO()
    fig.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close(fig)
    return image_base64

@app.get("/")
async def root():
    return {"message": "Stock Analysis API", "version": "1.0.0"}

@app.post("/analysis/comparative")
async def comparative_analysis(request: StockAnalysisRequest):
    """Perform comparative analysis between two stocks"""
    try:
        start_date = datetime.strptime(request.start_date, "%Y-%m-%d")
        end_date = datetime.strptime(request.end_date, "%Y-%m-%d")
        
        # Download data
        period = request.period or "1d"
        data1 = download_stock_data(request.stocks1, start_date, end_date, period)
        data2 = download_stock_data(request.stocks2, start_date, end_date, period)
        
        # Extract closing prices
        close1 = data1["Close"].squeeze()
        close2 = data2["Close"].squeeze()
        
        # Calculate log returns
        log_returns1 = np.log(close1 / close1.shift(1)).dropna()
        log_returns2 = np.log(close2 / close2.shift(1)).dropna()
        
        # Calculate statistics
        stat1 = analisi_statistiche(request.stocks1[0], log_returns1)
        stat2 = analisi_statistiche(request.stocks2[0], log_returns2)
        
        # Add autocorrelation
        stat1['acf'] = log_returns1.autocorr(lag=1)
        stat2['acf'] = log_returns2.autocorr(lag=1)
        
        # Generate comparative analysis
        comparative_output = analisi_comparata_completa_con_asimmetria_graduale(
            request.stocks1[0], stat1,
            request.stocks2[0], stat2,
        )
        
        return {
            "stocks": {
                "stock1": request.stocks1[0],
                "stock2": request.stocks2[0]
            },
            "statistics": {
                "stock1": stat1,
                "stock2": stat2
            },
            "comparative_analysis": comparative_output,
            "data_points": {
                "stock1_count": len(log_returns1),
                "stock2_count": len(log_returns2)
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analysis/visualizations")
async def generate_visualizations(request: StockAnalysisRequest):
    """Generate comprehensive visualizations for stock analysis"""
    try:
        start_date = datetime.strptime(request.start_date, "%Y-%m-%d")
        end_date = datetime.strptime(request.end_date, "%Y-%m-%d")
        
        # Download data
        period = request.period or "1d"
        data1 = download_stock_data(request.stocks1, start_date, end_date, period)
        data2 = download_stock_data(request.stocks2, start_date, end_date, period)
        
        close1 = data1["Close"].squeeze()
        close2 = data2["Close"].squeeze()
        log_returns1 = np.log(close1 / close1.shift(1)).dropna()
        log_returns2 = np.log(close2 / close2.shift(1)).dropna()
        
        # Calculate correlations
        corr_60 = close1.rolling(60).corr(close2)
        corr_120 = close1.rolling(120).corr(close2)
        corr_240 = close1.rolling(240).corr(close2)
        smooth_corr_60 = corr_60.rolling(10).mean()
        smooth_corr_120 = corr_120.rolling(10).mean()
        smooth_corr_240 = corr_240.rolling(10).mean()
        
        # Statistics for plotting
        x_min = min(log_returns1.min(), log_returns2.min())
        x_max = max(log_returns1.max(), log_returns2.max())
        density1 = gaussian_kde(log_returns1)
        density2 = gaussian_kde(log_returns2)
        density_max = max(density1(density1.dataset).max(), density2(density2.dataset).max())
        
        y_ret_min = min(log_returns1.min(), log_returns2.min())
        y_ret_max = max(log_returns1.max(), log_returns2.max())
        ret_margin = 0.05 * (y_ret_max - y_ret_min)
        
        # Create comprehensive plot
        fig = plt.figure(figsize=(18, 16))
        gs = gridspec.GridSpec(4, 2, height_ratios=[1, 1, 1, 1])
        
        # Row 1: Prices with dual axis
        ax0 = plt.subplot(gs[0, :])
        ax0b = ax0.twinx()
        l1, = ax0.plot(close1, color='blue', label=request.stocks1[0])
        l2, = ax0b.plot(close2, color='red', label=request.stocks2[0])
        ax0.set_ylabel(request.stocks1[0], color='blue')
        ax0.tick_params(axis='y', labelcolor='blue')
        ax0b.set_ylabel(request.stocks2[0], color='red')
        ax0b.tick_params(axis='y', labelcolor='red')
        ax0.set_title(f'Prices {request.stocks1[0]} (left) & {request.stocks2[0]} (right)')
        ax0.set_xlabel('Date')
        ax0.legend([l1, l2], [request.stocks1[0], request.stocks2[0]], loc='upper left')
        
        # Row 2: Moving correlations
        ax1 = plt.subplot(gs[1, :])
        ax1.plot(smooth_corr_60, label='60d', color='red')
        ax1.plot(smooth_corr_120, label='120d', color='green')
        ax1.plot(smooth_corr_240, label='240d', color='blue')
        ax1.axhline(0, color='gray', linestyle='--', linewidth=0.8)
        ax1.set_title(f'Moving Correlations between {request.stocks1[0]} and {request.stocks2[0]}')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Correlation')
        ax1.legend()
        ax1.grid(True)
        
        # Row 3: Log returns
        ax2 = plt.subplot(gs[2, 0])
        ax2.plot(log_returns1.index, log_returns1, color='blue')
        ax2.set_title(f'Log Returns {request.stocks1[0]}')
        ax2.set_xlabel('Date')
        ax2.set_ylabel('Log Return')
        ax2.set_ylim(y_ret_min - ret_margin, y_ret_max + ret_margin)
        ax2.grid(True)
        
        ax3 = plt.subplot(gs[2, 1])
        ax3.plot(log_returns2.index, log_returns2, color='red')
        ax3.set_title(f'Log Returns {request.stocks2[0]}')
        ax3.set_xlabel('Date')
        ax3.set_ylabel('Log Return')
        ax3.set_ylim(y_ret_min - ret_margin, y_ret_max + ret_margin)
        ax3.grid(True)
        
        # Row 4: Distributions
        ax4 = plt.subplot(gs[3, 0])
        sns.histplot(log_returns1, bins=30, kde=True, color='blue', stat='density', ax=ax4)
        ax4.set_title(f'Distribution Log Returns {request.stocks1[0]}')
        ax4.set_ylim(0, density_max * 1.1)
        ax4.set_xlim(x_min, x_max)
        
        ax5 = plt.subplot(gs[3, 1])
        sns.histplot(log_returns2, bins=30, kde=True, color='red', stat='density', ax=ax5)
        ax5.set_title(f'Distribution Log Returns {request.stocks2[0]}')
        ax5.set_ylim(0, density_max * 1.1)
        ax5.set_xlim(x_min, x_max)
        
        plt.tight_layout()
        
        # Convert to base64
        visualization_base64 = plot_to_base64(fig)
        
        return {
            "visualization": visualization_base64,
            "format": "png",
            "description": "Comprehensive stock analysis visualization including prices, correlations, returns, and distributions"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analysis/cointegration")
async def cointegration_analysis(request: CointegrationRequest):
    """Perform cointegration analysis between two stocks"""
    try:
        start_date = datetime.strptime(request.start_date, "%Y-%m-%d")
        end_date = datetime.strptime(request.end_date, "%Y-%m-%d")
        
        # Download data
        period = request.period or "1d"
        data1 = download_stock_data(request.stocks1, start_date, end_date, period)
        data2 = download_stock_data(request.stocks2, start_date, end_date, period)
        
        close1 = data1["Close"].squeeze()
        close2 = data2["Close"].squeeze()
        
        # Regression 1: stock2 ~ stock1
        X1 = close1.values.reshape(-1, 1)
        y1 = close2.values
        X1_ols = sm.add_constant(X1)
        model1 = sm.OLS(y1, X1_ols).fit()
        y1_pred = model1.predict(X1_ols)
        residuals1 = y1 - y1_pred
        r2_1 = model1.rsquared
        adf_result1 = adfuller(residuals1)
        
        # Regression 2: stock1 ~ stock2
        X2 = close2.values.reshape(-1, 1)
        y2 = close1.values
        X2_ols = sm.add_constant(X2)
        model2 = sm.OLS(y2, X2_ols).fit()
        y2_pred = model2.predict(X2_ols)
        residuals2 = y2 - y2_pred
        r2_2 = model2.rsquared
        adf_result2 = adfuller(residuals2)
        
        # Determine cointegration
        cointegrated = False
        best_model = None
        interpretation = ""
        
        if adf_result1[1] < 0.05 or adf_result2[1] < 0.05:
            cointegrated = True
            if adf_result1[1] < adf_result2[1]:
                best_model = 1
                interpretation = f"{request.stocks2[0]} and {request.stocks1[0]} are cointegrated according to regression 1 where {request.stocks2[0]} is Y and {request.stocks1[0]} is X"
            else:
                best_model = 2
                interpretation = f"{request.stocks1[0]} and {request.stocks2[0]} are cointegrated according to regression 2 where {request.stocks1[0]} is Y and {request.stocks2[0]} is X"
        else:
            interpretation = f"{request.stocks1[0]} and {request.stocks2[0]} are not cointegrated"
        
        return {
            "stocks": {
                "stock1": request.stocks1[0],
                "stock2": request.stocks2[0]
            },
            "cointegration_results": {
                "cointegrated": cointegrated,
                "best_model": best_model,
                "interpretation": interpretation
            },
            "regression_1": {
                "dependent": request.stocks2[0],
                "independent": request.stocks1[0],
                "r_squared": r2_1,
                "adf_statistic": adf_result1[0],
                "adf_p_value": adf_result1[1],
                "adf_critical_values": {
                    "1%": adf_result1[4]["1%"],
                    "5%": adf_result1[4]["5%"],
                    "10%": adf_result1[4]["10%"]
                }
            },
            "regression_2": {
                "dependent": request.stocks1[0],
                "independent": request.stocks2[0],
                "r_squared": r2_2,
                "adf_statistic": adf_result2[0],
                "adf_p_value": adf_result2[1],
                "adf_critical_values": {
                    "1%": adf_result2[4]["1%"],
                    "5%": adf_result2[4]["5%"],
                    "10%": adf_result2[4]["10%"]
                }
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analysis/cointegration/plots")
async def cointegration_plots(request: CointegrationRequest):
    """Generate cointegration analysis plots"""
    try:
        start_date = datetime.strptime(request.start_date, "%Y-%m-%d")
        end_date = datetime.strptime(request.end_date, "%Y-%m-%d")
        
        # Download data and perform calculations (same as above)
        period = request.period or "1d"
        data1 = download_stock_data(request.stocks1, start_date, end_date, period)
        data2 = download_stock_data(request.stocks2, start_date, end_date, period)
        
        close1 = data1["Close"].squeeze()
        close2 = data2["Close"].squeeze()
        
        # Regression analysis
        X1 = close1.values.reshape(-1, 1)
        y1 = close2.values
        X1_ols = sm.add_constant(X1)
        model1 = sm.OLS(y1, X1_ols).fit()
        y1_pred = model1.predict(X1_ols)
        residuals1 = y1 - y1_pred
        r2_1 = model1.rsquared
        
        X2 = close2.values.reshape(-1, 1)
        y2 = close1.values
        X2_ols = sm.add_constant(X2)
        model2 = sm.OLS(y2, X2_ols).fit()
        y2_pred = model2.predict(X2_ols)
        residuals2 = y2 - y2_pred
        r2_2 = model2.rsquared
        
        # Plot 1: Regression 1
        fig1, axs1 = plt.subplots(3, 1, figsize=(10, 12))
        
        axs1[0].scatter(close1, close2, alpha=0.5, label='Data')
        axs1[0].plot(close1, y1_pred, color='red', label='Regression')
        axs1[0].set_title(f'{request.stocks2[0]} ~ {request.stocks1[0]} - Regression')
        axs1[0].set_xlabel(f'Price {request.stocks1[0]}')
        axs1[0].set_ylabel(f'Price {request.stocks2[0]}')
        axs1[0].legend()
        axs1[0].grid(True)
        axs1[0].text(0.95, 0.05, f'R² = {r2_1:.2f}', transform=axs1[0].transAxes,
                     fontsize=12, verticalalignment='bottom', horizontalalignment='right',
                     bbox=dict(boxstyle='round', facecolor='white', edgecolor='gray'))
        
        axs1[1].scatter(close1, residuals1, alpha=0.5, label='Residuals')
        axs1[1].axhline(0, color='red', linestyle='--')
        axs1[1].set_title(f'Residuals - {request.stocks2[0]} ~ {request.stocks1[0]}')
        axs1[1].set_xlabel(f'Price {request.stocks1[0]}')
        axs1[1].set_ylabel('Residual')
        axs1[1].legend()
        axs1[1].grid(True)
        
        axs1[2].plot(close1.index, residuals1, label='Residuals', color='purple')
        axs1[2].axhline(0, color='red', linestyle='--')
        axs1[2].set_title('Time series of residuals')
        axs1[2].set_xlabel('Date')
        axs1[2].set_ylabel('Residual')
        axs1[2].legend()
        axs1[2].grid(True)
        
        plt.tight_layout()
        plot1_base64 = plot_to_base64(fig1)
        
        # Plot 2: Regression 2
        fig2, axs2 = plt.subplots(3, 1, figsize=(10, 12))
        
        axs2[0].scatter(close2, close1, alpha=0.5, label='Data')
        axs2[0].plot(close2, y2_pred, color='blue', label='Regression')
        axs2[0].set_title(f'{request.stocks1[0]} ~ {request.stocks2[0]} - Regression')
        axs2[0].set_xlabel(f'Price {request.stocks2[0]}')
        axs2[0].set_ylabel(f'Price {request.stocks1[0]}')
        axs2[0].legend()
        axs2[0].grid(True)
        axs2[0].text(0.95, 0.05, f'R² = {r2_2:.2f}', transform=axs2[0].transAxes,
                     fontsize=12, verticalalignment='bottom', horizontalalignment='right',
                     bbox=dict(boxstyle='round', facecolor='white', edgecolor='gray'))
        
        axs2[1].scatter(close2, residuals2, alpha=0.5, label='Residuals')
        axs2[1].axhline(0, color='red', linestyle='--')
        axs2[1].set_title(f'Residuals - {request.stocks1[0]} ~ {request.stocks2[0]}')
        axs2[1].set_xlabel(f'Price {request.stocks2[0]}')
        axs2[1].set_ylabel('Residual')
        axs2[1].legend()
        axs2[1].grid(True)
        
        axs2[2].plot(close2.index, residuals2, label='Residuals', color='green')
        axs2[2].axhline(0, color='red', linestyle='--')
        axs2[2].set_title(f'Time series of residuals - {request.stocks1[0]} ~ {request.stocks2[0]}')
        axs2[2].set_xlabel('Date')
        axs2[2].set_ylabel('Residual')
        axs2[2].legend()
        axs2[2].grid(True)
        
        plt.tight_layout()
        plot2_base64 = plot_to_base64(fig2)
        
        return {
            "regression_plots": {
                "plot1": {
                    "title": f"{request.stocks2[0]} ~ {request.stocks1[0]} Analysis",
                    "image": plot1_base64,
                    "r_squared": r2_1
                },
                "plot2": {
                    "title": f"{request.stocks1[0]} ~ {request.stocks2[0]} Analysis", 
                    "image": plot2_base64,
                    "r_squared": r2_2
                }
            },
            "format": "png"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 