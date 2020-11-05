# A-B test function.
def test_ab(dataframe, key1="A", key2="B", alpha=0.05, plot=True):
    """
    this function performs hypothesis checks and t-tests between two independent groups.
    dataframe: main dataframe of groups
    key1: parameter is first group name
    key2: parameter is second group name
    alpha: the alpha confidence score
    plot: showing boxplot with values
    """
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy import stats
    from scipy.stats import shapiro

    print("⁝" * 200)
    print(" " * 25, "▚ • AB Test Function Analysis Reports • ▚", " " * 16)
    print("-" * 100, "\n")
    print("Normality Assumption")
    print("➠", "Ho: The data follows a normal distribution.")
    print("➠", "H1: The data does not follow a normal distribution.")
    print("-" * 100, "\n")
    print("▚ Normality Assumption Report", "\n")
    # Normality Assumption
    norm_A = shapiro(dataframe[key1])[1]
    norm_B = shapiro(dataframe[key2])[1]
    if norm_A >= alpha:  # first group normality assumption is OK.
        print(key1, ": assumption of normality is provided ✓. | p-value: {} | Null hypothesis is not rejected.".format(
            "%.4f" % norm_A))
        if norm_B >= alpha:  # second group normality assumption is OK too.
            print(key2,
                  ": assumption of normality is provided ✓. | p-value: {} | Null hypothesis is not rejected.".format(
                      "%.4f" % norm_B))
            print("-" * 100)
            print("Assumption of normality is provided! ✓✓ Levene Test is loading...")
            print("-" * 100, "\n")
            print("Variance Homogenity Assumption")
            print("➠ Ho: There is no difference between the variance of the both groups.")
            print("➠ H1: There is a significant difference between the variance of the both groups.")
            print("-" * 100, "\n")
            var_as = stats.levene(dataframe[key1], dataframe[key2])[1]
            if var_as >= alpha:  # Variance Homogenity assumption is OK.
                print("▚ Variance Homogenity Assumption Report", "\n")
                print("There is no difference between the variance of the both groups ✓. | p-value {}".format(
                    "%.4f" % var_as))
                print("Assumption of variance homogenity is provided!✓✓ ")
                print("-" * 100, "\n")
                print("All assumptions are provided. Test Statistic is ready ✓✓✓".upper())
                print("-" * 100, "\n")
                test_stat, pvalue = stats.ttest_ind(dataframe[key1], dataframe[key2], equal_var=True)
                print('Test Statistic = %.4f, p-value = %.4f' % (test_stat, pvalue))
                if pvalue < alpha:
                    print("Ho: Rejected.", key1, "and", key2,
                          "There is a statistically significant difference between the means with ",
                          int(100 - 100 * alpha), "% confidence ✓.")
                    if dataframe[key1].mean() > dataframe[key2].mean():
                        print("Group A mean value is bigger than Group B")
                    else:
                        print("Group B mean value is bigger than Group A")

                else:
                    print("Ho: can not rejected.", key1, "and", key2,
                          "There is NOT  statistically significant difference between the means with ",
                          int(100 - 100 * alpha), "% confidence ✓.")
            else:
                print("There is a significant difference between the variance of the both groups. x")
                print("Variance Homogenity Assumption is failed, Welch T- Test is loading...")
                test_stat, pvalue = stats.ttest_ind(dataframe[key1], dataframe[key2], equal_var=False)
                print('According to the non-homogeneous variance results: Test Statistic = %.4f, p-value = %.4f' % (
                    test_stat, pvalue))
                if pvalue < alpha:
                    print("Ho: Rejected.", key1, "and", key2,
                          "There is a statistically significant difference between the means with ",
                          int(100 - 100 * alpha), "% confidence ✓.")
        else:  # second group normality assumption is not OK.
            print(key2, "Normality Assumption is failed. Non-parametric should be applied. p-value: {}".format(
                "%.4f" % norm_B))

    else:  # first group normality assumption is not OK.
        print(key1,
              "Normality Assumption is failed. Non-parametric should be applied. | p-value: {} | H0 rejected".format(
                  "%.4f" % norm_A))
    if plot:
        print("")
        vals, names, xs = [], [], []
        for i, col in enumerate(dataframe.columns):
            vals.append(dataframe[col].values)
            names.append(col)
            xs.append(np.random.normal(i + 1, 0.04, dataframe[col].values.shape[0]))  # adds jitter to the data points - can be adjusted
        plt.boxplot(vals, labels=names)
        palette = ['#25B89B', '#C20E69']
        for x, val, c in zip(xs, vals, palette):
            plt.scatter(x, val, alpha=0.7, color=c)
        plt.show()
