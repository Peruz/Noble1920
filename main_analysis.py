import argparse
import os
import pandas as pd
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
    files.add_argument('-ert_fname', type=str, help='file with rho data from ert analysis', default='ert.csv')
    files.add_argument('-weather_dir', type=str, help='path to weather_fname', default='weather')
    files.add_argument('-weather_fname', type=str, help='name of the file with weather data', default='weather.csv')
    files.add_argument('-soil_dir', type=str, help='path to soil_fname', default='soil')
    files.add_argument('-soil_fname', type=str, help='name of the file with soil data', default='soil.csv')
    output.add_argument('-out_dir', type=str, help='name of the output csv file', default='.')
    output.add_argument('-out_fname', type=str, help='name of the output directory', default='all_noble1920.csv')
    args = parse.parse_args()
    return(args)


def rho_temp_correction(rho_vec, temp_vec, temp_reference=20, temp_slope_compensation=0.025):
    """
    temperature compensation of the soil resistivity with ratio model
    based on:
    Comparing temperature correction models for soil electrical conductivity measurement
    eq. 2, pag. 56
    """
    rho_temp_reference = rho_vec + (temp_slope_compensation * (temp_vec - temp_reference) * rho_vec)
    return(rho_temp_reference)


def plot_datetime(df):
    year_start = 2020
    month_start = 3
    day_start = 15
    year_end = 2020
    month_end = 6
    day_end = 1
    fig, ax = plt.subplots(
        5,
        1,
        sharex=True,
        figsize=(10, 6.5 + 5),
        gridspec_kw={'height_ratios': [1, 1, 1, 1, 1], 'top': 0.98, 'bottom': 0.08, 'hspace': 0.2, 'wspace': 0}
        )

    df_plot = df.loc[:, ('ert', slice(None), 'avg')]
    df_plot = df_plot.dropna(how='any')
    ys = df_plot.columns
    for i, y in enumerate(ys):
        ax[0].plot_date(df_plot.index, df_plot[y], '-', linewidth=4, label=y[1:])
    ax[0].set_xlim([datetime.date(year_start, month_start, day_start), datetime.date(year_end, month_end, day_end)])
    ax[0].set_ylabel('ERT [ohm m]')
    ax[0].legend()

    df_plot = df.loc[:, ('soil', slice(None), 'w_cnt_vol')]
    ys = df_plot.columns
    for i, y in enumerate(ys):
        ax[1].plot_date(df_plot.index, df_plot[y], '-', linewidth=4, label=y[1])
    ax[1].set_xlim([datetime.date(year_start, month_start, day_start), datetime.date(year_end, month_end, day_end)])
    ax[1].set_ylabel('w content [vol]')
    ax[1].legend()

    df_plot = df.loc[:, ('soil', slice(None), 'w_pot_kPa')]
    ys = df_plot.columns
    for i, y in enumerate(ys):
        ax[2].plot_date(df_plot.index, -df_plot[y], '-', linewidth=4, label=y[1])
    ax[2].set_xlim([datetime.date(year_start, month_start, day_start), datetime.date(year_end, month_end, day_end)])
    ax[2].set_ylabel('- w potential [kPa]')
    ax[2].set_yscale('log')
    ax[2].legend()

    df_plot = df.loc[:, (['soil'], ['5te_1', '5te_2', '5te_3', '5te_4'], ['temp_C'])]
    ys = df_plot.columns
    for i, y in enumerate(ys):
        ax[3].plot_date(df_plot.index, df_plot[y], '-', linewidth=4, label=y[1])
    ax[3].set_xlim([datetime.date(year_start, month_start, day_start), datetime.date(year_end, month_end, day_end)])
    ax[3].set_ylabel('soil temp [C]')
    ax[3].legend()

    df_plot = df.loc[:, (['weather'], ['ARD2'], ['TAIR', 'RAIN'])]
    ys = df_plot.columns
    for i, y in enumerate(ys):
        ax[4].plot_date(df_plot.index, df_plot[y], '-', linewidth=4, label=y)
    ax[4].set_xlim([datetime.date(year_start, month_start, day_start), datetime.date(year_end, month_end, day_end)])
    ax[4].set_ylabel('daily rain [mm] air temp [C]')

    locator = matplotlib.dates.AutoDateLocator(minticks=5, maxticks=20)
    formatter = mdates.ConciseDateFormatter(locator)
    ax[4].xaxis.set_major_locator(locator)
    ax[4].xaxis.set_major_formatter(formatter)
    fig.autofmt_xdate()
    ax[4].set_xlim([datetime.date(year_start, month_start, day_start), datetime.date(year_end, month_end, day_end)])
    ax[4].legend()
    plt.tight_layout()
    plt.savefig('summary.pdf')
    plt.show()


def plot_df(df, output_name):
    fig, ax = plt.subplots(1, 1, figsize=(12, 6.5))
    fig.autofmt_xdate()
    for c in df.columns:
        plt.plot(df.index, df[c], '-', linewidth=2, ms=3, label=c)
    locator = matplotlib.dates.AutoDateLocator(minticks=25, maxticks=35)
    formatter = mdates.ConciseDateFormatter(locator)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)
    ax.set_xlim([datetime.date(2020, 4, 15), datetime.date(2020, 6, 1)])
    # ax.set_ylabel('solar radiation [W/m^2]')
    plt.tight_layout()
    plt.legend()
    plt.savefig(output_name, dpi=600)
    plt.show()
    plt.close()


def correlation(df, res_col='avg'):
    df = df.loc[:, (['ert', 'soil'], slice(None), ['avg', 'avg_comp', 'std', 'w_cnt_vol', 'temp_C'])]
    # df = df.dropna(how='any')
    df = df.loc[df[('ert', 'sensor1', res_col)].notnull()]

    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    # yerr=df.loc[:, ('ert', 'sensor1', slice(None))]
    plt.errorbar(
        x=df[('soil', '5te_1', 'w_cnt_vol')],
        y=df[('ert', 'sensor1', res_col)],
        yerr=df[('ert', 'sensor1', 'std')] / 2,
        fmt='o',
        markersize=0.1,
        )
    seaborn.scatterplot(
        data=df,
        ax=ax,
        x=('soil', '5te_1', 'w_cnt_vol'),
        y=('ert', 'sensor1', res_col),
        ci=('ert', 'sensor1', 'std'),
        sizes=(30, 150),
        s=90,
        size=('soil', '5te_1', 'temp_C'),
        hue=df.index,
        alpha=1,
        legend="brief",
        )
    plt.legend(ncol=2, fancybox=True, framealpha=0.5, loc=1, prop={"size": 8})
    plt.tight_layout()
    plt.savefig("ert_cnt_5te1.pdf")
    plt.show()

    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    plt.errorbar(
        x=df[('soil', '5te_2', 'w_cnt_vol')],
        y=df[('ert', 'sensor2', res_col)],
        yerr=df[('ert', 'sensor2', 'std')] / 2,
        fmt='o',
        markersize=0.1,
        )
    seaborn.scatterplot(
        data=df,
        ax=ax,
        x=('soil', '5te_2', 'w_cnt_vol'),
        y=('ert', 'sensor2', res_col),
        sizes=(30, 150),
        s=90,
        size=('soil', '5te_2', 'temp_C'),
        hue=df.index,
        alpha=1,
        legend="brief",
        )
    plt.legend(ncol=2, fancybox=True, framealpha=0.5, loc=1, prop={"size": 8})
    plt.tight_layout()
    plt.savefig("ert_cnt_5te2.pdf")
    plt.show()

    df = df.loc[df[('soil', '5te_3', 'w_cnt_vol')].notnull()]

    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    plt.errorbar(
        x=df[('soil', '5te_3', 'w_cnt_vol')],
        y=df[('ert', 'sensor3', res_col)],
        yerr=df[('ert', 'sensor3', 'std')] / 2,
        fmt='o',
        markersize=0.1,
        )
    seaborn.scatterplot(
        data=df,
        ax=ax,
        y=('ert', 'sensor3', 'avg'),
        x=('soil', '5te_3', 'w_cnt_vol'),
        sizes=(30, 150),
        s=90,
        size=('soil', '5te_3', 'temp_C'),
        hue=df.index,
        alpha=1,
        legend="brief",
        )
    plt.legend(ncol=2, fancybox=True, framealpha=0.5, loc=1, prop={"size": 8})
    plt.tight_layout()
    plt.savefig("ert_cnt_5te3.pdf")
    plt.show()

    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    df = df.loc[df[('soil', '5te_3', 'w_cnt_vol')].notnull()]
    plt.errorbar(
        x=df[('soil', '5te_4', 'w_cnt_vol')],
        y=df[('ert', 'sensor4', res_col)],
        yerr=df[('ert', 'sensor4', 'std')] / 2,
        fmt='o',
        markersize=0.1,
        )
    seaborn.scatterplot(
        data=df,
        ax=ax,
        y=('ert', 'sensor4', res_col),
        x=('soil', '5te_4', 'w_cnt_vol'),
        sizes=(30, 150),
        s=90,
        size=('soil', '5te_4', 'temp_C'),
        hue=df.index,
        alpha=1,
        legend="brief",
        )
    plt.legend(ncol=2, fancybox=True, framealpha=0.5, loc=1, prop={"size": 8})
    plt.tight_layout()
    plt.savefig("ert_cnt_5te4.pdf")
    plt.show()


def potential_content(df):
    df = df.loc[df[('soil', 'teros_1', 'w_pot_kPa')].notnull()]
    df = df.loc[df[('soil', '5te_1', 'w_cnt_vol')].notnull()]
    # df = df.loc[df[('ert', 'sensor1', 'avg')].notnull()]
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    seaborn.scatterplot(
        data=df,
        ax=ax,
        x=('soil', '5te_1', 'w_cnt_vol'),
        y=('soil', 'teros_1', 'w_pot_kPa'),
        size=('soil', '5te_2', 'temp_C'),
        sizes=(10, 50),
        hue=df.index,
        s=90,
        alpha=1,
        legend=False,
        edgecolor=None,
        )
    plt.savefig("pot_cnt_teros1_5te1.png")
    plt.show()

    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    seaborn.scatterplot(
        data=df,
        ax=ax,
        x=df.index,
        y=('soil', 'teros_1', 'w_pot_kPa'),
        size=('soil', '5te_1', 'temp_C'),
        sizes=(10, 50),
        hue=df.index,
        s=90,
        alpha=1,
        legend=False,
        edgecolor=None,
        )
    locator = matplotlib.dates.AutoDateLocator(minticks=25, maxticks=35)
    formatter = mdates.ConciseDateFormatter(locator)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)
    ax.set_xlim([datetime.date(2020, 4, 15), datetime.date(2020, 6, 1)])
    plt.savefig("potential_teros_1.png")
    plt.show()

    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    seaborn.scatterplot(
        data=df,
        ax=ax,
        x=df.index,
        y=('soil', '5te_1', 'w_cnt_vol'),
        size=('soil', '5te_1', 'temp_C'),
        sizes=(10, 50),
        hue=df.index,
        s=90,
        alpha=1,
        legend=False,
        edgecolor=None,
        )
    locator = matplotlib.dates.AutoDateLocator(minticks=25, maxticks=35)
    formatter = mdates.ConciseDateFormatter(locator)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)
    ax.set_xlim([datetime.date(2020, 4, 15), datetime.date(2020, 6, 1)])
    plt.savefig("content_5te_1.png")
    plt.show()

    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    seaborn.scatterplot(
        data=df,
        ax=ax,
        x=('soil', '5te_2', 'w_cnt_vol'),
        y=('soil', 'teros_2', 'w_pot_kPa'),
        sizes=(10, 50),
        size=('soil', '5te_2', 'temp_C'),
        s=90,
        hue=df.index,
        alpha=1,
        legend=False,
        edgecolor=None,
        )
    plt.savefig("pot_cnt_teros2_5te2.png")
    plt.show()

    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    seaborn.scatterplot(
        data=df,
        ax=ax,
        x=df.index,
        y=('soil', 'teros_2', 'w_pot_kPa'),
        size=('soil', '5te_2', 'temp_C'),
        sizes=(10, 50),
        hue=df.index,
        s=90,
        alpha=1,
        legend=False,
        edgecolor=None,
        )
    locator = matplotlib.dates.AutoDateLocator(minticks=25, maxticks=35)
    formatter = mdates.ConciseDateFormatter(locator)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)
    ax.set_xlim([datetime.date(2020, 4, 15), datetime.date(2020, 6, 1)])
    plt.savefig("content_5te_2.png")
    plt.show()

    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    seaborn.scatterplot(
        data=df,
        ax=ax,
        x=df.index,
        y=('soil', '5te_2', 'w_cnt_vol'),
        size=('soil', '5te_2', 'temp_C'),
        sizes=(10, 50),
        hue=df.index,
        s=90,
        alpha=1,
        legend=False,
        edgecolor=None,
        )
    locator = matplotlib.dates.AutoDateLocator(minticks=25, maxticks=35)
    formatter = mdates.ConciseDateFormatter(locator)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)
    ax.set_xlim([datetime.date(2020, 4, 15), datetime.date(2020, 6, 1)])
    plt.savefig("potential_teros_2.png")
    plt.show()


if __name__ == '__main__':
    args = get_cmd()

    # weather df
    weather_dir_file = os.path.join(args.weather_dir, args.weather_fname)
    weather = pd.read_csv(weather_dir_file, header=0, index_col=0, parse_dates=[0], infer_datetime_format=True)
    weather.index = weather.index.round('H')
    weather_mi_tuples = [('weather', 'ARD2', l0) for l0 in weather.columns.get_level_values(0).tolist()]
    weather_mi = pd.MultiIndex.from_tuples(weather_mi_tuples)
    weather.columns = weather_mi

    # ert df
    ert_dir_file = os.path.join(args.ert_dir, args.ert_fname)
    ert = pd.read_csv(ert_dir_file, header=[0, 1], index_col=0, parse_dates=[0], infer_datetime_format=True)
    ert.index = ert.index.round('H')
    ert_mi_tuples = [
        ('ert', l1, l2)
        for l1, l2 in zip(
            ert.columns.get_level_values(0).tolist(),
            ert.columns.get_level_values(1).tolist()
            )
        ]
    ert_mi = pd.MultiIndex.from_tuples(ert_mi_tuples)
    ert.columns = ert_mi

    # soil df
    soil_dir_file = os.path.join(args.soil_dir, args.soil_fname)
    soil = pd.read_csv(soil_dir_file, header=[0, 1], index_col=0, parse_dates=[0], infer_datetime_format=True)
    soil.index = soil.index.round('H')
    soil_mi_tuples = [
        ('soil', l1, l2)
        for l1, l2 in zip(
            soil.columns.get_level_values(0).tolist(),
            soil.columns.get_level_values(1).tolist(),
            )
        ]
    soil_mi = pd.MultiIndex.from_tuples(soil_mi_tuples)
    soil.columns = soil_mi

    # concat dfs
    df = pd.concat([weather, soil, ert], axis=1)
    # df = df.loc['2020-03-15 00:00:00': '2020-06-02 00:00:00']

    # compensate temperature effect on soil resistivity
    resistivities = [
        ('ert', 'sensor1', 'avg'),
        ('ert', 'sensor2', 'avg'),
        ('ert', 'sensor3', 'avg'),
        ('ert', 'sensor4', 'avg'),
        ]
    temperatures = [
        ('soil', '5te_1', 'temp_C'),
        ('soil', '5te_2', 'temp_C'),
        ('soil', '5te_3', 'temp_C'),
        ('soil', '5te_4', 'temp_C'),
        ]

    for r, t in zip(resistivities, temperatures):
        col_name = (r[0], r[1], 'avg_comp')
        df[col_name] = rho_temp_correction(df[r], df[t])

    # save main df
    out_dir_file = os.path.join(args.out_dir, args.out_fname)
    df = df.infer_objects()
    df.round(3)
    df.to_csv(out_dir_file, float_format='%g')

    plot_datetime(df)
    correlation(df, res_col='avg_comp')
    potential_content(df)

    # ert_avg = df.loc[:, ('ert', slice(None), 'avg')]
    # ert_avg = ert_avg.dropna(how='all')
    # soil_w_cnt = df.loc[:, ('soil', slice(None), 'w_cnt_vol')]
    # soil_w_pot = df.loc[:, ('soil', slice(None), 'w_pot_kPa')]
    # weather_rain = df.loc[:, ('weather', slice(None), 'RAIN')]

    # df_ert_noAll = df_ert.dropna(how='all')
    # plot_df(df_ert_noAll, 'ert.png')
    # plot_df(df_soil_wcnt, 'soil_cnt.png')
    # plot_df(df_soil_wpot, 'soil_pot.png')
    # plot_df(df_weather_rain, 'rain.png')

    # df = df.loc['2020-04-15 00:00:00': '2020-06-02 00:00:00']

    # sensors.index = pd.to_datetime(sensors.index)
    # sensors['datetime'] = sensors.index
    # sensors['datetimems'] = pd.to_datetime(sensors.index, unit='ms')
    # rho['datetime'] = pd.to_datetime(rho['datetime'])
    # rho['datetimems'] = pd.to_datetime(rho['datetime'], unit='ms')
