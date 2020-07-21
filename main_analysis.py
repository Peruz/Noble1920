import argparse
import os
import pandas as pd
# import plotting_functions
# import matplotlib.pyplot as plt
import analyze_correlation


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


def rho_temp_correction(rho_vec, temp_vec, temp_reference=25, temp_slope_compensation=0.025):
    """
    temperature compensation of the soil resistivity with ratio model
    based on:
    Comparing temperature correction models for soil electrical conductivity measurement
    eq. 2, pag. 56
    """
    rho_temp_reference = rho_vec + (temp_slope_compensation * (temp_vec - temp_reference) * rho_vec)
    return(rho_temp_reference)


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

    resistivities = [
        ('soil', '5te_1', 'conductivity_mS/cm'),
        ('soil', '5te_2', 'conductivity_mS/cm'),
        ('soil', '5te_3', 'conductivity_mS/cm'),
        ('soil', '5te_4', 'conductivity_mS/cm'),
        ]
    temperatures = [
        ('soil', '5te_1', 'temp_C'),
        ('soil', '5te_2', 'temp_C'),
        ('soil', '5te_3', 'temp_C'),
        ('soil', '5te_4', 'temp_C'),
        ]

    for r, t in zip(resistivities, temperatures):
        col_name = (r[0], r[1], 'res_comp')
        df[col_name] = 1 / (df[r] / 10)

    # save main df
    out_dir_file = os.path.join(args.out_dir, args.out_fname)
    df = df.infer_objects()
    df.round(3)
    df.to_csv(out_dir_file, float_format='%g')

    popt, r2 = analyze_correlation.fit_main(df)
    print(popt)

    # plotting_functions.plot_datetime(df)
    # plotting_functions.correlation(df, res_col='avg_comp', soil_col='w_cnt_vol', fig_name='ertRes_soilWcnt')
    # plotting_functions.correlation(df, res_col='avg_comp', soil_col='res_comp', fig_name='ertRes_soilRes')
    # plotting_functions.potential_content(df)

    # plot correlation together
    # plotting_functions.plot_df_pairs_mi3(
    #     df=df,
    #     x_col1=['soil'],
    #     x_col2=['5te_1', '5te_2', '5te_3', '5te_4'],
    #     x_col3=['w_cnt_vol'],
    #     y_col1=['ert'],
    #     y_col2=['sensor1', 'sensor2', 'sensor3', 'sensor4'],
    #     y_col3=['avg_comp'],
    #     fname='ertRes_soilWcnt_together',
    #     )

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
