import pyvista as pv

def view(fname, scalar, name, edge):
    pv.set_plot_theme("document")
    fin = fname + '.vtk'
    mesh = pv.read(fin)
    plotter = pv.Plotter()
    plotter.add_mesh(mesh, show_edges=edge, scalars=scalar, show_scalar_bar=True, edge_color='darkgrey', cmap='RdBu_r', clim=(0,80))
    plotter.show_bounds(mesh=mesh, grid='k', location='outer', ticks='both', font_size=18, font_family='times', use_2d=True, padding=0.1)
    plotter.show(screenshot=name, dpi=600)

if __name__ == '__main__':
    view('mesh_data', 'inv_rho', 'inv.png', True)
    view('mesh_fwd_data', 'true_rho', 'true.png', False)
