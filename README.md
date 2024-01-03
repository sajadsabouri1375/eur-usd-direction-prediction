# Forex Direction Prediction Basilica
This repository includes python programs required to test EUR/USD positive/negative direction prediction for Basilica company.

## Get EUR/USD DATA
To gather required data for modelling, we need a data provider with the ability to provide historical data (for several years) at intervals of interest.

There are plenty of APIs out there to provide required data:

    1) Alpha Vantage: Alpha Vantage provides EUR/USD candles at 1-min to monthly candles. This API is limited to 25 requests per day.
    Furtheremore, Alpha Vantage does not provide adjusted data as part of its free plan. You need a premium plan to get such data.

    2) Yahoo Finance: Yahoo Finance is a great data provider with less limitations than Alpha Vantage. Unfortunately this API is out of service currently.

    3) Trader Made: This is another data provider which returns EUR/USD historical data yearly (We need almost 20 requests to extract 20-year historical data). 
    This API provides 1000 free requests, but does not provide volume.

".py" scripts explained:
- data_provider_abstract.py: This script includes shared properties and methods of all data provider classes.
All data provider classes must inherit from this class. Note that this class could not be instantiated by itself.
- data_provider_alpha_vantage.py: This script contains methods and properties to request data from Alpha Vantage API. 
- test_data_provider_alpha_vantage.py: This is a test script which you could run to test main methods of Alpha
Vantage data provider class.
- data_provider_trader_made.py: This scripts implements required methods to request and store data from TraderMade API.
- test_data_provider_trader_made.py: This script is designed to test functionalities of TraderMade API calls.
