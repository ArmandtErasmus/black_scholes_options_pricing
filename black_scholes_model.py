# Import libraries to help with calculations
import numpy as np
from scipy.stats import norm

class BSM:

    # Class Constructor with Black-Scholes Model Input Parameters
    def __init__(self, spot_price, strike_price, rf_rate, maturity_time, volatility):
        """
        Parameters
        ----------
        spot_price : float
            The current market price of the underlying asset.
        strike_price : float
            The price at which the option holder can buy the underlying asset.
        rf_rate : float
            The risk-free interest rate (annualized).
        maturity_time : float
            The time to expiration of the option, in years.
        volatility : float
            The annualized standard deviation of the asset's returns (volatility).
        """

        self.spot_price = spot_price
        self.strike_price = strike_price
        self.rf_rate = rf_rate
        self.maturity_time = maturity_time
        self.volatility = volatility
    
    # Calculate the Call Price
    def call_price(self):
        """
        Calculates the theoretical price of a European call option using the Black-Scholes formula.

        Returns
        -------
        price : float
            The theoretical price of a European call option.
        """

        d_1 = (np.log(self.spot_price / self.strike_price) + (self.rf_rate + 0.5 * self.volatility ** 2) * self.maturity_time) / (self.volatility * np.sqrt(self.maturity_time))
        d_2 = d_1 - self.volatility * np.sqrt(self.maturity_time)
    
        normed_d_1 = norm.cdf(d_1)
        normed_d_2 = norm.cdf(d_2)

        price = self.spot_price * normed_d_1 - self.strike_price * np.exp(-self.rf_rate * self.maturity_time) * normed_d_2

        return price

    # Calculate the Put Price
    def put_price(self):
        """
        Calculates the theoretical price of a European put option using the Black-Scholes formula.

        Returns
        -------
        price : float
            The theoretical price of a European put option.
        """

        d_1 = (np.log(self.spot_price / self.strike_price) + (self.rf_rate + 0.5 * self.volatility ** 2) * self.maturity_time) / (self.volatility * np.sqrt(self.maturity_time))
        d_2 = d_1 - self.volatility * np.sqrt(self.maturity_time)
        
        normed_d_1 = norm.cdf(-d_1)
        normed_d_2 = norm.cdf(-d_2)

        price = self.strike_price * np.exp(-self.rf_rate * self.maturity_time) * normed_d_2 - self.spot_price * normed_d_1

        return price
    
    # Helper Methods to Compute d_1 and d_2
    def d1_d2(self):
        d_1 = (np.log(self.spot_price / self.strike_price) + (self.rf_rate + 0.5 * self.volatility ** 2) * self.maturity_time) / (self.volatility * np.sqrt(self.maturity_time))
        d_2 = d_1 - self.volatility * np.sqrt(self.maturity_time)
        return d_1, d_2

    # Calculating the Greeks
    def delta_call(self):
        d1, _ = self.d1_d2()
        return norm.cdf(d1)

    def delta_put(self):
        d1, _ = self.d1_d2()
        return norm.cdf(d1) - 1

    def gamma(self):
        d1, _ = self.d1_d2()
        return norm.pdf(d1) / (self.spot_price * self.volatility * np.sqrt(self.maturity_time))


    def vega(self):
        d1, _ = self.d1_d2()
        return (self.spot_price * norm.pdf(d1) * np.sqrt(self.maturity_time)) / 100  # Per 1% vol change


    def theta_call(self):
        d1, d2 = self.d1_d2()
        term1 = - (self.spot_price * norm.pdf(d1) * self.volatility) / (2 * np.sqrt(self.maturity_time))
        term2 = - self.rf_rate * self.strike_price * np.exp(-self.rf_rate * self.maturity_time) * norm.cdf(d2)
        return term1 + term2

    def theta_put(self):
        d1, d2 = self.d1_d2()
        term1 = - (self.spot_price * norm.pdf(d1) * self.volatility) / (2 * np.sqrt(self.maturity_time))
        term2 = self.rf_rate * self.strike_price * np.exp(-self.rf_rate * self.maturity_time) * norm.cdf(-d2)
        return term1 + term2


    def rho_call(self):
        _, d2 = self.d1_d2()
        return self.strike_price * self.maturity_time * np.exp(-self.rf_rate * self.maturity_time) * norm.cdf(d2)

    def rho_put(self):
        _, d2 = self.d1_d2()
        return -self.strike_price * self.maturity_time * np.exp(-self.rf_rate * self.maturity_time) * norm.cdf(-d2)
