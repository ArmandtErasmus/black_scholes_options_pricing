# Import necessary libraries
import streamlit as st 
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import black_scholes_model as bsm
import pandas as pd

# call_price(spot_price, strike_price, rf_rate, maturity_time, volatility): reference
def meshgrid(X_min, Y_min, X_max, Y_max):
    X_range = np.linspace(X_min, X_max, 100)
    Y_range = np.linspace(Y_min, Y_max, 100)
    X, Y = np.meshgrid(X_range, Y_range)
    return X, Y

def heatmap(X, Y, call_Z, put_Z, call_title, put_title, call_label, put_label, x_label, y_label):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Call Plot
    call = ax1.contourf(X, Y, call_Z, cmap="viridis")
    fig.colorbar(call, ax=ax1, label=call_label)
    ax1.set_title(call_title)
    ax1.set_xlabel(x_label)
    ax1.set_ylabel(y_label)

    # Put Plot
    put = ax2.contourf(X, Y, put_Z, cmap="plasma")
    fig.colorbar(put, ax=ax2, label=put_label)
    ax2.set_title(put_title)
    ax2.set_xlabel(x_label)
    ax2.set_ylabel(y_label)

    plt.tight_layout()
    return fig

# Streamlit Dashboard Configuration
st.set_page_config(
    layout='wide',
    page_title='A Visual Framework for Pricing and Sensitivity Analysis of European Options',
    page_icon="📊")

# Custom CSS to inject into Streamlit
st.markdown("""
<style>
.card-left {
    display: flex;
    border: 1px solid #ccc;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 1px 1px 6px rgba(0,0,0,0.05);
    margin-bottom: 10px;
}
.bar-green {
    width: 8px;
    background-color: #28a745;
}
.bar-red {
    width: 8px;
    background-color: #dc3545;
}
.content {
    padding: 15px;
    background-color: #ffffff;
    width: 100%;
}
.label {
    font-size: 16px;
    font-weight: bold;
    margin-bottom: 4px;
}
.label-green {
    color: #28a745;
}
.label-red {
    color: #dc3545;
}
.price {
    font-size: 28px;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

# Streamlit Dashboard Sidebar Parameters
with st.sidebar:
    st.title('Black-Scholes Model Parameters')

    spot_price = st.number_input('Asset Spot Price', value=100.00, help='Current price of the call/put option: e.g. 100')
    strike_price = st.number_input('Asset Strike Price', value=100.00, help='Price at which the call/put option can be exercised: e.g. 100')
    maturity_time = st.number_input('Time to Maturity (years)', value=1, help="Remaining time (in years) until the option's expiration date: e.g. 1")
    volatility = st.slider('Volatility', value=0.2, help='Volatility of the asset: e.g. 0.2')
    rf_rate = st.slider('Risk-Free Interest Rate', min_value=0.01, max_value=1.0, value=0.1, help='Risk-free interest rate: e.g. 0.01')

    # Add Small Break Between Upper and Lower Parts
    st.markdown("---")

    st.write("Heatmap Parameters")
    spot_price_min, spot_price_max = st.slider("Spot Price Range", 0.01, 1000.0, (0.01, 1000.0))
    volatility_min, volatility_max = st.slider("Volatility Range", 0.01, 1.0, (0.01, 1.0))
    maturity_time_min, maturity_time_max = st.slider("Time to Maturity Range", 0.01, 10.0, (0.01, 10.0))
    rf_rate_min, rf_rate_max = st.slider("Risk-Free Interest Rate Range", 0.01, 1.0, (0.01, 1.0))



# Streamlit Dashboard
st.title("A Visual Framework for Pricing and Sensitivity Analysis of European Options")

# Add Small Break Between Upper and Lower Parts
st.markdown("---")

# Display Model Paramters
model_parameters = {
    'Asset Spot Price' : [spot_price],
    'Asset Strike Price' : [strike_price],
    'Time to Maturity (years)' : [maturity_time],
    'Volatility' : [volatility],
    'Risk-Free Interest Rate' : [rf_rate]
}

# Create a Pandas DataFrame Object & Delete Index Column for Display Purposes
parameters = pd.DataFrame(model_parameters)
st.dataframe(parameters, hide_index=True)

# Create Black-Scholes Model Object
model = bsm.BSM(spot_price, strike_price, rf_rate, maturity_time, volatility)

# Calculate Call and Put Prices
call_price = model.call_price()
put_price = model.put_price()

# Display Call and Put Values in colored tables
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="card-left">
        <div class="bar-green"></div>
        <div class="content">
            <div class="label label-green">📈 CALL Option</div>
            <div class="price">${call_price:.2f}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="card-left">
        <div class="bar-red"></div>
        <div class="content">
            <div class="label label-red">📉 PUT Option</div>
            <div class="price">${put_price:.2f}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.title("Modeling European Option Sensitivities in the Black-Scholes Framework")
# -----
# Delta:
st.subheader("Δ (Delta): Sensitivity of the Option Price to Underlying Asset Movements")
st.write("Delta quantifies the rate of change in an option's price with respect to changes in the underlying asset's price. It represents the first-order derivative of the option value and is a key measure of directional exposure.")
st.markdown("---")

# Create Meshgrid Object for Spot Prices & Volatilities
X, Y = meshgrid(spot_price_min, volatility_min, spot_price_max, volatility_max)

# Create a Model for Delta Sensitivies
delta_model = bsm.BSM(X, strike_price, rf_rate, maturity_time, Y)

# Calculate Call & Put Deltas
call_deltas = delta_model.delta_call()
put_deltas = delta_model.delta_put()

# Create Deltas Heatmap
fig = heatmap(X, Y, call_deltas, put_deltas, "Call Option Delta Heatmap", "Put Option Delta Heatmap", "Call Delta", "Put Delta", "Spot Price", "Volatility")
st.pyplot(fig)

# Add Small Break Between Upper and Lower Parts
st.markdown("---")
# -----
# Gamma:
st.subheader("Γ (Gamma): Sensitivity of Delta to the Option Price")
st.write("Gamma measures the rate of change of Delta with respect to the underlying asset's price. It reflects the curvature in the option's price profile and indicates how much the Delta will change as the underlying asset moves. High Gamma implies greater convexity and risk in Delta hedging.")
st.markdown("---")

# Create Meshgrid Object for Spot Prices & Volatilities
X, Y = meshgrid(spot_price_min, maturity_time_min, spot_price_max, maturity_time_max)

# Create a Model for Gammas Sensitivies
gamma_model = bsm.BSM(X, strike_price, rf_rate, Y, volatility)

# Calculate Call & Put Gammas
call_gammas = gamma_model.gamma()
put_gammas = gamma_model.gamma()

# Create Gammas Heatmap
fig = heatmap(X, Y, call_gammas, put_gammas, "Call Option Gamma Heatmap", "Put Option Gamma Heatmap", "Call Gamma", "Put Gamma", "Spot Price", "Time to Maturity (years)")
st.pyplot(fig)

# Add Small Break Between Upper and Lower Parts
st.markdown("---")
# -----
# Theta:
st.subheader("Θ (Theta): Sensitivity to Time Decay")
st.write("Theta measures the rate at which an option’s value declines over time, holding other variables constant. It captures the impact of time decay and is typically negative for long options, reflecting the erosion of extrinsic value as expiration approaches.")
st.markdown("---")

# Create Meshgrid Object for Spot Prices & Vollities
X, Y = meshgrid(spot_price_min, maturity_time_min, spot_price_max, maturity_time_max)

# Create a Model for Theta Sensitivies
theta_model = bsm.BSM(X, strike_price, rf_rate, Y, volatility)

# Calculate Call & Put Thetas
call_thetas = theta_model.theta_call()
put_thetas = theta_model.theta_call()

# Create Thetas Heatmap
fig = heatmap(X, Y, call_thetas, put_thetas, "Call Option Theta Heatmap", "Put Option Theta Heatmap", "Call Theta", "Put Theta", "Spot Price", "Time to Maturity (years)")
st.pyplot(fig)

# Add Small Break Between Upper and Lower Parts
st.markdown("---")
# -----
# Vega:
st.subheader("ν (Vega): Sensitivity to Volatility")
st.write("Vega represents the sensitivity of an option’s price to changes in the volatility of the underlying asset. A higher Vega implies that the option is more responsive to volatility shifts, which is particularly relevant for long-dated or at-the-money options.")
st.markdown("---")

# Create Meshgrid Object for Spot Prices & Volatilities
X, Y = meshgrid(spot_price_min, volatility_min, spot_price_max, volatility_max)

# Create a Model for Vega Sensitivies
vega_model = bsm.BSM(X, strike_price, rf_rate, maturity_time, Y)

# Calculate Call & Put Vega
call_vegas = vega_model.theta_call()
put_vegas = vega_model.theta_put()

# Create Vegas Heatmap
fig = heatmap(X, Y, call_vegas, put_vegas, "Call Option Vega Heatmap", "Put Option Vega Heatmap", "Call Vega", "Put Vega", "Spot Price", "Volatility")
st.pyplot(fig)

# Add Small Break Between Upper and Lower Parts
st.markdown("---")
# -----
# rho:
st.subheader("ρ (Rho): Sensitivity to Interest Rate Changes")
st.write("Rho quantifies the sensitivity of the option's price to changes in the risk-free interest rate. It is most relevant for long-dated options and reflects how discounting and forward pricing influence option valuation.")
st.markdown("---")

# Create Meshgrid Object for Spot Prices & Volatilities
X, Y = meshgrid(spot_price_min, rf_rate_min, spot_price_max, rf_rate_max)

# Create a Model for Rho Sensitivies
rho_model = bsm.BSM(X, strike_price, Y, maturity_time, volatility)

# Calculate Call & Put Rho
call_rhos = rho_model.rho_call()
put_rhos = rho_model.rho_put()

# Create Rho Heatmap
fig = heatmap(X, Y, call_rhos, put_rhos, "Call Option Rho Heatmap", "Put Option Rho Heatmap", "Call Rho", "Put Rho", "Spot Price", "Risk-Free Interest Rate")
st.pyplot(fig)
