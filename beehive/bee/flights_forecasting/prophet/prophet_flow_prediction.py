import matplotlib.pyplot as plt
import pandas as pd
import time
from prophet import Prophet
from prophet.serialize import model_to_json, model_from_json


def save_prophet(m):
    with open('serialized_model.json', 'w') as fout:
        fout.write(model_to_json(m))


def train_prophet():
    start = time.time()
    df = (pd.read_csv('../data/flow_departures_schwartau.csv')
          .apply(lambda x: {'timestamp': x['timestamp'], 'flow': x['flow'] * -1}, axis=1, result_type='expand'))
    df.rename(columns={'timestamp': 'ds', 'flow': 'y'}, inplace=True)
    df['floor'] = 0
    print(df.head(5))
    m = Prophet()
    m.fit(df)
    save_prophet(m)
    end1 = time.time()
    print("training and saving time:")
    print(end1 - start)
    return m


def load_prophet():
    with open('serialized_model.json', 'r') as fin:
        return model_from_json(fin.read())


#m = train_prophet()
m = load_prophet()
print('loaded')
future = m.make_future_dataframe(freq='min', periods=129600, include_history=False)
future['floor'] = 0
print('future')
forecast = m.predict(future)
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()
print('forecast')
fig1 = m.plot(forecast)
fig1.show()
print('plot1')
components_fig = m.plot_components(forecast)
components_fig.show()
