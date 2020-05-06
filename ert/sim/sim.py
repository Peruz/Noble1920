import pandas as pd
import pybert as pb
import pygimli as pg
import matplotlib.pyplot as plt
import numpy as np

def init_nxyz():
    x = np.linspace(0, 31.5, 64)
    y = np.zeros(64)
    z = np.zeros(64)
    n = np.arange(1,65)
    nxyz = np.column_stack((n, x, y, z))
    return(nxyz)

def make_scheme(nxyz, sequence):
    scheme = pb.DataContainerERT()
    scheme.setSensorPositions(nxyz[:,1:])
    scheme.resize(len(sequence))
    for i, j in enumerate("abmn"):
        scheme.set(j, sequence[:, i] -1)
    scheme.set("valid", np.ones(len(sequence)))
    return(scheme)

def plot_k(sim_output):
    plt.plot(sim_output['k'], 'or', markersize=4)
    plt.savefig('k.png', dpi=600)
    plt.show()

    plt.plot(sim_output['rhoa'], 'or', markersize=4)
    plt.savefig('rhoa.png', dpi=600)
    plt.show()


if __name__ == "__main__":
    mesh = pg.load('../mesh/mesh_k.bms')

    # rho = np.ones(len(mesh.cells()))

    rho = []
    for cell in mesh.cells():
        if (cell.center().x() > 15 and cell.center().x() < 20 and cell.center().y() > -1.5 and cell.center().y() < 0):
            rho.append(1)
        else:
            rho.append(1)

    nxyz = init_nxyz()
    sequence = np.loadtxt('../seq/sequence.txt', dtype=int)
    scheme = make_scheme(nxyz, sequence)

    sim = pb.ERTManager()
    sim_result = sim.simulate(mesh=mesh, res=rho, scheme=scheme, noiseLevel=0.0)
    sim_result.save('sim_result.data')
    sim_output = pd.DataFrame(index=np.arange(scheme.size()), columns=['k', 'rhoa', 'r'])
    sim_output['rhoa'] = np.array(sim_result['rhoa'])
    sim_output['k'] = np.array(sim_result['k'])
    sim_output['r'] = sim_output['rhoa'] / sim_output['k']
    plot_k(sim_output)

#    sim_result.markInvalid(abs(sim_result('k')) > 100)
#    sim_result.markInvalid(sim_result('rhoa') < 5)
#    sim_result.markInvalid(sim_result('rhoa') > 400)
#    sim_result.removeInvalid()

    inv = pb.ERTManager()
    inv.setMesh(mesh)

    inv.setData(sim_result)
    inv_res = inv.invert(err=0.02, lam=20)
    inv.paraDomain.save("mesh.vtk")
    ax, cbar = inv.showModel(cmap='jet', cMin=0, cMax=50)
    plt.show()
    #mesh.addExportData('inv_rho', inv_res)
    #mesh.exportVTK('mesh_data.vtk')
