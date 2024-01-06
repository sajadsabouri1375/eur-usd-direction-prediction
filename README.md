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
Unfortunately, none of the providers tested provide "Volume" field properly. Thus, only OHLC fields of YFinance API for candles in 60min interval 
for 2 years is provided. Note that YFinance does not provide data which are past more than 730 days.

## Preprocess Data
To make sure that the downloaded timeseries is valid, we need to verify some stuff:

- Renaming Fields: The raw dataset might not have proper naming. Fields' names might need to change.
- Time Integrity: Obviously, the timeseries must have timestamps sorted in order, from the farther date, to the most recent one.
- OHLC Integrity: Fields "Open", "Close", "High", and "Low" must have reasonable order. "High" must be the highest value, "Low" must be the lowest value, 
"Open" and "Close" must be somewhere between "High" and "Low".
- Missing Values: All main 4 fields of the candles must have values. If there are missing values, we need to fill them with appropriate alternatives.
- Type Integrity: All main 4 fields must be of type float. 
- Forex market hours are from Monday to Friday. Thus, there must not be values on Saturdays and Sundays.
- Filtering Columns which are not useful.

".py" scripts explained:
- data_preprocessing.py: This scripts contains required classes to verify data integrity and prepareing dataset for feature extraction.
- test_data_preprocessing.py: This script would verify dataset integrity and make sure that the dataset is ready to be used for feature extraction.

## Feature Extraction

### Input Features
Now that we have prepared a verified dataset for EUR/USD timeseries, we need to do a perfect analysis to find as many useful features as possible.
Features of raw dataset are:
- Open
- Close
- High
- Low
- Day of Week
- Hour of Day
- Day of Year
- Month Index

Unfortunately "Volume" feature is missed, because none of the data providers provided proper amount of "Volume".

But these feature are not enough. We need more insightful features, like indicators, date features like specific events, holidays, and etc.
Candidate extra features per day are:
- Is Holiday? -> holidays data are important, because on holidays (which are not weekend), market is sort of closed, but data is available.
- Has Event?
- Event Sentiment
- Moving Averages (Simple and exponentially weights)
- Relative Strengh Index
- Average True Range

Note that evaluation of sentiments of each holiday and event is way beyond the context of this 1-day task.

### Output Features
We would also add output feature (label) for each day. Days which demonstrate a significant rise in EUR/USD price relative to the previous day are labelled as 1,
those that show a significant negative deviation from previous day are labelled as -1, and finally the days which do not have a significant change relative to previous day
are labelled as 0.
To find the threshold based on which the level of significance is determined, we fit a normal distribution with 0 as mean and standard deviation of the daily price changes, 
and we find Percent Point Function (PPF) of 33% and 67%.
Using this methodology, -0.003 and +0.003 are thresholds by which labels are determined.

".py" scripts explained:
- feature_extraction.py: This script would generate all date and indicator features which would be potentially correlated with the output feature.
- test_feature_extraction.py: This is a test script which would test all methods of feature extraction class.
- indicator_utils.py: This static class includes all utility funcitons which are required to calculate indicators.

## Feature Selection
To make up our mind about the final features, we need to do feature selection analysis and make sure that all features are reasonably correlated with the output feature.
Note that finding correlations between output feature and series is not easy to visualize. Thus, we demonstrated categorical and continuous features against output
feature by shifting data only 1 step.

".py" scripts explained:
- feature_selection.py: This script would generate all plots required to visualize correlation between input and output feature.
- test_feature_selection.py: This is a test script which would test all methods of feature selection class.
- plot_utils.py: This static class includes all utility funcitons which are required to plot different plots of interest.

## Model
To predict future EUR/USD price change direction, we used an LSTM model. LSTM is a Recurrent Neural Network (RNN) which can handle a larger history of data, which makes it
perfect for timeseries analysis. All the input features are used as series with up to 30 step shifting. 
The model architecture consists of an LSTM layer with 30 LSTM cells. The output layer is a softmax layer with 3 neurons to predict the class of EUR/USD price change direction.
The output labels are "Significant Drop", "Almost Constant", and "Significant Rise".
The moodel was fit and showed a 47% for training, 46% for validation, and 41%. Although the accuracies are not great, but we need to remember that we are modelling a 
very complex and variant problem which is controlled by plenty of factors. The features that we currently have are not sufficient for the perfect modelling, but it is
much better than the baseline model yet (with 33% accuracy), which shows the model is learning some real stuff.
Confusion matrices for training and test phase are also included in /outputs/plots/ to give a better understanding of modelling. Also, accuracy, precision, recall, and F1 score
metrics are stored in metrics.json file.
Baseline model for this project is a naive model which outputs the most frequent class all the time. The accuracy for such model would be about 33%. Thus, our model must
outperform this baseline model with a significant difference, which it has.

".py" scripts explained:
- model.py: This scripts includes LstmModel which is responsible 1) to convert dataset into a set which is applicable to model architecture, 2) Design model architecture, 3) Fit model, 
4) Generate results (confusion matrix, accuracy, recall, precision), and 5) split dataset into "Trainng", "Test", and "Validation" sets.
- test_model.py: This script runs model and tests the model accuracy againt the baseline model.