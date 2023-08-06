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
from typing import Union
import subprocess
import tempfile
import os
import time
import shutil
from .abstract import display, tic, toc, __AbstractMesh, exec2, __AbstractSol
from .mesh3D import Mesh3D
from .mesh import Mesh
from .P1 import P1Function, P1Vector
from .P1_3D import P1Function3D, P1Vector3D, P0Function3D


def mshdist(M: Union[Mesh, Mesh3D, str], output=None,
            fastMarching=True, phi=None,
            verb=None, ncpu=1, it=None, options=None, debug=0):
    """Compute the signed distance function of a mesh subdomain with mshdist
    (if available).
    See https://github.com/ISCDtoolbox/Mshdist and the examples
    pymedit/examples/iscd2d.py
    pymedit/examples/iscd3d.py

    INPUT
    -----

    M : either a 2D Mesh, a 3D Mesh3D or the path of a mesh file.

    output : (optional) a file name to save the solution.

    debug : a tuning level for the verbosity

    phi : a level set function (for redistancing instead of computing the
                            signed distance to a meshed subdomain)

    Other arguments are those of the mshdist command

    OUTPUT
    ------

    If `output` is not None, then the function returns 1 if the execution of
    mshdist is successful. The signed distance function can then be loaded
    from the user, e.g. with
    >>> phi=P1Function(M,output)


    If `output` is None, then the function returns the signed distance
    function as a P1Function or P1Function3D object.
    """
    if shutil.which("mshdist") is None:
        raise Exception("Error: mshdist does not seem installed. "
                        "Please install it for "
                        "using mshdist command.", 0, 0, "red")
    with tempfile.TemporaryDirectory() as tmpdir:
        if isinstance(M, str):
            meshFile = M
            base, ext = os.path.splitext(M)
            outputMshdist = base+".sol"
        else:
            meshFile = os.path.join(tmpdir, "Th.meshb")
            outputMshdist = tmpdir+"/Th.sol"
            M.debug -= 3
            M.save(meshFile)
            M.debug += 3
            debug = M.debug if debug is None else max(debug, M.debug)
        if isinstance(phi, str):
            solFile = tmpdir+"/Th.sol"
            exec2("cp "+phi+" "+solFile)
        elif isinstance(phi, P1Function) or isinstance(phi,P1Function3D):
            solFile = tmpdir+"/Th.sol"
            phi.debug -= 3
            phi.save(solFile)
            phi.debug += 31
        verbosity = debug if verb is None else verb
        cmd = f"mshdist -v {verbosity} -ncpu {ncpu} {meshFile}"
        if phi is None:
            cmd += " -dom"
        if it:
            cmd += f" -it {it}"
        if fastMarching:
            cmd += f" -fmm"
        if options:
            cmd += f" {options}"
        exec2(cmd, level=1, debug=debug, silent=False)
        if isinstance(M, __AbstractMesh):
            if M.Dimension == 2:
                phi = P1Function(M, outputMshdist, debug-3)
            elif M.Dimension == 3:
                phi = P1Function3D(M, outputMshdist, debug-3)
            if output:
                phi.save(output)
            phi.debug += 3
            return phi
        if output:
            exec2("mv "+outputMshdist+" "+output, 5, debug)
    return 1


def advect(M: Union[Mesh, Mesh3D, str], sol: Union[P1Function, P1Function3D, str],
           vel: Union[P1Vector, P1Vector3D, str],
           output=None, T=1, verbosity=None, debug=0):
    """
    Advect a P1 function using the command `advect`
    See https://github.com/ISCDtoolbox/Advection and the examples
    pymedit/examples/iscd2d.py
    pymedit/examples/iscd3d.py

    INPUT
    -----

    M       : either 2D Mesh, 3D Mesh3D or file path of the mesh

    sol     : either a P1Function, P1Function3D or file path of the
              solution file to be advected

    vel     : either a P1Vector, P1Vector3D or file path of the advection
              velocity

    output  : (optional) output path of the advected solution to be saved

    T       : final advection time

    verbosity: advect command verbosity

    debug   : tune the python shell verbosity

    OUTPUT
    ------

    If `output` is not None, then the function returns 1 if the execution of
    advect is successful. The advected function can then be loaded
    from the user, e.g. with
    >>> phi=P1Function(M,output)


    If `output` is None, then the function returns the advected
    function as a P1Function or P1Function3D object.
    """
    if shutil.which("advect") is None:
        raise Exception("Error: advect does not seem installed. Please install it for "
                        "using advect command.", 0, 0, "red")
    with tempfile.TemporaryDirectory() as tmpdir:
        if isinstance(sol, str):
            solFile = sol
        else:
            solFile = tmpdir+"/phi.chi.sol"
            sol.debug -= 3
            sol.save(solFile)
            sol.debug += 3
        if isinstance(M, str):
            meshFile = M
        else:
            meshFile = tmpdir+"/Th.meshb"
            M.debug -= 3
            M.save(meshFile)
            M.debug += 3
            debug = max(debug, M.debug)
        if isinstance(vel, str):
            velFile = vel
        else:
            velFile = tmpdir+"/velocity.solb"
            vel.debug -= 3
            vel.save(velFile)
            vel.debug += 3
        if output:
            outputAdvect = output
        else:
            outputAdvect = tmpdir+"/phi.o.solb"
        cmd = "advect -nocfl -dt "+str(T)+" "+meshFile+" -c " + solFile + \
            " -s "+velFile \
            + " -o "+outputAdvect
        if verbosity:
            cmd = cmd+" +v"
        exec2(cmd, level=1, debug=debug, silent=False)
        # Will return phi if output is none --> need to load M
        if isinstance(M, str) and output is None:
            M = __AbstractMesh(M)
        if isinstance(M, __AbstractMesh):
            if M.Dimension == 2:
                phi = P1Function(M, outputAdvect, debug=debug-3)
                phi.debug += 3
            elif M.Dimension == 3:
                phi = P1Function3D(M, outputAdvect, debug=debug-3)
                phi.debug += 3
            return phi
    return 1


def __mmgHeader(M: Union[Mesh, Mesh3D, str], hmin=None, hmax=None, hgrad=None, hausd=None,
                params=None, output=None, sol=None, ls=False, verb=0, nr=True,
                extra_args="", debug=0, dimension=2, tmpdir=""):
    """Assemble mmg command arguments"""
    if isinstance(M, str):
        meshFile = M
    else:
        meshFile = tmpdir+"/Th.meshb"
        M.debug -= 3
        M.save(meshFile)
        M.debug += 3
    if output is None:
        outputMmg = tmpdir+"/Th.o.meshb"
    else:
        outputMmg = output
    options = ""
    if hausd is None and isinstance(hmin, float):
        hausd = 0.1*hmin
    if nr:
        options += " -nr"
    if hmin:
        options += f" -hmin {hmin}"
    if hmax:
        options += f" -hmax {hmax}"
    if hgrad:
        options += f" -hgrad {hgrad}"
    if hausd:
        options += f" -hausd {hausd}"
    if ls:
        options += " -ls"
    if sol:
        if isinstance(sol, str):
            solFile = sol
        else:
            solFile = tmpdir+"/Th.solb"
            sol.debug -= 3
            sol.save(solFile)
            sol.debug += 3
        options += f" -sol {solFile}"
    if verb:
        options += f" -v {verb}"
    if output:
        options += f" -out {output}"
    if extra_args:
        options += " "+extra_args
    if params:
        paramFile = os.path.splitext(meshFile)[0]+".mmg"+str(dimension)+"d"
        if os.path.isfile(params):
            exec2(f"cp {params} {paramFile}", level=5, debug=debug)
        else:
            with open(paramFile, "w") as f:
                f.write(params)
    return options, meshFile, outputMmg


def mmg2d(M: Union[Mesh, str], hmin=None, hmax=None, hgrad=None, hausd=None,
          output=None, sol=None, ls=False, verb=0, nr=True, params=None,
          extra_args="", debug=0):
    """
    Remesh a 2D mesh using the command `mmg2d_O3`
    See https://www.mmgtools.org/ and the example
    pymedit/examples/iscd2d.py

    INPUT
    -----

    M       : either 2D Mesh or the file path of the mesh

    hmin, hmax, hgrad, hausd : remeshing parameters

    output  : (optional) output path of the remeshed mesh to be saved

    sol     : either a metric file if ls=False (level set mode disabled)
                     a level set P1Function or solution file  if ls=True
                            (level set mode)

    ls     :  if set to True, then remesh according to the zero isovalue of
              the level set function sol

    verb   :  tune Mmg verbosity

    nr     :  if True, call mmg2d_O3 with option "-nr" (no ridge detection)

    params :  a file path or the content of the file setting local
              remeshing parameters.
              See https://www.mmgtools.org/local-parameters-for-boundaries

    extra_args: extra arguments to pass to the mmg2d_O3 command

    debug   : tune the python shell verbosity

    OUTPUT
    ------

    If `output` is not None, then the function returns 1 if the execution of
    mmg2d_O3 is successful. The output mesh can then be loaded
    from the user, e.g. with
    >>> M=Mesh(output)


    If `output` is None, then the function returns the remeshed 2D mesh as
    a Mesh object."""
    if shutil.which("mmg2d_O3") is None:
        raise Exception("Error: mmg2d_O3 does not seem installed. Please install it for "
                        "using mmg2d command.", 0, 0, "red")
    if isinstance(M, Mesh):
        debug = max(debug, M.debug)
    with tempfile.TemporaryDirectory() as tmpdir:
        cmd = "mmg2d_O3"
        options, meshFile, outputMmg = \
            __mmgHeader(M, hmin, hmax, hgrad, hausd, params, output, sol, ls, verb, nr,
                        extra_args=extra_args, debug=debug, dimension=2,
                        tmpdir=tmpdir)
        cmd = cmd + options + " "+meshFile
        exec2(cmd, level=1, debug=debug, silent=False)

        if output is None:
            # Load and returns the new mesh
            Mnew = Mesh(outputMmg, debug=debug-3)
            return Mnew
    return 1


def mmg3d(M: Union[Mesh3D, str], hmin=None, hmax=None, hgrad=None, hausd=None,
          output=None, sol=None, ls=False, verb=0, nr=True, params=None,
          extra_args="", debug=0):
    """
    Remesh a 3D mesh using the command `mmg3d_O3`
    See https://www.mmgtools.org/ and the example
    pymedit/examples/iscd3d.py

    INPUT
    -----

    M       : either 3D Mesh3D object or the file path of the mesh

    hmin, hmax, hgrad, hausd : remeshing parameters

    output  : (optional) output path of the remeshed mesh to be saved

    sol     : either a metric file if ls=False (level set mode disabled)
                     a level set P1Function or solution file  if ls=True
                            (level set mode)

    ls     :  if set to True, then remesh according to the zero isovalue of
              the level set function sol

    verb   :  tune Mmg verbosity

    nr     :  if True, call mmg3d_O3 with option "-nr" (no ridge detection)

    params :  a file path or the content of the file setting local
              remeshing parameters.
              See https://www.mmgtools.org/local-parameters-for-boundaries

    extra_args: extra arguments to pass to the mmg3d_O3 command

    debug   : tune the python shell verbosity

    OUTPUT
    ------

    If `output` is not None, then the function returns 1 if the execution of
    mmg3d_O3 is successful. The output mesh can then be loaded
    from the user, e.g. with
    >>> M=Mesh3D(output)


    If `output` is None, then the function returns the remeshed 3D mesh as
    a Mesh3D object."""
    if shutil.which("mmg3d_O3") is None:
        raise Exception("Error: mmg3d_O3 does not seem installed. Please install it for "
                        "using mmg3d command.", 0, 0, "red")
    if isinstance(M, Mesh3D):
        debug = max(M.debug, debug)
    with tempfile.TemporaryDirectory() as tmpdir:
        cmd = "mmg3d_O3"
        options, meshFile, outputMmg = \
            __mmgHeader(M, hmin, hmax, hgrad, hausd, params, output, sol, ls, verb, nr,
                        extra_args=extra_args, debug=debug, dimension=3,
                        tmpdir=tmpdir)
        cmd = cmd + options + " "+meshFile
        returncode, _, _, stdout = exec2(cmd, level=1, debug=debug, silent=False,strict=False)
        if returncode != 0:
            display(f"Warning, mmg exited with return code {returncode}.", color="red", level=0, debug=debug,flag='warning')
        if "Check" in stdout:
            display("Warning, mmg encountered quality problem.",
                    color="red", level=0,debug=debug,flag='warning')
        if "Topological" in stdout:
            display("Warning, mmg encountered topological problem.",
                    color="red", level=0,debug=debug,flag='warning')
        if "rarely pass" in stdout:
            display("Warning, mmg encountered we should rarely pass"
                    " here problem.",
                    color="red", level=0,debug=debug,flag='warning')

        if output is None:
            # Load and returns the new mesh
            Mnew = Mesh3D(outputMmg, debug=debug-3)
            Mnew.debug += 3
            return Mnew
    return 1


def generate2DMesh(M: Mesh, phis: list, labels: list, hmin=None, hmax=None,
                   hausd=None, hgrad=None, params=None,
                   detectCorners=False):
    """
    Generate a 2D mesh with prescribed boundary tags
    given an input raw mesh M and a set of level set functions determining
    the locations of these boundaries.

    Requires mmg2d_O3

    See the example
    pymedit/examples/generate2DMesh.py

    INPUT
    -----

    M     :    2D mesh such as a meshed bounding box (without boundary labels)

    phis  :    a list of lambda functions [phi1,phi2,...] such that
                points x satisfying phi[i](x) <= 0 on the boundary of M should be
                labelled by labels[i]
                These functions should partition the boundary of M into disjoint
                subdomains, i.e.
                for any x, phii(x)<=0 ===> phij(x)>0 for any j!=i

    labels :  a list of integer labels for each subdomain described by the level set
              functions of phis

    params :  a set of local parameters for the output mesh (remeshed with mmg3d)

    detectCorners : if set to True, then the corners of the bounding box will
                     be detected with mmg2d and automatically added.


    OUTPUT
    ------

    newM    :   a Mesh object with boundary triangles labelled according
                to each level set functions of phis and with respective and to
                the list argument `labels`

    """
    tic(12)
    debug = M.debug

    def phi(x): return min([p(x) for p in phis])
    if detectCorners:
        M = mmg2d(M, nr=False, extra_args="-noswap -noinsert -nomove -nosurf")
    phiP1 = P1Function(M, phi)
    newM = mmg2d(M, sol=phiP1, ls=True, nr=True,
                 params=params, extra_args="-noswap -noinsert -nomove -nosurf")
    newM.debug = debug
    for (nedge, edge) in enumerate(newM.edges.tolist()):
        (p0, p1) = tuple(edge[:-1])
        adjacents = newM.elemToTri(edge[:-1])
        if len(adjacents) == 1 and newM.triangles[adjacents[0]][-1] == 3 \
                and edge[-1] != 10:
            for (i, phii) in enumerate(phis):
                if max(phii(newM.vertex(p0)), phii(newM.vertex(p1))) <= 1e-7:
                    # print(f"Rename label of triangle {nedge}
                    # {edge[-1]} ==> {labels[i]}")
                    newM.edges[nedge, -1] = int(labels[i])
                    break
    # Now improve the quality
    finalM = mmg2d(newM, hmin, hmax, hgrad, hausd, nr=True, params=params)
    display("Generated 2D mesh in "+toc(12)+".", 1, debug, "green")
    return finalM

def generate3DMesh(M: Mesh3D, phis: list, labels: list, hmin=None, hmax=None,
                   hausd=None, hgrad=None, params=None,
                   detectCorners=False):
    """
    Generate a 3D mesh with prescribed boundary tags
    given an input raw mesh M and a set of level set functions determining
    the locations of these boundaries.

    Requires mmg3d_O3

    See the example
    pymedit/examples/generate3DMesh.py

    INPUT
    -----

    M     :    3D mesh such as a meshed bounding box (without boundary labels)

    phis  :    a list of lambda functions [phi1,phi2,...] such that
                points x satisfying phi[i](x) <= 0 on the boundary of M should be
                labelled by labels[i]
                These functions should partition the boundary of M into disjoint
                subdomains, i.e.
                for any x, phii(x)<=0 ===> phij(x)>0 for any j!=i

    labels :  a list of integer labels for each subdomain described by the level set
              functions of phis

    params :  a set of local parameters for the output mesh (remeshed with mmg3d)

    detectCorners : if set to True, then the corners of the bounding box will
                     be detected with mmg3d and automatically added.


    OUTPUT
    ------

    newM    :   a Mesh3D object with boundary triangles labelled according
                to each level set functions of phis and with respective and to
                the list argument `labels`

    """
    tic(12)
    debug = M.debug

    def phi(x): return min([p(x) for p in phis])
    if detectCorners:
        M = mmg3d(M, nr=False, extra_args="-noswap -noinsert -nomove -nosurf")
    phiP1 = P1Function3D(M, phi)
    newM = mmg3d(M, sol=phiP1, ls=True, nr=True,
                 params=params, extra_args="-noswap -noinsert -nomove -nosurf")
    newM.debug = debug
    for (ntri, tri) in enumerate(newM.triangles.tolist()):
        (p0, p1, p2) = tuple(tri[:-1])
        adjacents = newM.elemToTetra(tri[:-1])
        if len(adjacents) == 1 and newM.tetrahedra[adjacents[0]][-1] == 3 \
                and tri[-1] != 10:
            for (i, phii) in enumerate(phis):
                if max(phii(newM.vertex(p0)), phii(newM.vertex(p1)),
                       phii(newM.vertex(p2))) <= 1e-7:
                    # print(f"Rename label of triangle {ntri}
                    # {tri[-1]} ==> {labels[i]}")
                    newM.triangles[ntri, -1] = int(labels[i])
                    break
    # Now improve the quality
    finalM = mmg3d(newM, hmin, hmax, hgrad, hausd, nr=True, params=params)
    display("Generated 3D mesh in "+toc(12)+".", 1, debug, "green")
    return finalM


try:
    from pyfreefem import FreeFemRunner
    withPyFreeFem = True
except:
    withPyFreeFem = False


def saveToVtk(M: Union[Mesh3D, str], sols=None,
              labels=None, orders=None, output=None, debug=0):
    """Save a 3D mesh and solutions in the vtu file format.
    Requires pyfreefem and a running instance of FreeFEM.

    See freefem.org/ and
    https://gitlab.com/florian.feppon/pyfreefem

    INPUT
    -----

    M   :  either a Mesh3D object or the path of a 3D mesh file

    sols:  a list of either P1Function3D, P1Vector3D, P0Function3D or
           file paths of solution files

    labels : a list of names associated to each solution in `sols`

    orders : a list of integers associated to each solution in `sols` such
             that:
                orders[i] = 1 if the solution sols[i] should be saved at the
                              vertices of the mesh
                              (i.e. it is a P1 function or P1 vector)
                orders[i] = 0 if the solution sols[i] should be saved on the
                              tetrahedra of the mesh
                              (i.e. it is a P0 function)

    output : a .vtu output file

    debug  : an integer tuning the verbosity of the python shell
    """
    if withPyFreeFem:
        tic(128)
        with tempfile.TemporaryDirectory() as tmpdir:
            if isinstance(M, Mesh3D):
                debug = max(debug, M.debug)
                M.debug -= 3
                M.save(tmpdir+"/Th.meshb")
                M.debug += 3
                M = M.meshFile
            if not sols is None:
                if isinstance(sols, __AbstractSol):
                    sols = [sols]
                assert isinstance(M, str)
                nsols = len(sols)
                for i, sol in enumerate(sols):
                    if isinstance(sol, __AbstractSol):
                        sol.debug -= 3
                        sol.save(tmpdir+f"/phi{i}.solb")
                        sol.debug += 3
                        sols[i] = sol.solFile
                    if isinstance(sol, list):
                        # Sol is a vector
                        assert len(sol) == 3
                        for j, component in enumerate(sol):
                            if isinstance(component,
                                          (P0Function3D, P1Function3D)):
                                component.debug -= 3
                                component.save(tmpdir+f"/phi{i}_{j}.solb")
                                component.debug += 3
                                sol[j] = component.solFile
                    if isinstance(sol, P1Vector3D):
                        sol.debug -= 3
                        sol.x.save(tmpdir+f"/phi{i}_0.solb")
                        sol.y.save(tmpdir+f"/phi{i}_1.solb")
                        sol.z.save(tmpdir+f"/phi{i}_2.solb")
                        sol.debug += 3
                        sols[i] = [
                            tmpdir+f"/phi{i}_{j}.solb" for j in [0, 1, 2]]
                assert len(labels) == nsols
                assert len(orders) == nsols
            code = """
            load "medit"
            load "iovtk"
            mesh3 Th = readmesh3("$MESH");
            fespace Fh0(Th,P0);
            fespace Fh1(Th,P1);
            """
            if sols:
                code += "\nint[int] order = [" \
                    + ",".join([str(int(i)) for i in orders])+"];\n"
                code += f'string dataname="' + " ".join(labels)+'";'
                solutions = []
                orders = list(map(int, orders))
                components_labels = {0: 'x', 1: 'y', 2: 'z'}
                for i, solFile in enumerate(sols):
                    if isinstance(solFile, list):
                        components = []
                        for j, component in enumerate(solFile):
                            components.append(f'phi{i}{components_labels[j]}')
                            code += f"""
                                Fh{orders[i]} {components[-1]};
                                {components[-1]}[] = readsol("{component}");"""
                        solutions.append('['+','.join(components)+']')
                    else:
                        code += f"""
                        Fh{orders[i]} phi{i};
                        phi{i}[] = readsol("{solFile}");"""
                        solutions.append(f"phi{i}")
            code += f"""
            savevtk("{output}", Th """
            if sols:
                code += ","
                code += ",".join(solutions)
                code += ',dataname=dataname, order=order'
            code += ');'
            FreeFemRunner(code, run_file="exportToVtk.edp", debug=debug-3).execute({'MESH': M})
        display(f"Saved data to {output} in "+toc(128)+"s.", 1, debug, "green")
        return
    else:
        raise Exception("saveToVtk requires pyfreefem. Please install it with"
                        " 'pip install pyfreefem'")


def medit(mesh: Union[Mesh3D, str], sol=None, keys=[], silent=True, debug=0):
    """Plot a 3D mesh and/or a 3D P1 function with medit.
    INPUTS:
        mesh  : the mesh as a file path or a Mesh3D object
        mesh  : the solution as a file path or a P1Function3D object
        keys  : a set of key strokes to be sent to the medit graphical
                window
        silent: (default True) If silent, then standard output of medit is
                hidden in the python execution shell
        debug : an integer tuning the verbosity of the shell"""
    if shutil.which("medit") is None:
        display("medit does not seem installed. Please install it for "
                "3D plotting.", 0, 0, "red")
        return
    with tempfile.TemporaryDirectory() as tmpdir:
        if isinstance(mesh,(Mesh3D,Mesh)):
            mesh.debug -= 3
            meshFile = tmpdir+"/Th.meshb"
            mesh.save(meshFile)
            mesh.debug += 3
            debug = max(debug,mesh.debug)
        else:
            meshFile = mesh
        if isinstance(sol,__AbstractSol):
            sol.debug -= 3
            sol.mesh.debug -= 3
            sol.save(tmpdir+"/Th.solb")
            sol.mesh.debug += 3
            sol.debug += 3
        cmd = "medit "+meshFile
        display(cmd, level=1, debug=debug, color="magenta")
        if silent:
            proc= subprocess.Popen(cmd, shell="True",stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        else:
            proc= subprocess.Popen(cmd, shell="True")
        time.sleep(0.15)
        for key in keys:
            xdotool = "xdotool search --name \"Medit -\" windowactivate " \
                +f"--sync %1 key {key} "
            xdotool += " windowactivate $(xdotool getactivewindow)"
            try:
                p=subprocess.Popen(xdotool, shell="True")
            except:
                display("Warning, xdotool not supported on this system", 0,
                        0, "red")
            p.wait()
        proc.wait()
