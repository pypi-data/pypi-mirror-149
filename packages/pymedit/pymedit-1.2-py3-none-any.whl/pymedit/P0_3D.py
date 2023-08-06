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
import tempfile
import subprocess
from .mesh3D import Mesh3D, meshCenters3D
from .abstract import __AbstractSol, SolException, exec2, display


class P0Function3D(__AbstractSol):
    """A structure for 3D P0 functions (constant on each tetrahedra)
    defined on a mesh, 
    based on the INDIRA .sol and .solb formats."""

    def __init__(self, M: Mesh3D, phi=None, debug=None):
        """Load a 3D P0 function. 

        INPUTS
        ------

        M         :  input 3D mesh

        phi       :  Either:
            - the path of a ".sol" or ".solb" file 
            - the path of a ".gp" file with a list of values of the solution
              saved line by line (of size M.ntet)
            - a list or a numpy.ndarray of function values for each of the mesh
              tetrahedra (of size M.ntet)
            - a lambda function `lambda x : f(x)`. The values of the P0 function 
              is determined by the values of the function at the centers
              x[0],x[1],x[2] of each tetrahedra 
            - a P1Function3D phi, in that case the value of the solution 
              at the tetrahedra i is the mean of the values of phi at the 
              vertices of the tetrahedra i

        debug : a level of verbosity for debugging when operations are applied
                to phi

        EXAMPLES
        --------
            >>> phi = P0Function3D(M, "phi.sol")
            >>> phi = P0Function3D(M, lambda x : x[0])

            >>> #values of the tags of the triangles
                phi = P0Function3D(M, M.tetrahedra[:,-1])

        """
        try:
            super().__init__(M, phi, debug)
        except SolException:
            self.n = self.mesh.ntet
            self.nsol = 1
            self.sol_types = np.asarray([1])
            if callable(phi):
                self.sol = np.apply_along_axis(phi, 1, meshCenters3D(M))
            elif phi is None:
                self.sol = np.zeros(self.mesh.ntet)
            elif phi.__class__.__name__ == 'P1Function3D':
                self.sol = (phi[self.mesh.tetrahedra[:, 0]-1]
                            + phi[self.mesh.tetrahedra[:, 1]-1]
                            + phi[self.mesh.tetrahedra[:, 2]-1]
                            + phi[self.mesh.tetrahedra[:, 3]-1])/4
        if self.nsol != 1 or self.sol_types.tolist() != [1] or self.n != self.mesh.ntet:
            raise Exception("Error: not a valid P0Function3D"
                            " solution.")
        if self.Dimension != 3:
            raise Exception("Error: "+phi+" should be associated with a 3-D "
                            "mesh.")
        if self.sol.shape != (self.mesh.ntet,) or self.n != self.mesh.ntet:
            raise Exception("Error: the provided array of values should be"
                            f" of size ({self.mesh.ntet},) while it is of size "
                            f"{self.sol.shape}.")

    def plot(self, title=None, keys=None, silent=True):
        """Plot a 3D P0 function with medit.
        INPUTS:
            title : a message to be printed in the console before plotting
            keys  : a set of key strokes to be sent to the medit graphical 
                    window
            silent: (default True) If silent, then standard output of medit is 
                    hidden in the python execution shell"""
        from .external import medit
        if title:
            display(title, level=0, debug=self.debug, color="green")
        medit(self.mesh, self, keys=keys, silent=silent)
