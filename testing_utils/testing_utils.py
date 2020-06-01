import pandas as pd
from sklearn.base import clone
from sklearn import metrics
import numpy as np
from matplotlib import pyplot
from sklearn.metrics import r2_score


def drop_col_feat_imp(model, X_train, y_train, random_state=42):
    # clone the model to have the exact same specification as the one initially trained
    model_clone = clone(model)
    # set random_state for comparability
    model_clone.random_state = random_state
    # training and scoring the benchmark model
    model_clone.fit(X_train, y_train)
    benchmark_score = model_clone.score(X_train, y_train)
    # list for storing feature importances
    importances = []

    # iterating over all columns and storing feature importance (difference between benchmark and new model)
    for col in X_train.columns:
        model_clone = clone(model)
        model_clone.random_state = random_state
        model_clone.fit(X_train.drop(col, axis=1), y_train)
        drop_col_score = model_clone.score(X_train.drop(col, axis=1), y_train)
        importances.append(benchmark_score - drop_col_score)

    importances_df = imp_df(X_train.columns, importances)
    return importances_df


def imp_df(column_names, importances):
    df = pd.DataFrame({'feature': column_names, 'feature_importance': importances}) \
        .sort_values('feature_importance', ascending=False) \
        .reset_index(drop=True)
    return df


def norm(data, train_stats):
    return (data - train_stats['mean']) / train_stats['std']


def print_results(model, X_test, y_test, y_pred):
    print('\n')
    name = str(model)
    print("Model:", name[0:name.index("(")])
    print('\n')
    print('Results:')
    print('Test R^2 score:', model.score(X_test, y_test))
    print('Test Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))
    print('Test Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))
    print('Test Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))


def norm(data, train_stats):
    return (data - train_stats['mean']) / train_stats['std']


def display_graphs(prediction, actual, title, folder):
    fig, ax = pyplot.subplots()
    ax.scatter(prediction, actual)
    y_max = max(actual)
    y_min = min(actual)

    ax.plot([y_min, y_max], [y_min, y_max], 'k--', lw=4)
    ax.set_xlabel('Prediction')
    ax.set_ylabel('Actual')
    ax.set_title(title + " R2 plot")

    pyplot.text(y_max / 1.5, y_max / 3.5, 'R-squared = %0.2f' % r2_score(actual, prediction))

    pyplot.savefig(folder + "/" + title + "-R2-plot")
    pyplot.show()

    error = prediction - actual

    pyplot.hist(error, bins=200)
    pyplot.title(title + " Prediction error distribution")
    pyplot.xlim([-20, 20])
    pyplot.xlabel("Prediction Error")
    pyplot.ylabel("Count")

    y_max = pyplot.gca().get_ylim()[1]

    pyplot.text(11, y_max / 2.70, 'MAE = %0.2f' % metrics.mean_absolute_error(actual, prediction))
    pyplot.text(11, y_max / 3.10, 'MSE = %0.2f' % metrics.mean_squared_error(actual, prediction))
    pyplot.text(11, y_max / 3.60, 'RMSE = %0.2f' % np.sqrt(metrics.mean_squared_error(actual, prediction)))

    pyplot.savefig(folder + "/" + title + "-error-distribution")
    pyplot.show()
