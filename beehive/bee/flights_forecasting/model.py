import matplotlib.pyplot as plt
import pandas as pd
from prophet import Prophet


def plot(data):
    plt.plot(data.index, data['flow'])
    plt.xticks(data.index[0::110000], rotation=30)
    plt.subplots_adjust(bottom=0.3)
    plt.savefig()


departures_data = pd.read_csv('./departures_dataset.csv', index_col='timestamp')
plot(departures_data)
