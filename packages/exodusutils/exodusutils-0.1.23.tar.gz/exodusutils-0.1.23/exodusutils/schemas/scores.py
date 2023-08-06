import logging
import math
from typing import Callable, DefaultDict, Dict, List, Union

import numpy as np
import numpy.typing as npt
from pydantic import BaseModel, validator
from pydantic.types import NonNegativeFloat
from sklearn import preprocessing
from sklearn.metrics import accuracy_score, auc, log_loss, mean_squared_error, roc_curve

from exodusutils.internal import sanitize_pred_and_actual


class RegressionScores(BaseModel):
    """
    The regression scores set.

    Metrics include:
        - mean squared error (`mse`)
        - root mean square error (`rmse`)
        - root mean square logarithmic error (`rmsle`)
        - mean absolute error (`mae`)
        - r squared (`r2`)
        - deviance (`deviance`)
        - mean absolute percentage error (`mape`)
        - weighted mean absolute percentage error (`wmape`)
    """

    mse: float
    rmse: float
    rmsle: float
    mae: float
    r2: float
    deviance: float
    mape: float
    wmape: float

    @validator("mse", "rmse", "rmsle", "mae", "mape", "wmape")
    def check_nonnegative_or_nan(cls, v):
        if not math.isnan(v) and v < 0:
            raise ValueError(
                f"Invalid score: required nan or non-negative float, got {v}"
            )
        return v

    @classmethod
    def get_scores(cls, pred: npt.NDArray[np.float64], actual: npt.NDArray[np.float64]):
        """
        Calculate the regrssion scores according to a set of predicted values (`pred`) and actual values (`actual`).

        Parameters
        ----------
        pred : np.ndarray
            Prediction results based on test set feature columns
        actual : np.ndarray
            The test set target values from the original dataframe

        Returns
        -------
        `RegressionScores`
        """
        pred, actual = sanitize_pred_and_actual(pred, actual)

        variance = np.var(actual)

        def calc_rmsle(y: np.ndarray, yhat: np.ndarray) -> float:
            try:
                log_diffs = list()
                for i in range(len(yhat)):
                    cur_pred = math.log(y[i] + 1)
                    cur_act = math.log(yhat[i] + 1)
                    log_diffs.append(pow(cur_act - cur_pred, 2))
                msle = sum(log_diffs) / len(log_diffs)
                res = math.sqrt(msle)
            except Exception as e:
                logging.error("Unable to calculate rmsle: " + str(e))
                res = np.NaN
            return res

        def calc_r2(yhat: np.ndarray, y: np.ndarray) -> float:
            diffs = np.abs(np.subtract(yhat, y))
            diffs_not_nan = diffs[~np.isnan(diffs)]

            square_diffs = [np.square(x) for x in diffs_not_nan]
            mse = sum(square_diffs) / len(square_diffs)

            return 1 - mse / variance

        def calc_metric_score(f: Callable[[np.ndarray, np.ndarray], float]):
            if actual.shape != pred.shape:
                raise RuntimeError(
                    f"actual shape ({actual.shape}) != predicted shape ({pred.shape})"
                )
            shape = actual.shape
            if len(shape) == 1:  # single target
                res = f(pred, actual)
            elif len(shape) == 2:  # multiple targets
                ls = list()
                for i in range(shape[0]):
                    ls.append(f(pred[i], actual[i]))
                res = sum(ls) / len(ls)
            else:  # can't happen
                raise RuntimeError(f"invalid shape: {shape}")
            return res

        mse = np.round(mean_squared_error(pred, actual), 5)
        rmse = np.round(np.sqrt(mse), 5)
        absolute_difference = np.abs(np.subtract(actual, pred))
        mae = np.round(np.mean(absolute_difference), 5)
        mape = (
            float("nan")
            if 0 in actual
            else np.round(100 * np.mean(absolute_difference / actual), 5)
        )
        wmape = (
            float("nan")
            if np.sum(actual) == 0.0
            else np.round(100 * np.sum(absolute_difference) / np.sum(actual), 5)
        )
        r2 = np.round(calc_metric_score(calc_r2), 5)
        deviance = mse
        rmsle = np.round(calc_metric_score(calc_rmsle), 5)
        return cls(
            mse=mse,
            rmse=rmse,
            rmsle=rmsle,
            mae=mae,
            mape=mape,
            wmape=wmape,
            r2=r2,
            deviance=deviance,
        )


class ClassificationScores(BaseModel):
    """
    If there are more than 2 classes, it is a MultinomialScores. Otherwise it is a BinomialScores.

    For BinomialScores, the metrics include:
        - logloss (`logloss`)
        - mean per class error (`mean_per_class_error`)
        - misclassification (`misclassification`)
        - area under curve (`auc`)
        - lift top group (`lift_top_group`)

    For MultinomialScores, the metrics include:
        - logloss (`logloss`)
        - mean per class error (`mean_per_class_error`)
        - misclassification (`misclassification`)

    """

    logloss: float
    mean_per_class_error: NonNegativeFloat
    misclassification: NonNegativeFloat

    @staticmethod
    def get_scores(
        pred: np.ndarray, pred_proba: np.ndarray, actual: np.ndarray, labels: np.ndarray
    ):
        """
        Calculate the classification scores according to a set of predicted values (`pred`) and actual values (`actual`).
        If `labels.size > 2`, a `MultinomialScores` will be returned. Otherwise it will return `BinomialScores`.

        Parameters
        ----------
        pred : np.ndarray
            Prediction results based on test set feature columns
        pred_proba : np.ndarray
            Nested list of probability scores.

            Each sub-list represents the probability of each class being the
            proper prediction for a particular record. Used for the log loss metric
            e.g., `[[ 0.1, 0.8, 0.1] [ 0.0, 0.79 , 0.21] .... ]`,
            meaning that, for record X[0] in the test set, the proper prediction
            being class_0 is 10%, class_1 is 80%, and class_2 is 10%.
        actual : np.ndarray
            The test set target values from the original dataframe
        labels : np.ndarray
            The labels that appear in target column.

        Returns
        -------
        An instance of either `MultinomialScores` or `BinomialScores`.
        """

        pred, actual = sanitize_pred_and_actual(pred, actual)

        if labels.size < 2:
            raise ValueError(f"Invalid labels, has to be more than 1, got {labels}")

        def mean_per_class_error(pred: List[float], actual: List[float]):
            from collections import Counter, defaultdict

            element_count = dict(Counter(actual))
            misclassification_count: DefaultDict = defaultdict(int)
            for y, yhat in zip(pred, actual):
                if y != yhat:
                    misclassification_count[yhat] += 1
            return sum(
                [
                    misclassification_count[i] / float(element_count[i])
                    for i in element_count
                ]
            ) / len(element_count)

        def lift_top_group(pred: List[float], actual: List[int]) -> float:
            def mean(arr):
                return sum(arr) / float(len(arr))

            top_group = sorted(zip(pred, actual), key=lambda x: x[0])
            one_percent_len = int(math.ceil(len(top_group) / 100.0))
            return mean([x[1] for x in top_group[:one_percent_len]]) / float(
                mean(actual)
            )

        le = preprocessing.LabelEncoder()
        labels = le.fit_transform(labels)
        actual = le.transform(actual)
        pred = le.transform(pred)
        log_loss_ = log_loss(actual, pred_proba, labels=labels)
        pred_scores = [pred_proba[i[0]][x] for i, x in np.ndenumerate(pred)]
        misclassification = 1 - accuracy_score(actual, pred)
        mpce = mean_per_class_error(list(pred), list(actual))
        if len(labels) > 2:  # n-ary classification problem
            return MultinomialScores(
                logloss=log_loss_,
                mean_per_class_error=mpce,
                misclassification=misclassification,
            )
        else:
            fpr, tpr, _ = roc_curve(actual, pred_scores, pos_label=None)
            auc_ = auc(fpr, tpr)
            lift = lift_top_group(pred_scores, list(actual))
            return BinomialScores(
                logloss=log_loss_,
                mean_per_class_error=mpce,
                misclassification=misclassification,
                auc=auc_,
                lift_top_group=lift,
            )


class BinomialScores(ClassificationScores):
    """
    The binomial scores set.

    Metrics include:
        - logloss (`logloss`)
        - misclassification (`misclassification`)
        - mean per class error (`mean_per_class_error`)
        - area under curve (`auc`)
        - lift top group (`lift_top_group`)
    """

    auc: float
    lift_top_group: float

    @validator("auc")
    def check_auc(cls, v):
        if v != np.nan and v < 0:
            raise ValueError(f"{v} should be greater than or equal to 0")
        return v


class MultinomialScores(ClassificationScores):
    """
    The multinomial scores set.

    Metrics include:
        - logloss (`logloss`)
        - misclassification (`misclassification`)
        - mean per class error (`mean_per_class_error`)
    """


Scores = Union[RegressionScores, BinomialScores, MultinomialScores]


class CVScores(BaseModel):
    """
    The CV scores struct.

    Usage
    -----
    ```python
    split_scores: List[Scores] = []
    for _ in nfolds:
        # dates, actual = extract_from_data(df)
        # pred = model.predict(dates)
        split_scores.append(RegressionScores.get_scores(pred, actual))
    # To get the CV scores that can be sent from FastAPI, do this
    CVScores(split_scores=split_scores).to_report()
    ```
    """

    split_scores: List[Scores]

    @validator("split_scores")
    def check_folds(cls, v):
        if not v:
            raise ValueError("No score")
        types = {type(f).__name__ for f in v}
        if len(types) > 1:
            raise ValueError(
                f"All split scores must have consistent type. Found {types}"
            )
        return v

    def to_report(self) -> Dict[str, List[float]]:
        """
        Turns this CV scores object into a `dict` from `str` (the metric names) to a list of `floats` (the actual scores).

        """
        return {
            field: [score.dict()[field] for score in self.split_scores]
            for field in self.split_scores[0].__fields__
        }
