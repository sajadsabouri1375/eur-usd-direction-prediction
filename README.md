# Forex Direction Prediction Basilica
This repository includes python programs required to test EUR/USD positive/negative direction prediction for Basilica company.

## Get EUR/USD Data
To gather required data for modelling, we need a data provider with the ability to provide historical data (for several years) at intervals of interest.

There are plenty of APIs out there to provide required data:

    1) Alpha Vantage: Alpha Vantage provides EUR/USD candles at 1-min to monthly candles. This API is limited to 25 requests per day.
    Furtheremore, Alpha Vantage does not provide adjusted data as part of its free plan. You need a premium plan to get such data.
    2) Yahoo Finance: Yahoo Finance is a great data provider with less limitations than Alpha Vantage. Unfortunately this API is out of service currently.
    3) Trader Made: This is another data provider which returns EUR/USD historical data yearly (We need almost 20 requests to extract 20-year historical data). 
    This API provides 1000 free requests, but does not provide volume.
    4) YFinance: YFinance is a great library to request Forex/Cryptocurrency historical data. This library provides the longest historical data, therefore
    it is a great choice for ML modelling.

".py" scripts explained:
- data_provider_abstract.py: This script includes shared properties and methods of all data provider classes.
All data provider classes must inherit from this class. Note that this class could not be instantiated by itself.
- data_provider_alpha_vantage.py: This script contains methods and properties to request data from Alpha Vantage API. 
- test_data_provider_alpha_vantage.py: This is a test script which you could run to test main methods of Alpha
Vantage data provider class.
- data_provider_trader_made.py: This script implements required methods to request and store data from TraderMade API.
- test_data_provider_trader_made.py: This script is designed to test functionalities of TraderMade API calls.
- data_provider_yfinance.py: This script includes methods to get data from yfinance provider.
- test_data_provider_yfinance.py: This is a test scripts to test whether yfinance provides data properly or not. 

Conclusion:
Unfortunately, none of the providers tested provide "Volume" field properly. Thus, only OHLC fields of Alpha Vantage API provider would be used in modelling.

## Preprocess Data
To make sure that the downloaded timeseries is valid, we need to verify some stuff:

- Renaming Fields: The raw dataset might not have proper naming. Fields' names might need to change.
- Time Integrity: Obviously, the timeseries must have timestamps sorted in order, from the farther date, to the most recent one.
- OHLC Integrity: Fields "Open", "Close", "High", and "Low" must have reasonable order. "High" must be the highest value, "Low" must be the lowest value, 
"Open" and "Close" must be somewhere between "High" and "Low".
- Missing Values: All main 4 fields of the candles must have values. If there are missing values, we need to fill them with appropriate alternatives.
- Type Integrity: All main 4 fields must be of type float. 
- Forex market hours are from Monday to Friday. Thus, there must not be values on Saturdays and Sundays.
- Filterin Columns which are not useful.