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
import scipy.sparse as sp
import scipy.sparse.linalg as lg
from .mesh import Mesh, shapeGradients, integrateP0P1Matrix, metric
from .mesh import integrateP1P1Matrix
from .abstract import __AbstractSol, display, tic, toc, SolException
from .P0 import P0Function


class P1Function(__AbstractSol):
    """A structure for P1 functions (piecewise linear on each triangle)
    defined on a 2D mesh, 
    based on the INRIA .sol and .solb  formats."""

    def __init__(self, M: Mesh, phi=None, debug=None, importfrom=None):
        """Load a P1 function on a 2D mesh. 

        INPUTS
        ------

        M         :  input 2D mesh

        phi       :  Either:
            - the path of a ".sol" or ".solb" file 
            - the path of a ".gp" file with a list of values of the solution
              saved line by line (of size M.nv)
            - a list or a numpy.ndarray of function values for each of the mesh
              vertices (of size M.nv)
            - a lambda function `lambda x : f(x)`. The values at each vertices
                (x[0],x[1]) will be computed accordingly.
            - a P0Function phi, in that case the conversion of phi to a P0 
              function is performed by solving the variational problem
                Find `phiP1` a P1Function such that for all `v` P1Function, 
                    int2d(M)(phiP1*v)=int2d(M)(phi*v).

        debug : a level of verbosity for debugging when operations are applied
                to phi

        EXAMPLES
        --------
            >>> phi = P1Function(M, "phi.sol")
            >>> phi = P1Function(M, lambda x : x[0])

            >>> #values of the tags of the vertices
                phi = P1Function(M, M.vertices[:,-1])

        """
        if importfrom:
            from pyfreefem import FreeFemRunner
            code = """
load "medit";
mesh Th=readmesh("$SCRIPTDIR/Th.mesh");
fespace Fh1b(Th,$IMPORT);
fespace Fh1(Th,P1);
Fh1b phi;
{
string dummy="";
ifstream f("""+'"'+phi+'"'+""");
f>>dummy;
for(int i=0;i<Fh1b.ndof;i++){
f>>phi[][i];
}
}
Fh1 phiInterp=phi;
savesol("$SCRIPTDIR/phi.sol",Th,phiInterp,order=1);
"""
            if debug is None:
                debug = 0
            with FreeFemRunner(code,debug=debug) as runner:
                M.save(runner.script_dir+'/Th.mesh')
                runner.execute({'IMPORT':importfrom})
                self.__init__(M, runner.script_dir+'/phi.sol', debug)
            return
        try:
            super().__init__(M, phi, debug)
            self.sol = self.sol.flatten()
        except SolException:
            self.n = self.mesh.nv
            self.nsol = 1
            self.sol_types = np.asarray([1])

            if callable(phi):
                try:
                    self.sol = np.apply_along_axis(phi, 1, self.mesh.vertices)
                except TypeError:
                    newsol = lambda x : phi(x[0],x[1])
                    self.sol = np.apply_along_axis(newsol, 1, self.mesh.vertices)
            elif isinstance(phi, P0Function):
                display("Converting P0 function into P1 function.", 2,
                        self.debug, "green")
                tic(20)
                B = integrateP0P1Matrix(self.mesh)
                A = integrateP1P1Matrix(self.mesh)
                RHS = B.dot(phi.sol)
                self.sol = lg.cg(A, RHS, tol=1e-7)[0]
                display(f"Conversion achieved in {toc(20)}s.", 3, self.debug,
                        "orange_4a")
            elif isinstance(phi, P1Function):
                self.sol = phi.sol.copy()
            elif phi is None:
                self.sol = np.zeros(self.mesh.nv)
        if self.nsol != 1 or self.sol_types.tolist() != [1] \
                or self.n != self.mesh.nv:
            raise Exception("Error: "+phi+" is not a valid P1Function"
                            " solution file.")
        if self.Dimension != 2:
            raise Exception("Error: "+phi+" should be associated with "
                            "a 2-D mesh.")
        if self.sol.shape != (self.mesh.nv,) or self.n != self.mesh.nv:
            raise Exception("Error: the provided array of values should be"
                            f" of size ({self.mesh.nv},) while it is of size "
                            f"{self.sol.shape}.")

    def gradientP0(self) -> np.ndarray:
        """
        Returns the components of the P0 gradient of the P1 function.

        OUTPUT
        ______

        (gradx,grady) where gradx and grady are of size self.mesh.nt and 
                      containing the values of the gradient of self on every 
                      triangle
        """
        gradLambdaA, gradLambdaB, gradLambdaC = shapeGradients(self.mesh)
        if not hasattr(self, '_P1Function__gradientP0'):
            self.__gradientP0 = \
                (gradLambdaA.T*self.sol[self.mesh.triangles[:, 0]-1]
                 + gradLambdaB.T*self.sol[self.mesh.triangles[:, 1]-1]
                 + gradLambdaC.T*self.sol[self.mesh.triangles[:, 2]-1]).T
        return self.__gradientP0

    def gradientP1(self)->'P1Vector':
        """
        Returns the gradient of the P1 function as a P1Vector.
        The gradient is computed by converting the components of the
        P0 gradient into a P1 functions"""
        return P1Vector(self.mesh, [self.dxP1(), self.dyP1()])

    def dxP0(self)->P0Function:
        """
        Returns the x component of the P0 gradient
        """
        return P0Function(self.mesh, self.gradientP0()[:, 0])

    def dyP0(self)->P0Function:
        """
        Returns the y component of the P0 gradient
        """
        return P0Function(self.mesh, self.gradientP0()[:, 1])

    def dxP1(self)->'P1Function':
        """
        Returns the x component of the P1 gradient
        """
        return P1Function(self.mesh, self.dxP0())

    def dyP1(self)->'P1Function':
        """
        Returns the y component of the P1 gradient
        """
        return P1Function(self.mesh, self.dyP0())

    def eval(self, x):
        """
        Evaluate at a set of points x using piecewise linear interpolation
        """
        if not hasattr(self, '_P1Function__triInterp'):
            from matplotlib.tri import Triangulation, LinearTriInterpolator
            triObj = Triangulation(self.mesh.vertices[:,0],self.mesh.vertices[:,1]) 
            #linear interpolation
            self.__triInterp = LinearTriInterpolator(triObj,self.sol)
        return self.__triInterp(x[:,0],x[:,1])

    def plot(self, cmap='jet', doNotPlot=False, tickFormat='',
             niso=49, XLIM=None, YLIM=None,
             title=None, vmin=None, vmax=None, fill=True, boundary=None,boundary_linewidth=2,
             **kwargs):
        """Plot a P1 function with matplotlib."""
        import matplotlib as mp
        import matplotlib.pyplot as plt
        from mpl_toolkits.axes_grid1 import make_axes_locatable
        x, y = self.mesh.vertices[:, 0], self.mesh.vertices[:, 1]
        triang = self.mesh.triangles[:, :-1]-1

        z = self.sol
        if fill:
            fig, ax = plt.subplots()
        if not vmin is None:
            levels = kwargs.get('levels', np.linspace(vmin, vmax, niso))
            if fill:
                plot = plt.tricontourf(x, y, triang, z, levels=levels,
                                       cmap=cmap)
            else:
                plot = plt.tricontour(x, y, triang, z,
                                      levels=levels)
        else:
            vmin = min(z)
            vmax = max(z)
            levels = kwargs.get('levels', np.linspace(vmin, vmax, niso))
            if fill:
                plot = plt.tricontourf(x, y, triang, z, niso, cmap=cmap, extend="both")
            else:
                fig, ax = self.mesh.plot(doNotPlot=True, colormap='dim',
                                         boundaryColor='b',
                                         boundary_linewidth=0.5)
                plot = ax.tricontour(x, y, triang, z, 1, levels=[
                                     0], linewidths=0.5, colors='indigo')
        if boundary:
            if boundary == 'all':
                boundary = self.mesh.Boundaries.keys()
            for i, bc in enumerate(boundary):
                edges = self.mesh.edges[np.where(self.mesh.edges[:, -1] == bc)[0]]
                X = self.mesh.vertices[edges[:, 0]-1][:, :-1]
                Y = self.mesh.vertices[edges[:, 1]-1][:, :-1]
                lines = [[tuple(x), tuple(y)]
                         for (x, y) in zip(X.tolist(), Y.tolist())]
                color = mp.cm.Dark2(i)
                lc = mp.collections.LineCollection(
                    lines, linewidths=boundary_linewidth, colors=color,
                    zorder=100)
                ax.add_collection(lc)
        if title:
            plt.title(title)
        if fill:
            divider = make_axes_locatable(ax)
            cax = divider.append_axes("right", size="5%", pad=0.05)
            ax.margins(0)
            cbar = fig.colorbar(plot, cax=cax)
            cbar.set_ticks(np.linspace(vmin, vmax, 5))
            if tickFormat:
                cbar.set_ticklabels([format(x, tickFormat)
                                     for x in np.linspace(vmin, vmax, 5)])
            cbar.ax.tick_params(labelsize=16)
            if not kwargs.get('colorbar',True):
                cbar.remove()
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


class P1Vector(__AbstractSol):
    """A structure for P1 vectors (components are piecewise linear on 
    each triangle) on a 2D mesh, 
    based on the INRIA .sol and .solb formats."""

    def __init__(self, M: Mesh, phi=None, debug=None):
        """Load a P1 vector on a 2D mesh. 

        INPUTS
        ------

        M         :  input 2D mesh

        phi       :  Either:
            - the path of a ".sol" or ".solb" file 
            - the path of a ".gp" file with an array of values of the solution
              saved line by line and separated by spaces (of size (M.nv,2))
            - a list or a numpy.ndarray of function values for each of the mesh
              vertices (of size (M.nv,2))
            - a list of two P1 functions determining the components x and y
            - a lambda function `lambda x : [ux(x),uy(x)]`.
              The components of the vector at each vertices
                (x[0],x[1]) is computed accordingly.

        debug : a level of verbosity for debugging when operations are applied
                to phi

        EXAMPLES
        --------
            >>> phi = P1Vector(M, "u.sol")
            >>> phi = P1Vector(M, lambda x : [x[0],1]) # vector field (x,1)

        """
        try:
            super().__init__(M, phi, debug)
        except SolException:
            self.n = self.mesh.nv
            self.nsol = 1
            self.sol_types = np.asarray([2])
            if isinstance(phi, list) and len(phi) == 2:
                x = P1Function(M, phi[0], self.debug)
                y = P1Function(M, phi[1], self.debug)
                self.sol = np.column_stack((x.sol, y.sol))
            elif callable(phi):
                self.sol = np.apply_along_axis(phi, 1, self.mesh.vertices)
            elif phi is None:
                self.sol = np.zeros((self.mesh.nv, 2))
            elif isinstance(phi, P1Vector):
                self.sol = phi.sol.copy()
            else:
                self.sol = np.asarray(phi)
        if self.nsol != 1 or self.sol_types.tolist() != [2]:
            raise Exception("Error: "+phi+" is not a valid P1Vector"
                            " solution file.")
        if self.Dimension != 2:
            raise Exception("Error: "+phi+" should be associated with "
                            "a 2-D mesh.")
        if self.sol.shape != (self.mesh.nv, 2):
            raise Exception("Error: the provided array of values should be"
                            f" of size ({self.mesh.nv},2) while it is of size "
                            f"{self.sol.shape}.")

    @property
    def x(self)->'P1Function':
        """ x component of a P1 vector as a P1 function"""
        return P1Function(self.mesh, self.sol[:, 0], self.debug)

    @property
    def y(self)->'P1Function':
        """ y component of a P1 vector as a P1 function"""
        return P1Function(self.mesh, self.sol[:, 1], self.debug)

    def plot(self, title=None, doNotPlot=False, XLIM=None, YLIM=None,
             fig=None, ax=None, scaling=1.5,color=False):
        """ Quiver plot of a 2D vector field with matplotlib"""
        import matplotlib.pyplot as plt
        import matplotlib as mp
        x, y = self.mesh.vertices[:, 0], self.mesh.vertices[:, 1]
        P = list(zip(x, y))
        (vx, vy) = zip(*self.sol)
        if fig is None:
            if color:
                fig, ax = \
                    self.mesh.plot(doNotPlot=True,
                                   colormap=[[1, 1, 1],
                                             [1, 1, 1]], edgeColor='gray',
                                   boundaryColor='b')
            else:
                fig, ax = \
                    self.mesh.plot(doNotPlot=True,
                                   colormap=[[0.9, 0.9, 1],
                                             [1, 1, 0.9]], edgeColor='gray',
                                   boundaryColor='b')
        norms = [np.sqrt(x**2+y**2) for (x, y) in zip(vx, vy)]
        _, h = metric(self.mesh, True)
        localSize = (1/np.sqrt(h[:, 0])+1/np.sqrt(h[:, 1]))*0.5

        meshSize = np.mean(localSize)*scaling
        rescale = np.max(norms)/meshSize
        vx = [x/rescale for x in vx]
        vy = [y/rescale for y in vy]
        norm = mp.colors.Normalize()
        norm.autoscale(norms)
        if color:
            plot = ax.quiver(x, y, vx, vy, norms, units='xy', scale_units='xy',cmap=mp.cm.jet,
                             angles='xy', scale=1, width=0.002, headwidth=3, alpha=0.8)
        else:
            plot = ax.quiver(x, y, vx, vy, color="black", units='xy', scale_units='xy',
                             angles='xy', scale=1, width=0.002, headwidth=3, alpha=0.8)
        if color:
            ax.margins(0)
            cbar = fig.colorbar(plot)
            #cbar.set_ticks(np.linspace(vmin, vmax, 5))
            #if tickFormat:
            #    cbar.set_ticklabels([format(x, tickFormat)
            #                         for x in np.linspace(vmin, vmax, 5)])
            cbar.ax.tick_params(labelsize=16)
        if title:
            plt.title(title)
        if not XLIM is None:
            ax.set_xlim(XLIM)
        if not YLIM is None:
            ax.set_ylim(YLIM)
        if not doNotPlot:
            plt.show()

abstractSolClass=__AbstractSol
class P1Metric(__AbstractSol):
    """A structure for metric files to use with mesh adaptation based on 
    the INRIA .sol and .solb formats."""

    def __init__(self, M: Mesh, phi=None, isotropic=False, debug=None):
        try:
            super().__init__(M, phi, debug)
        except SolException:
            self.n = self.mesh.nv
            self.nsol = 1
            self.sol_types = np.asarray([3],dtype=int)
            if isinstance(phi, list) and len(phi) == 3:
                m11 = P1Function(M, phi[0], self.debug)
                m12 = P1Function(M, phi[1], self.debug)
                m22 = P1Function(M, phi[2], self.debug)
                self.sol = np.column_stack((m11.sol, m12.sol, m22.sol))
            elif callable(phi):
                self.sol = np.apply_along_axis(phi, 1, self.mesh.vertices)
            elif phi is None:
                self.sol = np.zeros((self.mesh.nv, 3))
            elif isinstance(phi, abstractSolClass):
                self.sol = phi.sol.copy()
            else:
                self.sol = np.asarray(phi)
            if isotropic:
                if self.sol.shape != (self.mesh.nv,):
                        raise Exception("Error: provide only one component if you want to "
                                        "define an isotropic metric field.")
                self.sol = np.column_stack((self.sol, np.zeros_like(self.sol), self.sol))
        if self.nsol != 1 or self.sol_types.tolist() != [3]:
            raise Exception("Error: "+phi+" is not a valid P1Metric"
                            " solution file.")
        if self.Dimension != 2:
            raise Exception("Error: "+phi+" should be associated with "
                            "a 2-D mesh.")
        if self.sol.shape != (self.mesh.nv, 3):
            raise Exception("Error: the provided array of values should be"
                            f" of size ({self.mesh.nv},3) while it is of size "
                            f"{self.sol.shape}.")
