import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def read_csv(fn):
    data = pd.read_csv('data20200417.csv', skiprows=0, header=[0,2], skipinitialspace=True)
    # set datetime column as index
    dt_ind = data.columns.get_level_values(1).get_loc('Timestamp')
    dt_header = data.columns[dt_ind]
    datetime_column_raw = data[dt_header]
    datetime_column = pd.to_datetime(datetime_column_raw)
    data[dt_header] = datetime_column
    data.index = data[dt_header]
    data.index.name = 'datetime'
    data = data.drop(dt_header, axis=1)
    # rename columns
    ports = {'Port 1': 'teros_1',
             'Port 2': 'teros_2',
             'Port 3': '5t3_1',
             'Port 4': '5t3_2',
             'Port 5': '5te_3',
             'Port 6': '5t3_4',
             'Port 7': 'logger_battery',
             'Port 8': 'logger_weather',
             '°C Soil Temperature': 'temp_C',
             'kPa Matric Potential': 'w_pot_kPa',
             'm³/m³ Water Content': 'w_cnt_vol',
             'mS/cm Saturation Extract EC': 'conductivity_mS/cm',
             'mV Battery Voltage': 'batt_volt',
             '% Battery Percent': 'batt_pct',
             'kPa Reference Pressure': 'press_kPa',
             '°C Logger Temperature': 'temp_C'}
    data = data.rename(columns=ports)
    return(data)

def plot_datetime(df, ylabel, output):
    fig, ax = plt.subplots(1, 1, sharex=True, figsize=(10, 6.5))
    ys = df.columns
    for i, y in enumerate(ys):
        ax.plot_date(df.index, df[y], '-', linewidth=4, label=y)
    locator = matplotlib.dates.AutoDateLocator(minticks=5, maxticks=20)
    formatter = mdates.ConciseDateFormatter(locator)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)
    fig.autofmt_xdate()
    ax.legend()
    ax.grid()
    ax.set_ylabel(ylabel)
    plt.tight_layout()
    plt.savefig(output, dpi=600)
    plt.show()

if __name__ == '__main__':

    data = read_csv('data20200417.csv')
    data = data.loc['2020-03-15 00:00:00': '2020-04-15 00:00:00']
    data.to_csv('data_sensors.csv')
    plot_data = data.loc[:, (slice(None), 'temp_C')]
    plot_datetime(plot_data, ylabel='temp C', output='temp.png')
    plot_data = data.loc[:, (slice(None), 'w_pot_kPa')]
    plot_datetime(plot_data, ylabel='temp C', output='w_pot.png')
    plot_data = data.loc[:, (slice(None), 'w_cnt_vol')]
    plot_datetime(plot_data, ylabel='temp C', output='w_cnt.png')
