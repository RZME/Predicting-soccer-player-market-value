# %%
"""
### Importing modules
"""

# %%
import pickle

import keras
import numpy as np
import pandas as pd
from keras.callbacks import EarlyStopping
from keras.layers import Dense
from keras.models import Sequential
from matplotlib import pyplot
from pandas.errors import EmptyDataError
from sklearn import metrics
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
import _pickle as cPickle


from testing_utils.testing_utils import print_results, drop_col_feat_imp, display_graphs, norm

# %%
"""
### Declaring constants
"""

# %%
leagues = ["premier-league", "primera-division", "serie-a",
           "1-bundesliga", "ligue-1", "primeira-liga", "eredivisie"]

categories = ['club', 'club_league', 'club_country',
              'transfer_movement', 'player_nationality',
              'player_club', 'player_club_country',
              'player_position', 'player_position_category',
              'club_involved', 'club_involved_league',
              'club_involved_country', 'season']

# %% md
"""
# *Loading data*
"""

# %%
dfs = []
for year in range(2008, 2020):
    for league in leagues:
        try:
            dfs.append(pd.read_csv("soccer_data/{}-".format(league) + str(year) + ".csv"))
        except EmptyDataError:
            var = None
        except FileNotFoundError:
            var = None

df = pd.concat(dfs)

# %%
"""
# *Cleaning data*
"""

# %% md
"""
### • Dropping un-named columns
"""

# %%
for key in df.keys():
    if str(key).__contains__('Unnamed'):
        df = df.drop(columns=key)
# %% md
"""
### • Dropping nonnumericals transfer-fee and market-value
"""

# %%
df = df[df['transfer_fee'] != '-']
df = df[df['market_value'] != '-']
# %% md
"""
### • Converting data-types
"""
# %%
df['market_value'] = df['market_value'].astype(float)
df['player_rating'] = df['player_rating'].astype(float)
df['transfer_fee'] = df['transfer_fee'].astype(float)
# %% md
"""
### • Dropping N.A. rows transfer-fee
"""

# %%
df = df.dropna(subset=['transfer_fee'])
# %% md
"""
### • Dropping duplicates
"""

# %%
df = df.sort_values(by='transfer_movement')
df.drop_duplicates(subset=["player_name",
                           "season",
                           "player_age",
                           "player_nationality"], keep="first", inplace=True)
print(df.shape)
# %% md
"""
### • Dropping N.A. values player-rating
"""
# %%
df = df.dropna(subset=['player_rating'])
# %% md
"""
### • Dropping market value transfers below < 0.1 million pounds
### • Exporting data
"""
# %%
df = df[df['market_value'] > 0.1]
df.to_csv('data-set.csv')
# %% md
"""
### • Printing descriptive summary test
"""
# %%
print(df.describe())
# %%
"""
### • Categorizing data
"""
# %%
for category in categories:
    df[category] = df[category].astype('category')
print(df.keys())

cat_columns = df.select_dtypes(['category']).columns
df[cat_columns] = df[cat_columns].apply(lambda x: x.cat.codes)

# %%
"""
### • Checking correlation market-value vs transfer-fee of Transfermarkt predictions
"""
# %%
TM_y = df['transfer_fee']
TM_y_predict = df['market_value']

print('TM Mean Absolute Error:', metrics.mean_absolute_error(TM_y, TM_y_predict))
print('TM Mean Squared Error:', metrics.mean_squared_error(TM_y, TM_y_predict))
print('TM Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(TM_y, TM_y_predict)))
print('TM R^2 Score:', r2_score(TM_y, TM_y_predict))

display_graphs(TM_y_predict, TM_y, "TM", 'results_transfer_fee')

# %%
"""
# *Pre-test setup*
"""
# %%
"""
### • Dropping player-name column
"""
# %%
df = df.drop(columns='player_name')
print(df.shape)
# %%
"""
### • Specifying X and target variable
#### Dropping features with low importance
"""
# %%
y = df['market_value']
X = df.drop(columns=['transfer_fee',
                     'transfer_movement',
                     'market_value',
                     'player_position_category',
                     'player_club',
                     'player_club_country',
                     'player_nationality',
                     'player_position',
                     'remaining_contract_duration',
                     'club',
                     'total_minutes_per_point',
                     'total_apps',
                     'total_apps_ratio',
                     'el_minutes_played',
                     'el_assists',
                     'el_goals',
                     'el_apps',
                     'el_apps_ratio',
                     'el_minutes_per_point',
                     'ucl_apps',
                     'ucl_assists',
                     'ucl_minutes_played',
                     'ucl_goals',
                     'ucl_apps_ratio',
                     'ucl_minutes_per_point',
                     'club_involved_country',
                     'club_involved',
                     'club_country',
                     'club_involved_league',
                     'club_league',
                     'club_league_tier',
                     'club_involved_league_tier'])
print(X.keys())

# %%
"""
### • Splitting variables in train/test sets
"""

# %%
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
# %%
"""
### • Normalizing data
"""
# %%
train_stats = X_train.describe()
train_stats = train_stats.transpose()
train_stats.to_csv('train_stats.csv')
normed_train_data = norm(X_train, train_stats)
normed_test_data = norm(X_test, train_stats)

# %%
"""
# *Testing different models*
"""

"""
> ##  ANN
"""


# %%
def create_mlp():
    m = Sequential()
    m.add(Dense(8, input_shape=[len(X_train.keys())], activation='relu'))
    m.add(Dense(16, activation='relu'))
    m.add(Dense(1))
    return m


batch_size = 16
epochs = 1000

model = create_mlp()
optimizer = keras.optimizers.RMSprop(0.001)
es = EarlyStopping(monitor='val_loss', patience=10)
model.compile(loss="mse", optimizer=optimizer, metrics=['mae', 'mse'])
print(model.summary())

history = model.fit(normed_train_data, y_train, validation_data=(normed_test_data, y_test),
                    epochs=epochs, batch_size=batch_size, callbacks=[es])
hist = pd.DataFrame(history.history)

test_predictions = model.predict(normed_test_data).flatten()

_, train_mae, train_mse = model.evaluate(normed_train_data, y_train, verbose=0)
_, test_mae, test_mse = model.evaluate(normed_test_data, y_test, verbose=0)

print('\n')
print("ANN")
print('Results:')
print('Test R^2 score:', r2_score(y_test, test_predictions))
print('Test Mean Absolute Error:', test_mae)
print('Test Mean Squared Error:', test_mse)
print('Test Root Mean Squared Error:', np.sqrt(test_mse))
display_graphs(test_predictions, y_test, "ANN", "results_market_value")
print(normed_train_data.keys())

with open('final_ann_model', 'wb') as f:
    cPickle.dump(model, f)

# %%
"""
### • Plotting the train/test loss
"""

# %%
pyplot.plot(hist['loss'], label='train')
pyplot.plot(hist['val_loss'], label='test')
pyplot.legend()
pyplot.ylabel('MSE')
pyplot.xlabel('Epochs')
pyplot.title('Train/Test loss graph over epochs')
pyplot.savefig("results_market_value/" + 'ANN' + "-loss-vs-epochs")
pyplot.show()

# %%
"""
> ##  Random-Forest Regression
"""

# %%
rf = RandomForestRegressor()

# %%
"""
### • Displaying feature importances
"""

# %%
# print(drop_col_feat_imp(rf, X_train, y_train))

# %%
"""
### • Fitting and training the Random-Forest regressor
"""
# %%
rf.fit(normed_train_data, y_train)
y_pred = rf.predict(normed_test_data)
with open('final_rf_model', 'wb') as f:
    cPickle.dump(rf, f)
# %%
"""
### • Results
"""
# %%
print_results(rf, normed_test_data, y_test, y_pred)
display_graphs(y_pred, y_test, "Random-Forest-regression", "results_market_value")
# %%
"""
 > ##  Linear regression
"""
# %%
lr = LinearRegression()
# %%
"""
### • Fitting and training the Linear regressor
"""
# %%
lr.fit(normed_train_data, y_train)
y_pred = lr.predict(normed_test_data)
# %%
"""
### • Results
"""
# %%
print_results(lr, normed_test_data, y_test, y_pred)
display_graphs(y_pred, y_test, "Linear-regression", "results_market_value")
coefficients = pd.DataFrame(columns=['Feature', 'Coefficient'])

for x in range(0, len(normed_train_data.keys())):
    row = pd.DataFrame([[normed_train_data.keys()[x],
                         lr.coef_[x]]],
                       columns=['Feature', 'Coefficient'])
    coefficients = coefficients.append(row)
print('\n')
coefficients.set_index('Feature', inplace=True)
print(coefficients)
