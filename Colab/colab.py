import pandas as pd
import yfinance as yf 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller

from datetime import datetime
from scipy.stats import gaussian_kde
from scipy.stats import shapiro, jarque_bera, skew, kurtosis, norm
from statsmodels.tsa.seasonal import STL
from sklearn.linear_model import LinearRegression



######## INPUT!##########
# Modifica qui sotto i parametri per il tuo caso d'uso
######################## 
# Ticker e data di inizio E PERIODO (TIMEFRAME)
stocks1 = ['AAPL']
stocks2 = ['TSLA']

start_date = datetime(2022, 1, 3)
end_date = datetime(2025,5,1)

period = "1d" # weekly, orario, giornaliero (default)
########################



# Scarichiamo i dati
data1 = yf.download(stocks1, start=start_date, end=end_date, period=period)
data2 = yf.download(stocks2, start=start_date, end=end_date, period=period)

# Estraiamo le chiusure
close1 = data1["Close"].squeeze()
close2 = data2["Close"].squeeze()

# Calcoliamo log-rendimenti
log_returns1 = np.log(close1 / close1.shift(1)).dropna()
log_returns2 = np.log(close2 / close2.shift(1)).dropna()










##############
#### PREZZI E RENDIMENTI DEI DUE ASSET
###############

# Range comune per assi Y nei rendimenti
y_min = min(log_returns1.min(), log_returns2.min())
y_max = max(log_returns1.max(), log_returns2.max())

# Calcolo range per asse X e max densità
x_min = y_min
x_max = y_max
x_grid = np.linspace(x_min, x_max, 1000)
kde1 = gaussian_kde(log_returns1)
kde2 = gaussian_kde(log_returns2)
density_max = max(kde1(x_grid).max(), kde2(x_grid).max())

# Creazione della figura
fig, axs = plt.subplots(3, 2, figsize=(18, 12))

# --- RIGA 1: Prezzi con doppio asse (AAPL a sinistra, TSLA a destra) ---
ax_price = plt.subplot2grid((3, 2), (0, 0), colspan=2)
ax_tsla = ax_price.twinx()

# Plot delle serie
line1, = ax_price.plot(close1, color='blue', label='AAPL')
line2, = ax_tsla.plot(close2, color='red', label='TSLA')

# Personalizzazione degli assi
ax_price.set_ylabel('AAPL', color='blue')
ax_price.tick_params(axis='y', labelcolor='blue')
ax_price.yaxis.set_ticks_position('left')
ax_price.yaxis.set_label_position('left')

ax_tsla.set_ylabel('TSLA', color='red')
ax_tsla.tick_params(axis='y', labelcolor='red', left=False)
ax_tsla.yaxis.set_ticks_position('right')
ax_tsla.yaxis.set_label_position('right')

ax_price.set_title('Prezzi AAPL (sinistra) & TSLA (destra)')
ax_price.set_xlabel('Data')

# Legenda
lines = [line1, line2]
labels = [line.get_label() for line in lines]
ax_price.legend(lines, labels, loc='upper left')

# --- RIGA 2: Log-Rendimenti (stessa scala Y) ---
axs[1, 0].plot(log_returns1.index, log_returns1, color='blue')
axs[1, 0].set_title('Log-Rendimenti AAPL')
axs[1, 0].set_ylim(y_min, y_max)
axs[1, 0].set_xlabel('Data')
axs[1, 0].set_ylabel('Log-Rendimento')
axs[1, 0].grid(True)

axs[1, 1].plot(log_returns2.index, log_returns2, color='red')
axs[1, 1].set_title('Log-Rendimenti TSLA')
axs[1, 1].set_ylim(y_min, y_max)
axs[1, 1].set_xlabel('Data')
axs[1, 1].set_ylabel('Log-Rendimento')
axs[1, 1].grid(True)

# --- RIGA 3: Distribuzioni (stessa scala X e Y, istogramma + KDE) ---
sns.histplot(log_returns1, ax=axs[2, 0], bins=30, kde=True, color='blue', stat='density')
axs[2, 0].set_title('Distribuzione Log-Rendimenti AAPL')
axs[2, 0].set_ylim(0, density_max * 1.1)
axs[2, 0].set_xlim(x_min, x_max)

sns.histplot(log_returns2, ax=axs[2, 1], bins=30, kde=True, color='red', stat='density')
axs[2, 1].set_title('Distribuzione Log-Rendimenti TSLA')
axs[2, 1].set_ylim(0, density_max * 1.1)
axs[2, 1].set_xlim(x_min, x_max)


##### ANALISI DEGLI ASSET E DEI RENDIMENTI####
######### robetto prob singolo rendimento#####

# Layout finale
plt.tight_layout()
plt.show()



###############
# --- funzione STATISTICHE DESCRITTIVE E TEST DI NORMALITÀ ---
################

def analisi_statistiche(titolo, returns):
    media = returns.mean()
    dev_std = returns.std()
    asimmetria = skew(returns)
    curtosi = kurtosis(returns)  # Curtosi in eccesso

    print(f"\nStatistiche dei log-rendimenti di {titolo}:")
    print("--------------------------------------------")
    print(f"Media: {media:.6f}")
    print(f"Deviazione Standard: {dev_std:.6f}")
    print(f"Asimmetria (Skewness): {asimmetria:.6f}")
    print(f"Curtosi (Excess Kurtosis): {curtosi:.6f}")

    # Test di normalità
    shapiro_stat, shapiro_p = shapiro(returns)
    jb_stat, jb_p = jarque_bera(returns)

    print("\nTest di normalità - Shapiro-Wilk:")
    print(f"  Statistica: {shapiro_stat:.6f}  p-value: {shapiro_p:.6f}")
    print("Test di normalità - Jarque-Bera:")
    print(f"  Statistica: {jb_stat:.6f}  p-value: {jb_p:.6f}")

#########################################
#########################################

















####################
###### ANALISI SUI PREZZI
####################


# Prepara i dati
X1 = close1.values.reshape(-1, 1)  # AAPL
y1 = close2.values                # TSLA

X2 = close2.values.reshape(-1, 1)  # TSLA
y2 = close1.values                # AAPL

# Aggiungi costante per intercetta
X1_ols = sm.add_constant(X1)
X2_ols = sm.add_constant(X2)



###########################DUE FINESTRELLE SEPARATO
# Regressione TSLA ~ AAPL       
model1 = sm.OLS(y1, X1_ols).fit()
y1_pred = model1.predict(X1_ols)
residuals1 = y1 - y1_pred
r2_1 = model1.rsquared



########################## SECONDA FINESTRELLA SEPARATO
# Regressione AAPL ~ TSLA
model2 = sm.OLS(y2, X2_ols).fit()
y2_pred = model2.predict(X2_ols)
residuals2 = y2 - y2_pred
r2_2 = model2.rsquared



######### cooointegrazione, ANALISI DEI RESIDUI 

# Output riepilogativo
print("########### Regressione 1: TSLA ~ AAPL ###########")
print(model1.summary())
analisi_statistiche("tsla-apple resid", model1.resid)

adf_result_resid12 = adfuller(residuals1)
print("\nTest ADF per i residui della regressione 1 ~ 2:")
print("Statistic ADF:", adf_result_resid12[0])
print("p-value:", adf_result_resid12[1])


# 
print("\n########### Regressione 2: AAPL ~ TSLA ###########")
print(model2.summary())
analisi_statistiche("apple-tsla resid", model2.resid)

adf_result_resid21 = adfuller(residuals2)
print("\nTest ADF per i residui della regressione 2 ~ 1:")
print("Statistic ADF:", adf_result_resid21[0])
print("p-value:", adf_result_resid21[1])



#### if adf_result_resid12[1] < adf_result_resid21[1]      MODELLO 12 MIGLIORE, ALTRIMENTI MODELLO 21 MIGLIORE

### se IL PVALUE IN GENERALE DI UNA QUALUNQUE COPPIA è MINORE DI 0.05 ALLORA I DUE ASSET SONO COINTEGRATI. Quindi prima verificare cghe almeno UNO dei due p-value < 0.05, NON COINTEGRATI. 
### SE ENTRAMBI I P-VALUE SONO MINORI DI 0.05, prendi quello con pvalue minore. e di " PINCO E PALLO SONO COINTEGRATI SECONDO LA REGRESSIONE 1 è Y e l'altro è X"


# Crea i subplot
fig, axs = plt.subplots(2, 2, figsize=(14, 10))



# --- Subplot 1: TSLA vs AAPL ---
axs[0, 0].scatter(close1, close2, alpha=0.5, label='Dati')
axs[0, 0].plot(close1, y1_pred, color='red', label='Regressione')
axs[0, 0].set_title('TSLA vs AAPL (Prezzi)')
axs[0, 0].set_xlabel('Prezzo AAPL')
axs[0, 0].set_ylabel('Prezzo TSLA')
axs[0, 0].legend()
axs[0, 0].grid(True)
axs[0, 0].text(0.95, 0.05, f'R² = {r2_1:.2f}', transform=axs[0, 0].transAxes,
               fontsize=12, verticalalignment='bottom', horizontalalignment='right',
               bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='gray'))

# --- Subplot 2: AAPL vs TSLA ---
axs[0, 1].scatter(close2, close1, alpha=0.5, label='Dati')
axs[0, 1].plot(close2, y2_pred, color='blue', label='Regressione')
axs[0, 1].set_title('AAPL vs TSLA (Prezzi)')
axs[0, 1].set_xlabel('Prezzo TSLA')
axs[0, 1].set_ylabel('Prezzo AAPL')
axs[0, 1].legend()
axs[0, 1].grid(True)
axs[0, 1].text(0.95, 0.05, f'R² = {r2_2:.2f}', transform=axs[0, 1].transAxes,
               fontsize=12, verticalalignment='bottom', horizontalalignment='right',
               bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='gray'))

# --- Subplot 3: Residui TSLA vs AAPL ---
axs[1, 0].scatter(close1, residuals1, alpha=0.5, label='Residui')
axs[1, 0].axhline(0, color='red', linestyle='--')
axs[1, 0].set_title('Residui TSLA vs AAPL')
axs[1, 0].set_xlabel('Prezzo AAPL')
axs[1, 0].set_ylabel('Residuo')
axs[1, 0].legend()
axs[1, 0].grid(True)

# --- Subplot 4: Residui AAPL vs TSLA ---
axs[1, 1].scatter(close2, residuals2, alpha=0.5, label='Residui')
axs[1, 1].axhline(0, color='red', linestyle='--')
axs[1, 1].set_title('Residui AAPL vs TSLA')
axs[1, 1].set_xlabel('Prezzo TSLA')
axs[1, 1].set_ylabel('Residuo')
axs[1, 1].legend()
axs[1, 1].grid(True)

# --- Correlazioni mobili lisce sui prezzi ---
corr_60 = close1.rolling(60).corr(close2)
corr_120 = close1.rolling(120).corr(close2)
corr_240 = close1.rolling(240).corr(close2)

smooth_corr_60 = corr_60.rolling(10).mean()
smooth_corr_120 = corr_120.rolling(10).mean()
smooth_corr_240 = corr_240.rolling(10).mean()

# Calcolo range dinamico
y_min = min(smooth_corr_60.min(), smooth_corr_120.min(), smooth_corr_240.min())
y_max = max(smooth_corr_60.max(), smooth_corr_120.max(), smooth_corr_240.max())
margin = 0.05 * (y_max - y_min)

# Plot correlazioni
plt.figure(figsize=(12, 4))
plt.plot(smooth_corr_60, label='60d', color='red')
plt.plot(smooth_corr_120, label='120d', color='green')
plt.plot(smooth_corr_240, label='240d', color='blue')

plt.title('Correlazioni Mobili tra AAPL e TSLA (Prezzi)')
plt.ylim(y_min - margin, y_max + margin)
plt.axhline(0, color='gray', linestyle='--', linewidth=0.8)
plt.legend()


plt.grid(True)
plt.tight_layout()
plt.show()
