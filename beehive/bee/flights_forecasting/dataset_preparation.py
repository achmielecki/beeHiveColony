import pandas as pd


def create_dataset():
    df_humidity = pd.read_csv('./data/humidity_schwartau.csv').set_index('timestamp')
    df_temperature = pd.read_csv('./data/temperature_schwartau.csv').set_index('timestamp')
    df_weight = pd.read_csv('./data/weight_schwartau.csv').set_index('timestamp')
    df_flow_arrivals = pd.read_csv('./data/flow_arrivals_schwartau.csv').set_index('timestamp')
    df_flow_departures = pd.read_csv('./data/flow_departures_schwartau.csv').set_index('timestamp')
    df_flow_departures \
        .join(df_weight) \
        .join(df_humidity) \
        .join(df_temperature) \
        .ffill() \
        .bfill() \
        .to_csv('departures_dataset.csv')
    df_flow_arrivals \
        .join(df_weight) \
        .join(df_humidity) \
        .join(df_temperature) \
        .ffill() \
        .bfill() \
        .to_csv('arrivals_dataset.csv')


create_dataset()
