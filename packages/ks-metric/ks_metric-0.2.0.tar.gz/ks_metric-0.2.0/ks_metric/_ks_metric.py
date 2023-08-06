import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

def ks_table(y_true, y_pred, n_bins=10):
    """
    Builds and returns KS Table

    Parameters
    ----------
    y_true : 1d array-like, or label indicator array / sparse matrix
        Ground truth (correct) target values.
    y_pred : 1d array-like, or label indicator array / sparse matrix
        Estimated targets as returned by a classifier.
    n_bins : int, default=10
        Number of bins for the ks_table


    Returns
    -------
    ks_table : DataFrame
        KS table
    """

    y_true = np.array(y_true)
    y_pred = np.array(y_pred)

    df = pd.DataFrame()
    df["score"] = y_pred
    # one hot encode y_true
    df["class_0"] = 1 - y_true
    df["class_1"] = y_true

    # bucket/bin prediction after ordering them
    df["bin"] = pd.qcut(df.score.rank(method="first"), n_bins, labels=list(range(0, n_bins, 1)))

    # group by bins
    grouped = df.groupby("bin", as_index=False)

    # KS Table
    ks_table = pd.DataFrame()
    ks_table["min_score"] = grouped.min().score
    ks_table["max_score"] = grouped.max().score
    ks_table["n_class_0"] = grouped.sum().class_0
    ks_table["n_class_1"] = grouped.sum().class_1
    ks_table["n_total"] = ks_table.n_class_0 + ks_table.n_class_1

    count_class_0 = df.class_0.sum()
    count_class_1 = df.class_1.sum()

    # class rate
    ks_table["%_class_0"] = (ks_table.n_class_0 / count_class_0) * 100
    ks_table["%_class_1"] = (ks_table.n_class_1 / count_class_1) * 100

    # class cumilative rate
    ks_table["cs_class_0"] = (ks_table.n_class_0 / count_class_0).cumsum() * 100
    ks_table["cs_class_1"] = (ks_table.n_class_1 / count_class_1).cumsum() * 100

    # difference between cumilative class rates
    ks_table["cs_diff"] = np.abs(ks_table["cs_class_0"] - ks_table["cs_class_1"])
    
    # set style
    ks_table.style.format(
        "{:.1f}%", subset=["%_class_0", "%_class_1", "cs_class_0", "cs_class_1", "cs_diff"]
    )

    # KS as max of cs_diff
    def flag(x):
        return "<--" if x == ks_table.sep.max() else ""
    ks_table["KS"] = ks_table.sep.apply(flag)

    # set ks_table style
    ks_table = ks_table.round({'cs_bads': 2, 'cs_goods': 2, 'sep': 2})

    return ks_table


def ks_score(
    y_true,
    y_pred,
    return_threshold=False,
):
    """
    returns KS value

    Parameters
    ----------
    y_true : 1d array-like, or label indicator array / sparse matrix
        Ground truth (correct) target values.
    y_pred : 1d array-like, or label indicator array / sparse matrix
        Estimated targets as returned by a classifier.
    return_threshold : bool, default=False
        If True, returns threshold value along with KS value.

    Returns
    -------

    ks : float
        KS value
    
    threshold : float
        Threshold value for KS

    """

    y_true = np.array(y_true)
    y_pred = np.array(y_pred)

    # check y_true.nunique == 2
    classes = np.unique(y_true)
    if len(classes) != 2:
        raise ValueError('Cannot calculate KS statistic for data with '
                         '{} category/ies'.format(len(classes)))

    # encode y_true
    lb = LabelEncoder()
    encoded_labels = lb.fit_transform(y_true)

    # create 2D array with y_true, y_pred
    ks_arr = np.dstack((encoded_labels, y_pred))[0]

    # order by y_pred
    ks_arr = ks_arr[np.argsort(ks_arr[:, 1], kind="stable")]

    # counts of y_true
    y_true_counts = np.unique(ks_arr[:, 0], return_counts=True)[1]

    # cumilative sum by total counts of 0s and 1s
    cs_0 = (1 - ks_arr[:, 0]).cumsum() / y_true_counts[0]
    cs_1 = (ks_arr[:, 0]).cumsum() / y_true_counts[1]

    # seperation between cumilative percent
    cs_diff = np.abs(cs_0 - cs_1)

    # ks : max seperation
    ks = cs_diff.max() * 100

    if return_threshold:
        return ks, ks_arr[cs_diff.argmax(), 1]
    else:
        return ks


