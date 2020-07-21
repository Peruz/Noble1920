import matplotlib.pyplot as plt
import seaborn
import matplotlib
import matplotlib.dates as mdates
import datetime


def plot_df_pairs_mi3(df, x_col1, x_col2, x_col3, y_col1, y_col2, y_col3, fname):
    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    for xc1, yc1 in zip(x_col1, y_col1):
        for xc2, yc2 in zip(x_col2, y_col2):
            for xc3, yc3 in zip(x_col3, y_col3):
                df3 = df.loc[:, ([xc1, yc1], [xc2, yc2], [xc3, yc3])]
                df3 = df3.loc[df3[(xc1, xc2, xc3)].notnull()]
                df3 = df3.loc[df3[(yc1, yc2, yc3)].notnull()]
                seaborn.scatterplot(
                    data=df3,
                    ax=ax,
                    x=(xc1, xc2, xc3),
                    y=(yc1, yc2, yc3),
                    )
    plt.tight_layout()
    plt.savefig(fname)
    plt.show()


def correlation(df, res_col='avg', soil_col='w_cnt_vol', fig_name='ertRes_soilWcnt'):
    df = df.loc[
        :,
        (['ert', 'soil'], slice(None), ['std', 'temp_C', res_col, soil_col])
        ]
    # df = df.dropna(how='any')
    df = df.loc[df[('ert', 'sensor1', res_col)].notnull()]

    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    # yerr=df.loc[:, ('ert', 'sensor1', slice(None))]
    plt.errorbar(
        x=df[('soil', '5te_1', soil_col)],
        y=df[('ert', 'sensor1', res_col)],
        yerr=df[('ert', 'sensor1', 'std')] / 2,
        fmt='o',
        markersize=0.1,
        )
    seaborn.scatterplot(
        data=df,
        ax=ax,
        x=('soil', '5te_1', soil_col),
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
    fout = fig_name + '_1.pdf'
    plt.savefig(fout)
    plt.show()

    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    plt.errorbar(
        x=df[('soil', '5te_2', soil_col)],
        y=df[('ert', 'sensor2', res_col)],
        yerr=df[('ert', 'sensor2', 'std')] / 2,
        fmt='o',
        markersize=0.1,
        )
    seaborn.scatterplot(
        data=df,
        ax=ax,
        x=('soil', '5te_2', soil_col),
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
    fout = fig_name + '_2.pdf'
    plt.savefig(fout)
    plt.show()

    df = df.loc[df[('soil', '5te_3', soil_col)].notnull()]

    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    plt.errorbar(
        x=df[('soil', '5te_3', soil_col)],
        y=df[('ert', 'sensor3', res_col)],
        yerr=df[('ert', 'sensor3', 'std')] / 2,
        fmt='o',
        markersize=0.1,
        )
    seaborn.scatterplot(
        data=df,
        ax=ax,
        y=('ert', 'sensor3', res_col),
        x=('soil', '5te_3', soil_col),
        sizes=(30, 150),
        s=90,
        size=('soil', '5te_3', 'temp_C'),
        hue=df.index,
        alpha=1,
        legend="brief",
        )
    plt.legend(ncol=2, fancybox=True, framealpha=0.5, loc=1, prop={"size": 8})
    plt.tight_layout()
    fout = fig_name + '_3.pdf'
    plt.savefig(fout)
    plt.show()

    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    df = df.loc[df[('soil', '5te_3', soil_col)].notnull()]
    plt.errorbar(
        x=df[('soil', '5te_4', soil_col)],
        y=df[('ert', 'sensor4', res_col)],
        yerr=df[('ert', 'sensor4', 'std')] / 2,
        fmt='o',
        markersize=0.1,
        )
    seaborn.scatterplot(
        data=df,
        ax=ax,
        y=('ert', 'sensor4', res_col),
        x=('soil', '5te_4', soil_col),
        sizes=(30, 150),
        s=90,
        size=('soil', '5te_4', 'temp_C'),
        hue=df.index,
        alpha=1,
        legend="brief",
        )
    plt.legend(ncol=2, fancybox=True, framealpha=0.5, loc=1, prop={"size": 8})
    plt.tight_layout()
    fout = fig_name + '_4.pdf'
    plt.savefig(fout)
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
