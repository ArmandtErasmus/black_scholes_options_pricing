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
    page_title='Black-Scholes Option Pricing Model')

# Custom CSS to inject into Streamlit
st.markdown("""
<style>
/* Adjust the size and alignment of the CALL and PUT value containers */
.metric-container {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 8px; /* Adjust the padding to control height */
    width: auto; /* Auto width for responsiveness, or set a fixed width if necessary */
    margin: 0 auto; /* Center the container */
}

/* Custom classes for CALL and PUT values */
.metric-call {
    background-color: #8cd47e; /* Light green background */
    color: white; /* Black font color */
    margin-right: 10px; /* Spacing between CALL and PUT */
    border-radius: 10px; /* Rounded corners */
}

.metric-put {
    background-color: #d94b58; /* Light red background */
    color: white; /* Black font color */
    border-radius: 10px; /* Rounded corners */
}

/* Style for the value text */
.metric-value {
    font-size: 1.5rem; /* Adjust font size */
    font-weight: bold;
    margin: 0; /* Remove default margins */
}

/* Style for the label text */
.metric-label {
    font-size: 1rem; /* Adjust font size */
    margin-bottom: 4px; /* Spacing between label and value */
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
    spot_price_min, spot_price_max = st.slider("Spot Price Range", 0.0, 1000.0, (0.0, 1000.0))
    volatility_min, volatility_max = st.slider("Volatility Range", 0.0, 1.0, (0.0, 1.0))



# Streamlit Dashboard
st.title("Black-Scholes Options Pricing Model")

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

# Calculate Call and Put Prices
call_price = bsm.BSM(spot_price, strike_price, rf_rate, maturity_time, volatility).call_price()
put_price = bsm.BSM(spot_price, strike_price, rf_rate, maturity_time, volatility).put_price()

# Display Call and Put Values in colored tables
col1, col2 = st.columns([1,1], gap="small")

with col1:
    # Using the custom class for CALL value
    st.markdown(f"""
        <div class="metric-container metric-call">
            <div>
                <div class="metric-label">CALL Value</div>
                <div class="metric-value">${call_price:.2f}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    # Using the custom class for PUT value
    st.markdown(f"""
        <div class="metric-container metric-put">
            <div>
                <div class="metric-label">PUT Value</div>
                <div class="metric-value">${put_price:.2f}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.title("Modeling European Option Sensitivities in the Black-Scholes Framework")
# -----
# Delta:
st.subheader("Δ (Delta): Sensitivity of the Option Price to Underlying Asset Movements")
st.write("Delta measures how much an option's price is expected to change for a small change in the underlying asset's price.")
st.markdown("---")
# Create Meshgrid Object for Spot Prices & Volatilities
X, Y = meshgrid(spot_price_min, volatility_min, spot_price_max, volatility_max)

# Calculate Call & Put Deltas
call_deltas = bsm.BSM(X, strike_price, rf_rate, maturity_time, Y).delta_call()
put_deltas = bsm.BSM(X, strike_price, rf_rate, maturity_time, Y).delta_put()

# Create Deltas Heatmap
fig = heatmap(X, Y, call_deltas, put_deltas, "Call Option Delta Heatmap", "Put Option Delta Heatmap", "Call Delta", "Put Delta", "Spot Price", "Volatility")
st.pyplot(fig)

# -----