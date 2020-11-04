import pandas as pd
import matplotlib.pyplot as plt

from adtk.data import validate_series
from adtk.detector import ThresholdAD
from adtk.detector import QuantileAD, SeasonalAD, AutoregressionAD


from adtk.visualization import plot


path_file = r'Put_Here_you_Path_to_file\excel.xslx'
df_data = pd.ExcelFile(path_file).parse(sheet_name='QL_1', index_col='Date')
stations = df_data.columns

for sta in stations:
    x = df_data[sta]
    df_anomalies = pd.DataFrame(data=None, index=x.index)

    s_train = validate_series(x)

    threshold_ad = ThresholdAD(high=35, low=10)
    anomalies = threshold_ad.detect(s_train)
    df_anomalies['threshold_ad'] = anomalies
    plot(s_train, anomalies)
    # plt.show()

    quantile_ad = QuantileAD(high=0.99, low=0.01)
    anomalies = quantile_ad.fit_detect(s_train)
    df_anomalies['quantile_ad'] = anomalies
    plot(s_train, anomalies, ts_linewidth=1, ts_markersize=3, anomaly_markersize=5, anomaly_color='red', anomaly_tag="marker")
    # plt.show()

    seasonal_ad = SeasonalAD(freq=12)
    anomalies = seasonal_ad.fit_detect(s_train)
    df_anomalies['seasonal_ad'] = anomalies
    plot(s_train, anomalies, ts_linewidth=1, ts_markersize=3, anomaly_markersize=5, anomaly_color='red', anomaly_tag="marker")
    # plt.show()

    autoreg_ad = AutoregressionAD()
    anomalies = autoreg_ad.fit_detect(s_train)
    df_anomalies['autoreg_ad'] = anomalies
    plot(s_train, anomalies, ts_linewidth=1, ts_markersize=3, anomaly_markersize=5, anomaly_color='red', anomaly_tag="marker")
    # plt.show()






