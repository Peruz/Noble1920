import pybert as pb
import pygimli as pg
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

def invert_file(data, mesh):
    """ invert file and saves to para_mesh
    """
    ert = pb.ERTManager()
    ert.setData(data)
    ert.setMesh(mesh)
    res = ert.invert(err=0.05, lam=50, robustData=False)
    return(ert)

def invert_opt(data, mesh, lam):
    """ invert file and saves to para_mesh
    """
    ert = pb.ERTManager()
    ert.setData(data)
    ert.setMesh(mesh)
    res = ert.invert(err=0.05, robustData=False, lam=lam)
    chi2 = ert.inv.chi2()
    model = ert.inv.model()
    lam_record = []
    chi2_record = []
    model_record = []
    lam_record.append(lam)
    chi2_record.append(chi2)
    model_record.append(model)
    while not 0.8 < chi2 < 1.2:
        if chi2 < 0.8:
            lam *= 2
        if chi2 > 1.2:
            lam /= 3
        res = ert.invert(err=0.05, robustData=False, lam=lam, startModel=model)
        chi2 = ert.inv.chi2()
        model = ert.inv.model()
        model_record.append(model)
        lam_record.append(lam)
        chi2_record.append(chi2)
    return(ert, lam_record, chi2_record, model_record)

def save_vtk(f, ert):
    """ after the inversion ert instance contains: paradomain, resistivity, and coverage.
    """
    res = ert.resistivity
    cov = ert.coverageDC()
    ert.paraDomain.save('mesh_para')
    mesh_para = pg.load('mesh_para.bms')
    mesh_para.addExportData('res', res)
    mesh_para.addExportData('cov', cov)
    name_vtk = f.replace('.dat', '_inv.vtk')
    mesh_para.exportVTK(name_vtk)

def save_misfit(f, ert):
    """ after the inv the ert instance contains the fwd response to be compared with the data
    """
    fwd_response = np.array(ert.inv.response())
    measured = np.array(data['rhoa'])
    misfit = pd.DataFrame({'fwd': fwd_response, 'measured': measured})
    misfit['misfit'] = misfit['fwd'] - misfit['measured']
    misfit['abs_misfit'] = misfit['misfit'].abs()
    misfit['percent_misfit'] = misfit['abs_misfit'] / misfit['measured'].abs()
    name_misfit = f.replace('.dat', '_misfit.csv')
    misfit.to_csv(name_misfit)

def plot_vtk(f):
    data = pg.load(f)
    fig = plt.figure(figsize=(10, 5))
    ax = plt.gca()
    rho = data.exportData('res')
    cov = data.exportData('cov')
    ax, cbar = pg.show(mesh=data, data=rho, coverage=cov, cMap='jet', cMin=2, cMax=12, colorBar=True, ax = ax, showelectrodes=True, label='resistivity [ohm m]')
    ax.set_xlabel('m')
    ax.set_ylabel('m')
    plt.tight_layout()
    name_fig = f.replace('_inv.vtk', '_inv.png')
    plt.savefig(name_fig, dpi=600)
    plt.show()

def plot_misfit(f):
    misfit = pd.read_csv(f)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    ax1.plot(misfit['measured'], 'bo', markersize=7)
    ax1.plot(misfit['fwd'], 'ro', markersize=7)
    ax1.set_xlabel('num')
    ax1.set_ylabel('rho')
    ax2.plot(misfit['measured'], misfit['fwd'], 'og', markersize=7)
    ax2.set_xlabel('measured')
    ax2.set_ylabel('fwd calculated')
    ax2.axis('equal')
    fig.tight_layout()
    name_fig = f.replace('_misfit.csv', '_misfit.png')
    plt.savefig(name_fig, dpi=600)
    plt.show()


if __name__ == '__main__':

    do_invert = False
    do_invert_all = False
    do_plot_misfit = False
    do_plot_vtk = True

    if do_invert:
        mesh = pg.load('../mesh/mesh.bms')
        all_dat = [f for f in os.listdir() if f.endswith('.dat')]
        if not do_invert_all:
            inverted_dat = [f for f in all_dat if f.replace('.dat', '_inv.vtk') in os.listdir()]
            toinvert_dat = [f for f in all_dat if f not in inverted_dat]
        else:
            toinvert_dat = all_dat
        for f in toinvert_dat:
            print('---\n' * 2, f)
            data = pb.load(f)
            lam = 700
            #ert = invert_file(data, mesh)
            ert, lam_record, chi2_record, model_record = invert_opt(data, mesh, lam)
            print(lam_record)
            print(chi2_record)
            lam = lam_record[-1]
            save_misfit(f, ert)
            save_vtk(f, ert)

    if do_plot_misfit:
        misfit_files = [f for f in os.listdir() if f.endswith('_misfit.csv')]
        for f in misfit_files:
            plot_misfit(f)

    if do_plot_vtk:
        vtk_files = [f for f in os.listdir() if f.endswith('_inv.vtk')]
        for f in vtk_files:
            plot_vtk(f)
