# import libraries
import pandas as pd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import shapiro, levene, ttest_ind

# set display options
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

# data loading
df_control = pd.read_excel("ab_testing_comparing_the_conversion_of_bidding_methods\\ab_testing.xlsx", sheet_name="Control Group")
df_test = pd.read_excel("ab_testing_comparing_the_conversion_of_bidding_methods\\ab_testing.xlsx", sheet_name="Test Group")

# check df
def check_df(dataframe, head=5):
    print("##################### Shape #####################")
    print(dataframe.shape)
    print("##################### Types #####################")
    print(dataframe.dtypes)
    print("##################### Head #####################")
    print(dataframe.head())
    print("##################### Tail #####################")
    print(dataframe.tail())
    print("##################### NA #####################")
    print(dataframe.isnull().sum())
    print("##################### Quantiles #####################")
    print(dataframe.quantile([0, 0.05, 0.50, 0.95, 0.99, 1]).T)

check_df(df_control)
check_df(df_test)


# concatenate dataframes
df_control["group"] = "control"
df_test["group"] = "test"

df = pd.concat([df_control,df_test], axis=0,ignore_index=False)
df.head()


# A/B Testing hypotheses

# Define the Hypotheses:

# H0: M1 = M2 (There is no difference between the control group and the test group purchase averages.)

# H1: M1 ≠ M2 (There is a difference between the control group and the test group purchase averages.)

# Hypothesis Testing:

df.groupby("group").agg({"Purchase": "mean"})

#Test if the Control and Test groups meet the normality assumption using the "Purchase" variable separately:

# Normality Assumption:
# H0: The assumption of normality is met.
# H1: The assumption of normality is not met.
# If p > 0.05, fail to reject H0.

# Based on the test results, does the normality assumption hold for the Control and Test groups? Interpret the obtained p-values.

test_stat, pvalue = shapiro(df.loc[df["group"] == "control", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# p-value = 0.5891
# H0 cannot be rejected. The values for the Control group satisfy the normality assumption.

# Test for Variance Homogeneity:

# Variance Homogeneity:
# H0: Variances are homogeneous.
# H1: Variances are not homogeneous.
# If p < 0.05, reject H0.
# If p > 0.05, fail to reject H0.

# Test if variance homogeneity is met for the Control and Test groups based on the "Purchase" variable. Interpret the obtained p-values.

test_stat, pvalue = levene(df.loc[df["group"] == "control", "Purchase"],
                           df.loc[df["group"] == "test", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# p-value = 0.1083
# H0 cannot be rejected. The values for the Control and Test groups satisfy the assumption of variance homogeneity.

# Choose the appropriate test based on the Normality and Variance Homogeneity results:

# Since the assumptions are satisfied, an independent two-sample t-test (parametric test) is performed.

# H0: M1 = M2 (There is no statistically significant difference between the Control and Test group purchase averages.)
# H1: M1 ≠ M2 (There is a statistically significant difference between the Control and Test group purchase averages.)
# If p < 0.05, reject H0.
# If p > 0.05, fail to reject H0.

test_stat, pvalue = ttest_ind(df.loc[df["group"] == "control", "Purchase"],
                              df.loc[df["group"] == "test", "Purchase"],
                              equal_var=True)

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))


# Interpret whether there is a statistically significant difference in purchase averages between the Control and Test groups based on the p-value:

# p-value = 0.3493
# H0 cannot be rejected. There is no statistically significant difference in purchase averages between the Control and Test groups.
