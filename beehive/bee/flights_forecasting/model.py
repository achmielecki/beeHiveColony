import pandas as pd
from prophet import Prophet

df_humidity = pd.read_csv('./data/humidity_schwartau.csv').set_index('timestamp')
df_temperature = pd.read_csv('./data/temperature_schwartau.csv').set_index('timestamp')
df_weight = pd.read_csv('./data/weight_schwartau.csv').set_index('timestamp')
# df_weight = df_weight[df_weight['timestamp'].str.contains(':00:00')].reset_index().set_index('timestamp')
# df_flow = pd.read_csv('./data/flow_schwartau.csv')
# df_flow = df_flow[df_flow['timestamp'].str.contains(':00:00')]
df_final = df_humidity.join(df_temperature, how='inner') \
    #.join(df_weight, how='inner') \
    # .join(df_flow, lsuffix='', rsuffix='_flow') \
    # .drop("timestamp_flow", axis=1)
print(df_humidity.head(5))
print(df_temperature.head(5))
print(df_final.head(5))
