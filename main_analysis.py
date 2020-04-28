import pandas as pd
import pyvista as pv
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import seaborn

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
    sensors = pd.read_csv('MeterSensors/data_sensors.csv',
                          header=[0,1],
                          index_col=0,
                          infer_datetime_format=True)
    rho = pd.read_csv('ERT/proc_inv_plot/analysis/csv_analysis.csv', infer_datetime_format=True)

    sensors.index = pd.to_datetime(sensors.index)
    sensors['datetime'] = sensors.index
    sensors['datetimems'] = pd.to_datetime(sensors.index, unit='ms')
    rho['datetime'] = pd.to_datetime(rho['datetime'])
    rho['datetimems'] = pd.to_datetime(rho['datetime'], unit='ms')
    plot_datetime(sensors, rho)
