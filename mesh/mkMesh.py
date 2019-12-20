import pygimli as pg
import pygimli.meshtools as mt
import numpy as np
import matplotlib.pyplot as plt
import pyvista as pv


def show_mesh(mesh, elec):
    pg.show(mesh, showBoundary=True, markers=True, hold=True, showMesh=True)
    plt.plot(elec, np.zeros_like(elec), 'or')
    plt.xlim([-2, 33.5])
    plt.ylim([-8, 0])
    plt.title('mesh')
    plt.show()

def make_mesh():
    elec = np.linspace(0, 31.5, 64)
    world = mt.createWorld(start=[-20, -30], end=[51.5, 0], worldMarker=True, area=2)
    medium = mt.createRectangle(start=[-2, -7], end=[33.6, 0], marker=2, area=0.05)
    for e in elec:
        medium.createNode(pg.RVector3(e, 0, 0), marker=pg.MARKER_NODE_ELECTRODE)
        medium.createNode(pg.RVector3(e,-0.05, 0))
    geom = mt.mergePLC([world, medium])
    mesh = mt.createMesh(geom, quality=33, smooth=[1,20])
    return(mesh, elec)

def view():
    pv.set_plot_theme("document")
    mesh = pv.read('mesh.vtk')
    plotter = pv.Plotter()
    plotter.add_mesh(mesh, show_edges=True, scalar='Marker', show_scalar_bar=False, edge_color='k', cmap='RdBu', clim=(-1, 1))
    plotter.show_bounds(mesh=mesh, grid='back', location='outer', ticks='both', font_size=18, font_family='times', use_2d=True, padding=0.1)
    plotter.show()

if __name__ == '__main__':
    mesh, elec = make_mesh()
    show_mesh(mesh, elec)
    mesh.save('mesh.bms')
    mesh.exportVTK('mesh.vtk')
    view()
