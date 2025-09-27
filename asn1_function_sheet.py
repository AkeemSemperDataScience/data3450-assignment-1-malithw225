
import pandas as pd
import numpy as np
import math

def age_splitter(df, col_name, age_threshold):
    df_below = df[df[col_name] < age_threshold]
    df_above_equal = df[df[col_name] >= age_threshold]
    return df_below, df_above_equal
    
def effectSizer(df, num_col, cat_col):
    classes = df[cat_col].unique()
    if len(classes) != 2:
        raise ValueError("The categorical column must have exactly two unique values.")

    group1 = df[df[cat_col] == classes[0]][num_col]
    group2 = df[df[cat_col] == classes[1]][num_col]

    mean1, mean2 = group1.mean(), group2.mean()
    std1, std2 = group1.std(), group2.std()
    n1, n2 = len(group1), len(group2)

    pooled_std = np.sqrt(((n1 - 1)*std1**2 + (n2 - 1)*std2**2) / (n1 + n2 - 2))

    effect_sizes = {
        classes[0]: (mean1 - mean2) / pooled_std,
        classes[1]: (mean2 - mean1) / pooled_std
    }

    return effect_sizes

def cohortCompare(df, cohorts, statistics=['mean', 'median', 'std', 'min', 'max']):
    cohorts_stats = None
    value_counts = None
    if pd.api.types.is_numeric_dtype(df[cohorts]):
        cohorts_stats = CohortMetric(cohorts)
        cohorts_stats.setMean(df[cohorts].mean())
        cohorts_stats.setMedian(df[cohorts].median())
        cohorts_stats.setStd(df[cohorts].std())
        cohorts_stats.setMin(df[cohorts].min())
        cohorts_stats.setMax(df[cohorts].max())
        print(cohorts_stats)
    elif pd.api.types.is_categorical_dtype(df[cohorts]) or pd.api.types.is_object_dtype(df[cohorts]):
        value_counts = df[cohorts].value_counts()
        print(value_counts)
    return cohorts_stats, value_counts

class CohortMetric():  # don't change this
    def __init__(self, cohort_name):
        self.cohort_name = cohort_name
        self.statistics = {
            "mean": None,
            "median": None,
            "std": None,
            "min": None,
            "max": None
        }

    def setMean(self, new_mean):
        self.statistics["mean"] = new_mean

    def setMedian(self, new_median):
        self.statistics["median"] = new_median

    def setStd(self, new_std):
        self.statistics["std"] = new_std

    def setMin(self, new_min):
        self.statistics["min"] = new_min

    def setMax(self, new_max):
        self.statistics["max"] = new_max

    def compare_to(self, other):
        for stat in self.statistics:
            if not self.statistics[stat].equals(other.statistics[stat]):
                return False
        return True

    def __str__(self):
        output_string = f"\nCohort:\n {self.cohort_name}\n"
        for stat, value in self.statistics.items():
            output_string += f"\t{stat}:\n{value}\n"
        output_string += "\n"
        return output_string



def cohortCompare(df, cohorts, statistics=['mean', 'median', 'std', 'min', 'max']):
    # Split into numeric vs. categorical
    data = df[cohorts]
    numeric_cols = data.select_dtypes(include='number')
    cat_cols    = data.select_dtypes(exclude='number')

    # Create the CohortMetric object
    cohorts_stats = CohortMetric(cohorts)

    # ----- Numeric statistics -----
    if not numeric_cols.empty:
        if 'mean' in statistics:
            cohorts_stats.setMean(numeric_cols.mean())
        if 'median' in statistics:
            cohorts_stats.setMedian(numeric_cols.median())
        if 'std' in statistics:
            cohorts_stats.setStd(numeric_cols.std())
        if 'min' in statistics:
            cohorts_stats.setMin(numeric_cols.min())
        if 'max' in statistics:
            cohorts_stats.setMax(numeric_cols.max())

    # ----- Categorical statistics -----
    # We'll store value counts and mode in the CohortMetric.statistics dict
    if not cat_cols.empty:
        cat_summary = {}
        for col in cat_cols:
            cat_summary[col] = {
                "counts": cat_cols[col].value_counts(),
                "mode":   cat_cols[col].mode().iloc[0] if not cat_cols[col].mode().empty else None
            }
        cohorts_stats.statistics["categorical"] = cat_summary

    return cohorts_stats
    
   

class CohortMetric():
    # don't change this
    def __init__(self, cohort_name):
        self.cohort_name = cohort_name
        self.statistics = {
            "mean": None,
            "median": None,
            "std": None,
            "min": None,
            "max": None
        }
    def setMean(self, new_mean):
        self.statistics["mean"] = new_mean
    def setMedian(self, new_median):
        self.statistics["median"] = new_median
    def setStd(self, new_std):
        self.statistics["std"] = new_std
    def setMin(self, new_min):
        self.statistics["min"] = new_min
    def setMax(self, new_max):
        self.statistics["max"] = new_max

    def compare_to(self, other):
        for stat in self.statistics:
            if not self.statistics[stat].equals(other.statistics[stat]):
                return False
        return True
    def __str__(self):
        output_string = f"\nCohort:\n {self.cohort_name}\n"
        for stat, value in self.statistics.items():
            output_string += f"\t{stat}:\n{value}\n"
            output_string += "\n"
        return output_string
