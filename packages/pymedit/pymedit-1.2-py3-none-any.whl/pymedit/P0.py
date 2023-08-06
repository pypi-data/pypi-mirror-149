# This file is part of pymedit.
#
# pymedit is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# pymedit is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# A copy of the GNU General Public License is included below.
# For further information, see <http://www.gnu.org/licenses/>
import numpy as np
import inspect
from .mesh import Mesh, meshCenters
from .abstract import __AbstractSol, display, SolException


class P0Function(__AbstractSol):
    """A structure for P0 functions (constant on each tetrahedra)
    defined on a 2D mesh, 
    based on the INDIRA .sol and .solb formats."""

    def __init__(self, M: Mesh, phi=None, debug=None):
        """Load a P0 function on a 2D mesh. 

        INPUTS
        ------

        M         :  input 2D mesh

        phi       :  Either:
            - the path of a ".sol" or ".solb" file 
            - the path of a ".gp" file with a list of values of the solution
              saved line by line (of size M.nt)
            - a list or a numpy.ndarray of function values for each of the mesh
              triangles (of size M.nt)
            - a lambda function `lambda x : f(x)`. The values at each triangle
                center
                (x[0],x[1]) will be computed accordingly.
            - a P1Function phi, in that case the value of the solution 
              at the triangle i is the mean of the values of phi at the 
              vertices of the triangle i

        debug : a level of verbosity for debugging when operations are applied
                to phi

        EXAMPLES
        --------
            >>> phi = P0Function(M, "phi.sol")
            >>> phi = P0Function(M, lambda x : x[0])

            >>> #values of the tags of the triangles
                phi = P0Function(M, M.triangles[:,-1])

        """
        try:
            super().__init__(M, phi, debug)
            self.sol = self.sol.flatten()
        except SolException:
            self.n = self.mesh.nt
            self.nsol = 1
            self.sol_types = np.asarray([1])
            if callable(phi):
                self.sol = np.apply_along_axis(phi, 1, meshCenters(M))
            elif phi is None:
                self.sol = np.zeros(self.mesh.nt)
            elif phi.__class__.__name__ == 'P1Function':
                self.sol = (phi[self.mesh.triangles[:, 0]-1]
                            + phi[self.mesh.triangles[:, 1]-1]
                            + phi[self.mesh.triangles[:, 2]-1])/3
        if self.nsol != 1 or self.sol_types.tolist() != [1] \
                or self.n != self.mesh.nt:
            raise Exception("Error: not a valid P0Function"
                            " solution.")
        if self.Dimension != 2:
            raise Exception(
                "Error: "+phi+" should be associated with a 2-D mesh.")
        if self.sol.shape not in [(self.mesh.nt,), (self.mesh.nt, 1)] \
                or self.n != self.mesh.nt:
            raise Exception("Error: the provided array of values should be"
                            f" of size ({self.mesh.nt},) while it is of size "
                            f"{self.sol.shape}.")

    def plot(self, cmap='jet', doNotPlot=False, tickFormat='2.1f',
             bcColor='k', bcLineWidth=0.5, niso=49,
             XLIM=None, YLIM=None, title=None):
        """Plot a P0 function with matplotlib."""
        import matplotlib as mp
        import numpy as np
        import matplotlib.pyplot as plt
        from mpl_toolkits.axes_grid1 import make_axes_locatable
        x, y = self.mesh.vertices[:, 0], self.mesh.vertices[:, 1]
        tri = self.mesh.triangles[:, :-1]-1
        z = self.sol
        fig, ax = plt.subplots()
        vmin = min(z)
        vmax = max(z)
        if len(set(z)) <= 10:
            cmap = plt.cm.Set3
            values = list(set(z))
            values.sort()
            middles = \
                [values[0], *[0.5*(x+y) for (x, y)
                              in zip(values[:-1], values[1:])], values[-1]]
            middles[0] = 2*middles[0]-middles[1]
            middles[-1] = 2*middles[-1]-middles[-2]

            class Normalize(mp.colors.Normalize):
                def __init__(self, vmin=None, vmax=None, clip=False):
                    mp.colors.Normalize.__init__(self, vmin, vmax, clip)

                def __call__(self, value, clip=None):
                    x, y = middles, np.linspace(
                        0, len(values)/cmap.N, len(middles))
                    return np.ma.masked_array(np.interp(value, x, y))
            norm = Normalize()
            bounds = middles
        else:
            cmap = plt.cm.jet
            cmaplist = [cmap(i) for i in range(cmap.N)]
            bounds = np.linspace(min(z), max(z), min(20, len(set(z))))
            norm = mp.colors.BoundaryNorm(bounds, cmap.N)
        if len(set(z)) <= 10:
            ticks = [0.5*(x+y) for (x, y) in zip(middles[:-1], middles[1:])]
            # print(middles);
            # print(values);
            # ticks=middles+values;
        else:
            ticks = bounds
        plot = ax.tripcolor(x, y, tri, cmap=cmap, norm=norm,
                            facecolors=z, edgecolor='gray')

        if title:
            plt.title(title)
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        ax.margins(0)
        # ax2=fig.add_axes([0.95,0.1,0.03,0.8]);
        try:
            cbar = mp.colorbar.ColorbarBase(plt.gca(), cmap=cmap,
                                            norm=norm, spacing='proportional',
                                            ticks=ticks,
                                            boundaries=bounds, format='%2.1f')
            cbar.set_ticklabels([format(x, tickFormat)
                                 for x in bounds])
            if len(set(z)) <= 10:
                cbar.ax.set_yticklabels(values)
        except:
            pass

        ax.set_aspect('equal')
        ax.tick_params(axis='both', which='both', length=0)
        plt.setp(ax.get_xticklabels(), visible=False)
        plt.setp(ax.get_yticklabels(), visible=False)
        if not XLIM is None:
            ax.set_xlim(XLIM)
        if not YLIM is None:
            ax.set_ylim(YLIM)
        if not doNotPlot:
            plt.show()
        return fig, ax
