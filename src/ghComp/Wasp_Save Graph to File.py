# Wasp: Discrete Design with Grasshopper plug-in (GPL) initiated by Andrea Rossi
# 
# This file is part of Wasp.
# 
# Copyright (c) 2017, Andrea Rossi <a.rossi.andrea@gmail.com>
# Wasp is free software; you can redistribute it and/or modify 
# it under the terms of the GNU General Public License as published 
# by the Free Software Foundation; either version 3 of the License, 
# or (at your option) any later version. 
# 
# Wasp is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the 
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Wasp; If not, see <http://www.gnu.org/licenses/>.
# 
# @license GPL-3.0 <https://www.gnu.org/licenses/gpl.html>
#
# Significant parts of Wasp have been developed by Andrea Rossi
# as part of research on digital materials and discrete design at:
# DDU Digital Design Unit - Prof. Oliver Tessmann
# Technische Universitt Darmstadt


#########################################################################
##                            COMPONENT INFO                           ##
#########################################################################

"""
Saves current status of an aggregation to a .json file.
-
Provided by Wasp 0.5
    Args:
        G: Graph to save
        PATH: Path where to save the file
        NAME: Name of the exported file
        SAVE: True to export
    Returns:
        TXT: Text representation of the graph
        FILE: Path to the saved file
"""

ghenv.Component.Name = "Wasp_Save Graph to File"
ghenv.Component.NickName = 'SaveGraph'
ghenv.Component.Message = 'v0.5.001'
ghenv.Component.IconDisplayMode = ghenv.Component.IconDisplayMode.application
ghenv.Component.Category = "Wasp"
ghenv.Component.SubCategory = "6 | Aggregation"
try: ghenv.Component.AdditionalHelpFromDocStrings = "3"
except: pass


import sys
import os
import Rhino.Geometry as rg
import Grasshopper as gh
import json


## add Wasp install directory to system path
wasp_loaded = False
ghcompfolder = gh.Folders.DefaultAssemblyFolder
if ghcompfolder not in sys.path:
    sys.path.append(ghcompfolder)
try:
    from wasp import __version__
    wasp_loaded = True
except:
    msg = "Cannot import Wasp. Is the wasp folder available in " + ghcompfolder + "?"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Error, msg)

## if Wasp is installed correctly, load the classes required by the component
if wasp_loaded:
    from wasp.core import Graph


def main(graph, path, filename, save):
        
    check_data = True
    
    ## check inputs
    if graph is None:
        check_data = False
        msg = "No graph provided"
        ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
    
    if path is None:
        check_data = False
        msg = "No path provided"
        ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
    
    if filename is None:
        check_data = False
        msg = "No filename provided"
        ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
    
    if save is None:
        save = False
    
    ## execute main code if all needed inputs are available
    if check_data:
        
        graph_dict = graph.to_data()
        full_path = os.path.join(path, filename + ".json")
        
        if save:
            with open(full_path, "w") as outF:
                json.dump(graph_dict, outF)
        
        return json.dumps(graph_dict), full_path
    else:
        return -1

result = main(G, PATH, NAME, SAVE)

if result != -1:
    TXT = result[0]
    FILE = result[1]