# gbm_autosplit

GBM scikit-learn interfaces which performs "early stopping" with single data set during `fit`.

"Early stopping" is great practice to tune the number of estimators for gradient boosting models. 
However it is not difficult to use it in tuning module in scikit-learn such as RandomizedSearchCV / GridSearchCV
because to use early stopping module requires two data sets but scikit learn does not have such interface.

To solve this situation, this interface performs following steps with in `fit`.
1. Split original input data into two randomly
2. Estimate `n_estimators` by using split data set with early stopping
3. Perform `fit` by using entire data set with estimated `n_estimators`


## Install

```
pip install gbm_autosplit
```

## Usage

```
import gbm_autosplit

estimator = gbm_autosplit.LGBMClassifier()
estimator.fit(x, y)
```