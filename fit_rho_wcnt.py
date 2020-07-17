from scipy.optimize import least_squares
import numpy as np
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
    files.add_argument('-csv', type=str, help='csv file with data', default='all_noble1920.csv')
    files.add_argument('-ert_fname', type=str, help='file with rho data from ert analysis', default='ert.csv')
    files.add_argument('-weather_dir', type=str, help='path to weather_fname', default='weather')
    files.add_argument('-weather_fname', type=str, help='name of the file with weather data', default='weather.csv')
    files.add_argument('-soil_dir', type=str, help='path to soil_fname', default='soil')
    files.add_argument('-soil_fname', type=str, help='name of the file with soil data', default='soil.csv')
    output.add_argument('-out_dir', type=str, help='name of the output csv file', default='.')
    output.add_argument('-out_fname', type=str, help='name of the output directory', default='all_noble1920.csv')
    args = parse.parse_args()
    return(args)


def init_parameters():
    pass


def Waxman_Smits(F, GMC, D_g, D_w, phi, n, B_ws, c, sigma):
    """
    F: Formation factor
    GMC: Gravimetric Water Content
    D_g: Density of soil particles
    D_w: Density of water
    phi: Porosity
    n: Saturation exponent
    B_ws: Ion Mobility
    c: Cation echange capacity
    sigma_w: Water conductivity
    """
    rho = (
        F
        * ((((1 - phi) * D_g * GMC) / (phi * D_w)) ** -n)
        * (
            sigma_w
            + (
                Bws
                * (((1 - phi) * D_g * c) / (100 * phi))
                * ((phi * D_w) / ((1 - phi) * D_g * GMC))
            )
        ) ** -1

def simple(rho_sat):
    """
    F: Formation factor
    GMC: Gravimetric Water Content
    D_g: Density of soil particles
    D_w: Density of water
    phi: Porosity
    n: Saturation exponent
    B_ws: Ion Mobility
    c: Cation echange capacity
    sigma_w: Water conductivity
    """
    rho = rho_sat * Se ** -n 


def fit_single():
    pass


def fit_rho_wcnt(df, rhos, wcnts):
    for rc, wc in zip(rhos, wcnts):
        pass


if __name__ == '__main__':
    args = get_cmd()
    df = pd.read_csv(
        args.csv,
        header=[0, 1, 2],
        index_col=0,
        parse_dates=True,
        infer_datetime_format=True,
        )

    rhos = [
        ('ert', 'sensor1', 'avg_comp'),
        ('ert', 'sensor2', 'avg_comp'),
        ('ert', 'sensor3', 'avg_comp'),
        ('ert', 'sensor4', 'avg_comp'),
        ]
    wcnts = [
        ('soil', '5te_1', 'w_cnt_vol'),
        ('soil', '5te_2', 'w_cnt_vol'),
        ('soil', '5te_3', 'w_cnt_vol'),
        ('soil', '5te_4', 'w_cnt_vol'),
        ]
