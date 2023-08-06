"""Asset class."""

import datetime
from abc import ABC, abstractmethod
from typing import Tuple, Union
# import matplotlib.pyplot as plt
import pandas as pd
# import seaborn as sns

pd.plotting.register_matplotlib_converters()


class Asset(ABC):
    """Asset class. The base class of all assets. Asset is an abstract class and needs a
    mixin to become concrete. Assets can report price information and display graphs.
    """

    def __init__(self, ticker):
        self.ticker = ticker

    def p(self):
        """Convenience method to print the asset."""
        print(str(self))

    @abstractmethod
    def get_price_history(self) -> pd.DataFrame:
        """Return the price history as a DataFrame of dates and close prices."""

    def get_latest_price(self) -> Tuple[datetime.datetime, float]:
        """Return the latest price including the date."""
        return self.get_price_history().iloc[-1]
        # FIXME Check if this return statement is inline with the type hint.

    def lookup_price(self, date: Union[str, datetime.datetime]):
        """Look up price at given date."""
        return self.get_price_history().loc[date]

    # def pricegraph(self, monthsback=6):
    #     """Display this stock's price graph over the last monthsback months.

    #     Returns from_date, fig, and ax in order for subclass functions to add to the
    #     information and even the graph displayed here.
    #     """
    #     fig, ax = plt.subplots(figsize=(16, 8))
    #     hist = self.price_history()

    #     # Calc start date:
    #     from_date = datetime.date.today() - pd.offsets.DateOffset(months=monthsback)
    #     from_date = from_date.strftime("%Y-%m-%d")

    #     # Plot the prices:
    #     sns.lineplot(ax=ax, data=hist.loc[from_date:, "close"], marker="o").set(
    #         title=self.ticker
    #     )

    #     # Derive todayprice. Note that we use do not use self.todayprice here because
    #     # that attribute is often one day behind which affects the calculations below.
    #     # So we simply take the last entry in the history so the numbers fit with the
    #     # graph.
    #     todayprice = hist.iloc[-1]["close"]

    #     # Print some stats about the stock:
    #     print(f"{self.ticker}")
    #     print("Latest price: {:.2f}".format(todayprice))
    #     maxprice = hist[hist.index > from_date].max().close
    #     print("Drop since max: {:2.0%}".format((todayprice - maxprice) / maxprice))

    #     return from_date, fig, ax
