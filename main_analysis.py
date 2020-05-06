import argparse
import os
import pandas as pd
import pyvista as pv
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import seaborn

def get_cmd():
    parse = argparse.ArgumentParser()
    files = parse.add_argument_group('files')
    output = parse.add_argument_group('output')
    files.add_argument('-ert_dir', type=str, help='path to ert_fname', default='ert/proc_inv_plot/analysis')
    files.add_argument('-ert_fname', type=str, help='name of the file with rho data from ert analysis', default='ert.csv')
    files.add_argument('-weather_dir', type=str, help='path to weather_fname', default='weather')
    files.add_argument('-weather_fname', type=str, help='name of the file with weather data', default='weather.csv')
    files.add_argument('-soil_dir', type=str, help='path to soil_fname', default='soil')
    files.add_argument('-soil_fname', type=str, help='name of the file with soil data', default='soil.csv')
    output.add_argument('-out_dir', type=str, help='name of the output csv file', default='.')
    output.add_argument('-out_fname', type=str, help='name of the output directory', default='all_noble1920.csv')
    args = parse.parse_args()
    return(args)

def plot_datetime(sensors, rho):
    """ plot rho, w_cont, w_pot, temp """
    fig, ax = plt.subplots(4, 1, sharex=True, figsize=(10, 6.5 + 4))

    # ravg
    seaborn.scatterplot(data=rho, x='datetimems', y='ravg', ax=ax[0], s=90, hue='reg_name', alpha=1, legend='full')
    ax[0].set_xlim([datetime.date(2019, 9, 15), datetime.date(2020, 5, 1)])

    # w_cnt 
    plot_sensors = sensors.loc[:, (slice(None), 'w_cnt_vol')]
    ys = plot_sensors.columns
    for i, y in enumerate(ys):
        ax[1].plot_date(plot_sensors.index, plot_sensors[y], '-', linewidth=4, label=y)
    ax[1].set_xlim([datetime.date(2019, 9, 15), datetime.date(2020, 5, 1)])
    ax[1].set_ylim(0.28, 0.52)
    ax[1].legend()

    # w_pot 
    plot_sensors = sensors.loc[:, (slice(None), 'w_pot_kPa')]
    ys = plot_sensors.columns
    for i, y in enumerate(ys):
        ax[2].plot_date(plot_sensors.index, plot_sensors[y], '-', linewidth=4, label=y)
    ax[2].set_xlim([datetime.date(2019, 9, 15), datetime.date(2020, 5, 1)])
    ax[2].legend()

    # temp_C
    plot_sensors = sensors.loc[:, (slice(None), 'temp_C')]
    plot_sensors = plot_sensors.drop('logger_weather', axis=1)
    ys = plot_sensors.columns
    for i, y in enumerate(ys):
        ax[3].plot_date(plot_sensors.index, plot_sensors[y], '-', linewidth=4, label=y)
    ax[3].set_xlim([datetime.date(2019, 9, 15), datetime.date(2020, 5, 1)])
    ax[3].set_ylim(10, 20)

    locator = matplotlib.dates.AutoDateLocator(minticks=5, maxticks=20)
    formatter = mdates.ConciseDateFormatter(locator)
    ax[3].xaxis.set_major_locator(locator)
    ax[3].xaxis.set_major_formatter(formatter)
    fig.autofmt_xdate()
    ax[3].set_xlim([datetime.date(2020, 3, 15), datetime.date(2020, 4, 15)])
    ax[3].legend()
    plt.tight_layout()
    plt.savefig('summary.png', dpi=600)
    plt.show()

if __name__ == '__main__':
    args = get_cmd()

    weather_dir_file = os.path.join(args.weather_dir, args.weather_fname)
    weather = pd.read_csv(weather_dir_file, header=0, index_col=0, parse_dates=[0], infer_datetime_format=True)
    weather.index = weather.index.round('H')
    weather_mi_tuples = [('weather', 'ARD2', l0) for l0 in weather.columns.get_level_values(0).tolist()]
    weather_mi = pd.MultiIndex.from_tuples(weather_mi_tuples)
    weather.columns = weather_mi

    ert_dir_file = os.path.join(args.ert_dir, args.ert_fname)
    ert = pd.read_csv(ert_dir_file, header=[0, 1], index_col=0, parse_dates=[0], infer_datetime_format=True)
    ert.index = ert.index.round('H')
    ert_mi_tuples = [('ert', l1, l2) for l1, l2 in zip(ert.columns.get_level_values(0).tolist(), ert.columns.get_level_values(1).tolist())]
    ert_mi = pd.MultiIndex.from_tuples(ert_mi_tuples)
    ert.columns = ert_mi

    soil_dir_file = os.path.join(args.soil_dir, args.soil_fname)
    soil = pd.read_csv(soil_dir_file, header=[0, 1], index_col=0, parse_dates=[0], infer_datetime_format=True)
    soil.index = soil.index.round('H')
    soil_mi_tuples = [('soil', l1, l2) for l1, l2 in zip(soil.columns.get_level_values(0).tolist(), soil.columns.get_level_values(1).tolist())]
    soil_mi = pd.MultiIndex.from_tuples(soil_mi_tuples)
    soil.columns = soil_mi

    df = pd.concat([weather, soil, ert], axis=1)
    out_dir_file = os.path.join(args.out_dir, args.out_fname)
    df = df.infer_objects()
    df.round(3)
    df.to_csv(out_dir_file, float_format='%g')
    #sensors.index = pd.to_datetime(sensors.index)
    #sensors['datetime'] = sensors.index
    #sensors['datetimems'] = pd.to_datetime(sensors.index, unit='ms')
    #rho['datetime'] = pd.to_datetime(rho['datetime'])
    #rho['datetimems'] = pd.to_datetime(rho['datetime'], unit='ms')
    #plot_datetime(sensors, rho)
