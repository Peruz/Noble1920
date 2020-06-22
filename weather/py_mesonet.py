import numpy as np
import pandas as pd
import os
import argparse
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.dates as mdates


def get_cmd():
    parse = argparse.ArgumentParser()
    files = parse.add_argument_group('files')
    output = parse.add_argument_group('output')
    files.add_argument('-in_dir', type=str, help='mesonet folder with the weather data', default='mesonet_data')
    output.add_argument('-out_dir', type=str, help='name of the output csv file')
    output.add_argument('-out_csv', type=str, help='name of the output directory')
    args = parse.parse_args()
    return(args)


def plot_temp(df, output_name):
    fig, ax = plt.subplots(1, 1, figsize=(12, 6.5))
    fig.autofmt_xdate()
    plt.plot(df.index, df['TA9M'], '-c', linewidth=2, ms=3, label='9.0 m', alpha=1)
    plt.plot(df.index, df['TAIR'], '-m', linewidth=2, ms=3, label='1.5 m', alpha=0.5)
    locator = matplotlib.dates.AutoDateLocator(minticks=25, maxticks=35)
    formatter = mdates.ConciseDateFormatter(locator)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)
    # ax.set_xlim([datetime.date(2019, 11, 15), datetime.date(2020, 5, 15)])
    ax.set_ylabel('temperature C')
    ax.legend(loc='upper left')
    plt.tight_layout()
    plt.savefig(output_name, dpi=600)
    plt.show()
    plt.close()


def plot_rain(df, output_name):
    fig, ax = plt.subplots(1, 1, figsize=(12, 6.5))
    plt.bar(df.index, df, width=0.8, edgecolor='k')
    locator = matplotlib.dates.AutoDateLocator(minticks=10, maxticks=25)
    formatter = mdates.ConciseDateFormatter(locator)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)
    fig.autofmt_xdate()
    # ax.set_xlim([datetime.date(2019, 11, 15), datetime.date(2020, 5, 15)])
    ax.set_ylabel('daily rain [mm]')
    plt.tight_layout()
    plt.savefig(output_name, dpi=600)
    plt.show()
    plt.close()


def plot_radiation(df, output_name):
    fig, ax = plt.subplots(1, 1, figsize=(12, 6.5))
    fig.autofmt_xdate()
    plt.plot(df.index, df, '-', linewidth=2, ms=3, color='darkorange')
    locator = matplotlib.dates.AutoDateLocator(minticks=25, maxticks=35)
    formatter = mdates.ConciseDateFormatter(locator)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)
    # ax.set_xlim([datetime.date(2019, 11, 15), datetime.date(2020, 5, 15)])
    ax.set_ylabel('solar radiation [W/m^2]')
    plt.tight_layout()
    plt.savefig(output_name, dpi=600)
    plt.show()
    plt.close()


def plot_humidity(df, output_name):
    fig, ax = plt.subplots(1, 1, figsize=(12, 6.5))
    fig.autofmt_xdate()
    plt.plot(df.index, df, '-', linewidth=2, ms=3, color='steelblue')
    locator = matplotlib.dates.AutoDateLocator(minticks=25, maxticks=35)
    formatter = mdates.ConciseDateFormatter(locator)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)
    # ax.set_xlim([datetime.date(2019, 11, 15), datetime.date(2020, 5, 15)])
    ax.set_ylabel('relative humidity at 1.5 m [%]')
    plt.tight_layout()
    plt.savefig(output_name, dpi=600)
    plt.show()
    plt.close()


def main():
    args = get_cmd()
    files = [f for f in os.listdir(args.in_dir) if f.endswith('t05')]
    dir_files = [os.path.join(args.in_dir, f) for f in files]
    reading_opts = {'skiprows': 3, 'delim_whitespace': True, 'skipinitialspace': True}
    df = pd.concat([pd.read_csv(f, **reading_opts) for f in dir_files], ignore_index=True)
    df.index = pd.to_datetime(df['YYYYMMDDhhmm'], format='%Y%m%d%H%M')
    df.index = df.index.rename('datetime')
    df = df.sort_index()
    df = df.drop('YYYYMMDDhhmm', axis=1)
    df = df.loc['2019-11-15': '2020-08-16']
    df = df.replace({-999: np.nan})
    # rain
    df_rain = df['RAIN']
    df_rain_daily = df_rain.resample('D').sum()
    plot_rain(df_rain_daily, 'rain.pdf')
    # temp
    df_temp = df[['TAIR', 'TA9M']]
    plot_temp(df_temp, 'temp.pdf')
    # solar radiation
    df_radiation = df['SRAD']
    plot_radiation(df_radiation, 'radiation.pdf')
    # humidity
    df_humidity = df['RELH']
    plot_humidity(df_humidity, 'humidity.pdf')
    # output
    df.to_csv('weather.csv')


if __name__ == '__main__':
    main()
