from sys import exit
import re
import io
import seaborn
import numpy as np
import requests
import pandas as pd
from dateutil import parser, rrule
from datetime import datetime, time, date, timedelta
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def scrape_weather(date_start, stations):
    date_start = parser.parse(date_start)
    date_end = date.today() + timedelta(days=1)
    dates = list(rrule.rrule(rrule.DAILY, dtstart=date_start, until=date_end))
    url = "http://www.wunderground.com/weatherstation/WXDailyHistory.asp?ID={station}&day={day}&month={month}&year={year}&graphspan=day&format=1"
    all_stations = []
    for s in stations:
        all_days = []
        for d in dates:
            print(s, d)
            date_url = url.format(station=s, day=d.day, month=d.month, year=d.year)
            response = requests.get(date_url, headers={'User-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
            response.raise_for_status()
            data = response.text
            data = data.replace('<br>', '')
            df_day = pd.read_csv(io.StringIO(data), index_col=False)
            all_days.append(df_day)
        df_station = pd.concat(all_days, axis=0, ignore_index=True, sort=False)
        df_station['Time'] = pd.to_datetime(df_station['Time'])
        df_station = df_station.set_index('Time')
        df_station = df_station.resample('5min').mean()
        df_station['TemperatureC'] = (df_station['TemperatureF'] - 32) * 5/9
        all_stations.append(df_station)
    df = pd.concat(all_stations, axis=1, join='outer', sort=False, keys=stations)
    df.to_csv('weather.csv', float_format='%8.4f')

def get_weather(fname):
    weather = pd.read_csv('../weather.csv', index_col=0, parse_dates=True, header=[0, 1])
    weather = weather.rename_axis(index='Time')
    weather = weather.loc[datetime_start : datetime_end]
    weather = weather.resample('5min').mean()
    weather['Time'] = weather.index
    weather.loc[:, (slice(None), 'HourlyPrecipIn')] = weather.loc[:, (slice(None), 'HourlyPrecipIn')] * 2.54
    weather = weather.rename(columns={'HourlyPrecipIn' : 'HourlyPrecip_cm'})
    weather = temperature_cleaning(weather, (slice(None), 'TemperatureC'))
    return(weather)

def plot_datetime(df, ys, output_name, ylabels=['temp C', 'load kg']):
    nc = len(ys)
    fig, ax = plt.subplots(nc, 1, sharex=True, figsize=(10, 6.5 + nc))
    if nc == 1:
        ax = [ax]
    for i, y in enumerate(ys):
        ax[i].plot_date(df.index, df.loc[:, y],'-', color='green', linewidth=4, label=y)
        locator = matplotlib.dates.AutoDateLocator(minticks=5, maxticks=20)
        formatter = mdates.ConciseDateFormatter(locator)
        ax[i].xaxis.set_major_locator(locator)
        ax[i].xaxis.set_major_formatter(formatter)
        fig.autofmt_xdate()
        ax[i].legend()
        #ax[i].set_ylim(5, 30)
        if ylabels is not None:
            ax[i].set_ylabel(ylabels[i])
        ax[i].grid()
    plt.tight_layout()
    plt.savefig(output_name, dpi=600)
    plt.show()

def plot_xy_seaborn(df, x, ys, output_name):
    nr = len(ys)
    fig, ax = plt.subplots(nr, sharex=True, figsize=(10, 6.5 + nr))
    if nr == 1:
        ax = [ax]
    x = x[0]
    for i, y in enumerate(ys):
        x = df[x]
        y = df[y]
        print(type(x))
        print(type(y))
        ax[i].plot(x, y, color='black', linewidth=3)
        seaborn.scatterplot(x, y, ax=ax[i], s=90, hue=df.index, alpha=1, legend=False)
        ax[i].set_xlabel('temp C')
        ax[i].set_ylabel('load kg')
        ax[i].legend()
    plt.tight_layout()
    plt.savefig(output_name, dpi=600)
    plt.show()

def plot_xy(df, x, ys, output_name):
    nr = len(ys)
    fig, ax = plt.subplots(nr, sharex=True, figsize=(10, 6.5 + nr))
    if nr == 1:
        ax = [ax]
    for i, y in enumerate(ys):
        ax[i].plot(df.loc[:, x], df.loc[:, y], '-', color='green', linewidth=4, label=y)
        ax[i].set_xlabel('temp C')
        ax[i].set_ylabel('load kg')
        ax[i].legend()
    plt.tight_layout()
    plt.savefig(output_name, dpi=600)
    plt.show()

def temperature_cleaning(df, c, temperature_min=0, temperature_max=30):
    df_temp = df.loc[:, c]
    outliers = ((df_temp < temperature_min) | (df_temp > temperature_max))
    df[outliers] = np.NaN
    return(df)

def include_thermocouples_function(fname):
    df = pd.read_csv(fname, skiprows=16, encoding='UTF-16 LE')
    df['Time'] = pd.to_datetime(df['Time'], format='%m/%d/%Y %H:%M:%S:%f')
    df = df.set_index('Time')
    df = df.resample('5min').mean()
    df['Time'] = df.index
    temp_columns = [c for c in df.columns if '(C)' in c]
    num_temp_columns = [re.split('\s+', c)[0] for c in temp_columns]
    rename_columns = {old:new for (old, new) in zip(temp_columns, num_temp_columns)}
    df = df.rename(columns=rename_columns)
    use_columns = num_temp_columns +['Time']
    df = df[use_columns]
    df.columns = pd.MultiIndex.from_product([['thermo'], df.columns])
    return(df)

if __name__ == '__main__':

    include_scrape_weather = True
    include_weather = True

    if include_scrape_weather:
        scrape_weather(date_start='2020-02-15', stations=['KCABERKE108', 'KOKARDMO4'])

    weather = get_weather('../weather.csv')

    #df.to_csv('df.csv')

    weather = weather.loc['2020-02-28 12:00:00' : '2020-03-03 11:00:00']
    print(df.columns)
    ys = df.columns.tolist()
    raise SystemExit
    #ys.remove('Time')
    #ys = pd.MultiIndex.from_product([['load'], load_columns])
    d = {'F180623305':'107', 'F180623306':'107', 'F180623304':'103','F180623303':'104', 'F193827839':'105', 'F193827840':'106', 'Total':'102'}
    for k, v in d.items():
        y = pd.MultiIndex.from_tuples([('load', k)])
        x = pd.MultiIndex.from_tuples([('thermo', v)])
        name = 'l' + k[-2:] + '_t' + v[-2:] + '.png'
        print(name)
        plot_xy_seaborn(df, x, y, name)
        name = 'l' + k[-2:] + '_t' + v[-2:] + '_time.png'
        plot_datetime(df, [x, y], name)
