# A Visual Framework for Pricing and Sensitivity Analysis of European Options

---

![dashboard](https://github.com/ArmandtErasmus/black_scholes_options_pricing/blob/main/BSM_FRAMEWORK_SHOWCASE.png)

# Try it out! Visit the Dashboard Below:
[Demo](https://blackscholesframework.streamlit.app/)

---

### Table of Contents
1. [Introduction](#1.-Introduction)
2. [Features](#2.-Features)
3. [Installation](#3.-Installation)
4. [Usage](#4.-Usage)
5. [Contributing](#5.-Contributing)
6. [License](#6.-License)

---

### 1. Introduction

This Streamlit web application provides a hands-on way to explore the Black-Scholes model for options pricing. It includes:

- Real-time calculation of European option prices (calls and puts).
- Interactive sliders and inputs for model parameters.
- Visualization of option price sensitivity to inputs.
- Display of Greeks (Delta, Gamma, Theta, Vega, Rho).

---

### 2. Features

## Application Structure
The app is structured around core Black-Scholes concepts and includes:

- Option Pricing
- Option Greeks

## Inputs (Sidebar Controls)

| Parameter        | Description                                               |
|------------------|-----------------------------------------------------------|
| **Option Type**  | Call or Put                                               |
| **Stock Price**  | Current price of the underlying asset                     |
| **Strike Price** | Exercise price of the option                              |
| **Time to Maturity** | In years (e.g., 1.0 = 1 year)                       |
| **Volatility**   | Annualized volatility of the underlying asset (σ)         |
| **Risk-Free Rate** | Annualized continuously compounded rate (e.g., 0.05) |

## Mathematical Model

### Black-Scholes Formula (no dividends)
For a European **Call**:

    C = S * N(d₁) - K * e^(−rT) * N(d₂)

For a European **Put**:

    P = K * e^(−rT) * N(−d₂) - S * N(−d₁)

Where:

    d₁ = [ln(S/K) + (r + σ²/2)T] / (σ√T)
    d₂ = d₁ − σ√T

- `N(x)` is the cumulative distribution function of the standard normal distribution.

## Option Greeks Displayed
- **Delta**: Sensitivity to stock price
- **Gamma**: Sensitivity of delta to stock price
- **Theta**: Time decay
- **Vega**: Sensitivity to volatility
- **Rho**: Sensitivity to interest rate

## Visual Components
- Option price chart vs. strike price
- Option price chart vs. stock price
- Heatmaps for price and Greeks

---

### 3. Installation

To run the dashboard, follow these steps:
1. Clone the repository:
`git clone https://github.com/ArmandtErasmus/black_scholes_options_pricing`
2. Navigate into the project directory and install dependencies:
`pip install -r requirements.txt`

### 4. Usage

After installing, run the application using:
`streamlit run streamlit_app.py`

This will launch the dashboard in your default web browser.

---

### 5. Contributing

Contributions are encouraged! Whether it’s fixing bugs, improving layout, or adding new models (like Binomial Trees or Greeks visualizations), feel free to get involved.

#### Potential Improvements:
- Support for American options (e.g., binomial pricing).
- Implied volatility calculator.
- Side-by-side comparison of options strategies (e.g., spreads, straddles).
- Integration with live data APIs (e.g., Yahoo Finance).

#### How to Contribute:
1. Fork the repo.
2. Create a feature branch (`git checkout -b feature-name`).
3. Make and commit changes (`git commit -m 'Add new feature'`).
4. Push to GitHub (`git push origin feature-name`).
5. Submit a pull request.

---

### 6. License

Distributed under the MIT License. See `LICENSE` for more information.
