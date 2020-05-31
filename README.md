# Predicting-soccer-player-market-value
 Project _Tilburg University_
 
 This is a private repository dedicated to my project.
 Next to the .py dedicated for data science purposes, data-visualization scripts & data, it also
 contains a scraper that scrapes Transfermarkt and SoFIFA
 in order to create a comprehensive dataset.
 
 This research uses the Transfermarkt's market value estimate
 **and** reported transfer fee as ground-truth labels.
 Each data-point is a transfer originating from the season of 2008 up until the season of 2019
 from 7 Soccer leagues of Europe namely:
 
     - Eredivisie (Netherlands)
     - Premier League (England)
     - Primera Division (Spain)
     - Primeira Liga (Portugal)
     - Serie A (Italy)
     - Ligue 1 (France)
     - Bundesliga (Germany)
 
 I tried to determine both market value and transfer-fee based on player performance,
 player characteristics and transfer details.
 After reducing dimensionality these were the final variables that were used:
 
     - FIFA Player rating
     - FIFA Player potential
     - Player age
     - Total season goals
     - Total season assists
     - Total minutes played
     - Remaining contract duration
     - Season
 
 The ANN and Random-Forest models were fairly simple. Cross-validation + hyper-parameter tuning was done but it did not increase the performance of the models, hence simple models were used.

 **Data-set:**
 
    N - Total     : 6633
    N - Test set  : 1990
    N - Train set : 4643
    
    
 **Tests:**
    
        - Predicting soccer-player market value
        - Predicting soccer-player transfer-fee without the market-value as a predictor

Transfer-fee and Market value were predicted and are expressed in million £. Predicting transfer fee was significantly more complex due to the large variance. Best results were obtained with the ANN model for the prediction of market value, where the model was able to explain for 80% of the data's variance (R2 = 0.80). However, results did not significantly differ from the Random-Forest model. 

 ## **Results** _(Predicting market-value)_
 

 - *ANN*:
 
     ![Alt Text](https://github.com/RZME/Predicting-soccer-player-market-value/blob/master/results_market_value/ANN-R2-plot.png?raw=true)
     
     ![Alt Text](https://github.com/RZME/Predicting-soccer-player-market-value/blob/master/results_market_value/ANN-error-distribution.png?raw=true)
     
     ![Alt Text](https://github.com/RZME/Predicting-soccer-player-market-value/blob/master/results_market_value/ANN-loss-vs-epochs.png?raw=true)
             
 - *Random-Forest regression*:
 
     ![Alt Text](https://github.com/RZME/Predicting-soccer-player-market-value/blob/master/results_market_value/Random-Forest-regression-R2-plot.png?raw=true)
     
     ![Alt Text](https://github.com/RZME/Predicting-soccer-player-market-value/blob/master/results_market_value/Random-Forest-regression-error-distribution.png?raw=true)
          
 - *Linear regression*:
 
     ![Alt Text](https://github.com/RZME/Predicting-soccer-player-market-value/blob/master/results_market_value/Linear-regression-R2-plot.png?raw=true)
     
     ![Alt Text](https://github.com/RZME/Predicting-soccer-player-market-value/blob/master/results_market_value/Linear-regression-error-distribution.png?raw=true)
         

## **Results** _(Predicting transfer-fee)_

 - *ANN*:
 
     ![Alt Text](https://github.com/RZME/Predicting-soccer-player-market-value/blob/master/results_transfer_fee/ANN-R2-plot.png?raw=true)
     
     ![Alt Text](https://github.com/RZME/Predicting-soccer-player-market-value/blob/master/results_transfer_fee/ANN-error-distribution.png?raw=true)
    
     ![Alt Text](https://github.com/RZME/Predicting-soccer-player-market-value/blob/master/results_transfer_fee/ANN-loss-vs-epochs.png?raw=true)
         
 - *Random-Forest regression*:
 
     ![Alt Text](https://github.com/RZME/Predicting-soccer-player-market-value/blob/master/results_transfer_fee/Random-Forest-regression-R2-plot.png?raw=true)
     
     ![Alt Text](https://github.com/RZME/Predicting-soccer-player-market-value/blob/master/results_transfer_fee/Random-Forest-regression-error-distribution.png?raw=true)
          
 - *Linear regression*:
 
     ![Alt Text](https://github.com/RZME/Predicting-soccer-player-market-value/blob/master/results_transfer_fee/Linear-regression-R2-plot.png?raw=true)
     
     ![Alt Text](https://github.com/RZME/Predicting-soccer-player-market-value/blob/master/results_transfer_fee/Linear-regression-error-distribution.png?raw=true)
         
