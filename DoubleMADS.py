import pandas as pd
import matplotlib.pyplot as plt


def points_plot(points, m):
    fig, ax = plt.subplots(figsize=(8, 1.5))
    ax.scatter(x=points, y=[1]*len(points), c='lightgrey', s=100, alpha=0.7)
    ax.scatter(x=m, y=1, c='red', s=50, marker='s', alpha=.55)
    ax.scatter(x=points.mean(), y=1, c='blue', s=50, marker='s', alpha=.55)

    ax.set(yticklabels=[])  # remove the tick labels
    ax.set_xlabel('flow [$m^3/s$]')
    ax.tick_params(left=False)  # remove the ticks
    ax.text(m, 1.02, 'median', verticalalignment='center', horizontalalignment='center')
    ax.text(points.mean(), 0.98, 'mean', verticalalignment='center', horizontalalignment='left')
    fig.tight_layout()
    plt.show()


def mads_plot(points, m):
    fig, ax = plt.subplots(figsize=(8, 1.5))
    ax.scatter(x=points, y=[1]*len(points), c='lightgrey', s=100, alpha=0.7)
    ax.scatter(x=m, y=1, c='red', s=50, marker='s', alpha=.55)

    ax.set(yticklabels=[])  # remove the tick labels
    ax.set_xlabel('Anomalies in terms of MAD')
    ax.tick_params(left=False)  # remove the ticks
    ax.text(m, 1.02, 'Cutoff', verticalalignment='center', horizontalalignment='center')

    fig.tight_layout()
    plt.show()


def series_plot(x, z):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_title(x.name)
    ax.plot(x.index, x.values)
    ax.scatter(x=z.index, y=z.values, c='red', s=50, marker='s', alpha=.5)

    ax.set_ylabel('streamflow [$m^3/s$]')

    fig.tight_layout()
    plt.show()


def single_mads(x, k):

    # 1 Step: Calculating the Median of the data
    m = pd.Series.median(x)

    # points_plot(x, m)  # What does that look like?

    # 2 Step: Calculating the data absolute anomalies with respect to the median
    abs_dev = (x - m).abs()

    # 3 step: Now for the median of those absolute deviations
    # 1.4826, is a constant linked to the assumption of normality of the data, disregarding the abnormality induced by outliers
    # (Rousseeuw & Croux, 1993)

    mad = abs_dev.median() * 1.4826

    # 4 step: Now let's get the absolute deviation from the median of each point in the vector x,
    # and let's put those deviations in terms of the MAD
    d = abs_dev / mad

    mads_plot(d, k)  # What does that look like?

    # 5 step: Filtering the suspects
    shifty = x[d >= k]

    series_plot(x, shifty)  # What does that look like?


def double_mad(x):
    # 1 Step: Calculating the Median of the data
    m = pd.Series.median(x)

    # points_plot(x, m)  # What does that look like?

    # 2 Step: Calculating the data absolute anomalies with respect to the median
    abs_dev = (x - m).abs()

    # 3 step: Now for the median of those absolute deviations (left and right)
    left_mad = abs_dev[x <= m].median()
    right_mad = abs_dev[x > m].median()

    return left_mad, right_mad


def double_mads_from_median(x, k):
    # 1 step: absolute deviations for both, left and right.
    two_sided_mad = double_mad(x)

    # 2 Step: Calculating the Median of the data (again)
    m = pd.Series.median(x)

    x_mad = pd.Series(data=None, index=x.index, name=x.name)  # only another vector for storing the mads

    # 3 step: Now we just store both mads values in a single vector (pd.Series)
    # Here we do not need the assumption of normality (multiply by 1.4826)
    x_mad[x <= m] = two_sided_mad[0]
    x_mad[x > m] = two_sided_mad[1]

    # 4 step: Now let's get the absolute deviation from the median of each point in the vector x,
    # and let's put those deviations in terms of the MAD
    mad_distance = (x - m).abs() / x_mad

    mad_distance[x == m] = 0  # When data is equal to the median, then obviously the deviation is zero.

    # 5 step: Filtering the suspects
    shifty = x[mad_distance >= k]

    series_plot(x, shifty)  # What does that look like?


path_file = r'G:\Dropbox\18_EDOC_PUJ\Webinar\SESSION_03_OUTLIERS.xlsx'
df_data = pd.ExcelFile(io=path_file).parse(sheet_name='QL_1', index_col='Date')
stations = df_data.columns

for sta in stations:
    # single_mads(x=df_data[sta], k=3.0)
    double_mads_from_median(x=df_data[sta], k=3.0)
