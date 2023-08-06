"""Retrieve and store fx data and provide access to it. Make sure the fx data is not
loaded too often.

The API returns list of dictionaries and _pickkey is used to access the correct key in
those dictionaries.

Note: This module's code is not as straightforward as it could be because, historically,
it supported multiple data sources (namely, Alphavantage). After getting rid of those
sources, I didn't streamline the module yet.
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Any, Callable
import investpy

logger = logging.getLogger(__name__)

# Set things up:
_currencypairs = ["USD/CHF", "EUR/CHF", "USD/EUR", "CHF/EUR"]
# The key we pick for the price data -- must be global, will be set later:
_pickkey = None  #  pylint: disable=invalid-name
_source = None  # Will later contain the data source pylint: disable=invalid-name
_fxdata = {}


def _get_investing_data(currencypair):
    # Get the data:
    res = investpy.get_currency_cross_historical_data(
        f"{currencypair}",
        from_date="01/01/2015",
        to_date=datetime.now().strftime("%d/%m/%Y"),
        as_json=True,
    )
    # Turn it into the right format:
    data = {}
    for entry in json.loads(res)["historical"]:
        (day, month, year) = entry["date"].split("/")
        data[f"{year}-{month}-{day}"] = entry
    return data


def setup():
    """Retrieve all fx data and store it in the cache (_fxdata)."""
    global _fxdata, _pickkey, _source  # pylint: disable=global-statement,invalid-name
    for currencypair in _currencypairs:
        logger.info("Getting fx data for %s", currencypair)
        data = _get_investing_data(currencypair)
        _pickkey = "close"
        _source = "Investing"
        _fxdata[currencypair] = data


def scanner(date: str, lookup_callback: Callable[[str], Any]) -> Any:
    """Return lookup_callback(date). If the callback results in a KeyError, scan back
    from date until some valid result is returned (or 100 tries exceeded).

    This function is generic and being used not only by this module.

    Args:
    - date: E.g., "2020-11-01"
    - lookup_callback: Looks up a date (given as a string such as "2020-11-01") and
      returns the value at that date -- or raises KeyError. The return value can be of
      any type.
    """
    adjdate_as_string = date
    tries = 0
    while True:
        try:
            return lookup_callback(adjdate_as_string)
        except KeyError:
            pass
        adjdate = datetime.strptime(adjdate_as_string, "%Y-%m-%d") + timedelta(-1)
        adjdate_as_string = datetime.strftime(adjdate, "%Y-%m-%d")
        tries += 1
        if tries > 2:
            logger.warning("Needed %s tries to retrieve data", tries)
        if tries > 100:
            raise RuntimeError(f"Needing way too many tries to find data for {date}")


def create_lookup_exception(
    from_exception: Exception,
    currency: str,
    target_currency: str,
    date: str,
    last_date: str,
    additional_msg: str = "",
):
    """Helper function that raises the correct exception with all the relevant
    information when a lookup fails.

    Args:
    - from_exception: Raise from this exception
    - currency, target_currency: Currency pair being looked up
    - date: Date that is being looked up
    - last_date: The last date for which we have exchange data
    - additional_msg: To add something to the message
    """
    # Check if the fx data is stale so we can warn the user:
    then = datetime.strptime(last_date, "%Y-%m-%d")
    msg = ""
    if (datetime.now() - then).days >= 100:
        msg = """
### 
### FX DATA SEEMS TO BE STALE
### Either something's wrong with api.fx.setup() or, if this is raised in a test, 
### you need to update the fxdata pickle via picklemap.
### 
"""
    msg += additional_msg
    raise RuntimeError(
        f"Lookup failed for {currency} -> {target_currency} at {date} {msg}"
    ) from from_exception


def lookup(currency, date, target_currency="CHF"):
    """Look up currency exchange rate.

    For robustness, this function uses scanner to try further dates in the past if the
    given date does not exist in the pre-fetched data.
    """
    if _fxdata == {}:
        # Fetch all the data if not done yet; we do this here instead of
        # the module level because it makes it easier to detect tests
        # that want to access the network.
        setup()

    currencypair = f"{currency}/{target_currency}"
    try:
        return scanner(date, lambda when: float(_fxdata[currencypair][when][_pickkey]))
    except RuntimeError as exc:
        create_lookup_exception(
            exc, currency, target_currency, date, list(_fxdata[currencypair].keys())[-1]
        )
