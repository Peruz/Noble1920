import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np


def stack_rho_wcnt(df):
    df_to_stack = df.loc[:, (['ert', 'soil'], slice(None), ['avg_comp', 'w_cnt_vol'])]
    df_to_stack = df_to_stack.loc[df_to_stack['ert', 'sensor1', 'avg_comp'].notnull()]
    ert_to_stack = df_to_stack.loc[:, ('ert', ['sensor1', 'sensor2', 'sensor3', 'sensor4'], 'avg_comp')]
    soil_to_stack = df_to_stack.loc[:, ('soil', ['5te_1', '5te_2', '5te_3', '5te_4'], 'w_cnt_vol')]
    ert_stack = ert_to_stack.stack([0, 1, 2])
    soil_stack = soil_to_stack.stack([0, 1, 2])
    df_stacked = pd.DataFrame(data={'soil': soil_stack.to_numpy(), 'ert': ert_stack.to_numpy()})
    return(df_stacked)


def fit_model(eff_sat, rho_sat, n):
    print(rho_sat, n)
    rho = rho_sat * eff_sat ** (- n)
    # plt.plot(eff_sat, rho, 'o')
    # plt.pause(1)
    return(rho)


def fit_rho_wcnt(df):
    popt, pcov = curve_fit(
        fit_model,
        xdata=df['soil'].to_numpy(),
        ydata=df['ert'].to_numpy(),
        p0=[1., 1.],
        )
    return(popt, pcov)


def fit_main(df):
    df = stack_rho_wcnt(df)
    popt, pcov = fit_rho_wcnt(df)
    r2 = calc_r2(fit_model, popt, df['soil'], df['ert'])
    fit_plot_final(df, popt[0], popt[1])
    return(popt, r2)


def fit_plot_final(df, rho_sat, n):
    fig, ax = plt.subplots(1, 1)
    ax.plot(df['soil'], df['ert'], 'or')
    model_x = np.linspace(0.2, 0.55, 201)
    calc = fit_model(model_x, rho_sat, n)
    ax.plot(model_x, calc, 'b')
    ax.set_xlabel('volumetric water content')
    ax.set_ylabel('ERT resistivity')
    plt.show()


def calc_r2(model, params, x, y_meas):
    y_calc = model(x, *params)
    y_meas_mean = np.mean(y_meas)
    SST = np.sum((y_meas - y_meas_mean) ** 2)
    SSR = np.sum((y_meas - y_calc) ** 2)
    r2 = 1 - SSR / SST
    return(r2)
