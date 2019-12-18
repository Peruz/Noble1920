import pybert as pb
import pygimli as pg
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

invert = True
plot_misfit = True

if invert:
    files = [f for f in os.listdir() if f.endswith('.dat')]
    for f in files:
        print('INFO inverting:   ', f)
        # load data and mesh
        data = pb.load(f)
        mesh = pg.load('../mesh/mesh.bms')
        # set up inversion
        ert = pb.ERTManager()
        ert.setData(data)
        ert.setMesh(mesh)
        # run inversion
        res = ert.invert(err=0.05, lam=20, robustData=False)
        # vtk
        ert.paraDomain.save('mesh_para')
        mesh_para = pg.load('mesh_para.bms')
        mesh_para.addExportData('res', res)
        mesh_para.exportVTK(f + 'mesh_para.vtk')
        # plot
        ax, cbar = ert.showModel(cMap='jet')
        plt.savefig(f + 'inv.png', dpi=600)
        plt.show()
        # misfit
        fwd_response = np.array(ert.inv.response())
        measured = np.array(data['rhoa'])
        misfit = pd.DataFrame({'fwd': fwd_response, 'measured': measured})
        misfit['misfit'] = misfit['fwd'] - misfit['measured']
        misfit['abs_misfit'] = misfit['misfit'].abs()
        misfit['percent_misfit'] = misfit['abs_misfit'] / misfit['measured'].abs()
        name_misfit = f.replace('.dat', '_misfit.csv')
        misfit.to_csv(name_misfit)


if plot_misfit:
    files = [f for f in os.listdir() if f.endswith('_misfit.csv')]
    for f in files:
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
        name_fig = f.replace('.csv', '.png')
        plt.savefig(name_fig, dpi=500)
        plt.close()
