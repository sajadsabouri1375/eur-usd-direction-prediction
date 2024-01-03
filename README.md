# Forex Direction Prediction Basilica
This repository includes python programs required to test EUR/USD positive/negative direction prediction for Basilica company.

## Get EUR/USD DATA
To gather required data for modelling, we need a data provider with the ability to provide historical data (for several years) at intervals of interest.

There are plenty of APIs out there to provide required data:

    1) Alpha Vantage: Alpha Vantage provides EUR/USD candles at 1-min to monthly candles. This API is limited to 25 requests per day.
    Furtheremore, Alpha Vantage does not provide adjusted data as part of its free plan. You need a premium plan to get such data.

    2) Yahoo Finance: Yahoo Finance is a great data provider with less limitations than Alpha Vantage. Unfortunately this API is out of service currently.

For now, Alpha Vantage with daily candles is used as the main time series for the analysis of this task. If required, we may request timeseries with shorter intervals later.
