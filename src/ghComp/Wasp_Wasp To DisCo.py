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
Export Wasp information for DisCo VR software.
DisCo (Discrete Choreography) is developed by Jan Philipp Drude at dMA Hannover - Prof. Mirco Becker.
Project DisCo is available at: http://www.project-disco.com/
--> WIP Component: might be incomplete or contain bugs <--
-
Provided by Wasp 0.2
    Args:
        PART: Parts to be aggregated in DisCo
        RULES: Aggregation rules
        COLL: OPTIONAL // Part collider. If not provided, part geometry will be used.
        PROB: OPTIONAL // Probability distribution for each part
        ADD_GEO: OPTIONAL // Additional geometry to import in DisCo (e.g., environment geometry)
        PATH: Path where to save the DisCo .json file
        NAME: Export file name
        SAVE: True to export
    Returns:
        TXT: ...
        FILE: ...
"""

ghenv.Component.Name = "Wasp_Wasp To DisCo"
ghenv.Component.NickName = 'Wasp2DisCo'
ghenv.Component.Message = 'VER 0.2.08'
ghenv.Component.IconDisplayMode = ghenv.Component.IconDisplayMode.application
ghenv.Component.Category = "Wasp"
ghenv.Component.SubCategory = "5 | DisCo VR"
try: ghenv.Component.AdditionalHelpFromDocStrings = "1"
except: pass

import sys
import json
import Rhino.Geometry as rg
import Grasshopper as gh

## add Wasp install directory to system path
ghcompfolder = gh.Folders.DefaultAssemblyFolder
wasp_path = ghcompfolder + "Wasp"
if wasp_path not in sys.path:
    sys.path.append(wasp_path)
try:
    import wasp
except:
    msg = "Cannot import Wasp. Is the wasp.py module installed in " + wasp_path + "?"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Error, msg)


def MeshToString(mesh, name):
    mesh_text = ""
    mesh_text += "\no " + name + "\n"
    
    for v in mesh.Vertices:
        mesh_text += "v "
        mesh_text += str(v.X) + " "
        mesh_text += str(v.Y) + " "
        mesh_text += str(v.Z) + "\n"
        
        
    for f in mesh.Faces:
        mesh_text += "f "
        t = f.A + 1
        mesh_text += str(t) + " "
        t = f.B + 1
        mesh_text += str(t) + " "
        t = f.C + 1
        mesh_text += str(t) + "\n"

        if (f.D != f.C):
            mesh_text += "f "
            t = f.A + 1
            mesh_text += str(t) + " "
            t = f.C + 1
            mesh_text += str(t) + " "
            t = f.D + 1
            mesh_text += str(t) + "\n"
    
    return mesh_text



def main(parts, rules, rule_groups, colliders, probabilities, additional_geometry, filepath, filename, save):
    
    check_data = True
    
    ## check inputs
    if len(parts) == 0:
        check_data = False
        msg = "No parts provided"
        ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
    
    if len(rules) == 0:
        check_data = False
        msg = "No parts provided"
        ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
    
    if len(colliders) != 0 and len(colliders) != len(parts):
        check_data = False
        msg = "Different count of parts and colliders. Please provide one collider for each part"
        ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
    
    if filepath is None:
        check_data = False
        msg = "No path provided"
        ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
    
    if filename is None:
        check_data = False
        msg = "No filename provided"
        ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
    
    if save is None:
        save = False
    
    if check_data:
        
        data_dict = {}
        
        probability_total = 0
        for prob in probabilities:
            probability_total += prob
        
        
        parts_data = []
        part_count = 0
        for part in parts:
            part_dict = {}
            
            center_vector = rg.Vector3d.Subtract(rg.Vector3d(0,0,0), rg.Vector3d(part.center))
            center_transform = rg.Transform.Translation(center_vector)
            
            part = part.transform(center_transform)
            
            part_dict["Name"] = part.name
            part_dict["Geometry"] = MeshToString(part.geo, "Geo_" + part.name)
            
            connections_data = []
            for conn in part.connections:
                conn_dict = {}
                
                conn_dict["ConID"] = conn.id
                conn_dict["Part"] = part.name
                conn_dict["ConType"] = conn.type
                
                conn_dict["PlaneOriginX"] = conn.pln.Origin.X
                conn_dict["PlaneOriginY"] = conn.pln.Origin.Y
                conn_dict["PlaneOriginZ"] = conn.pln.Origin.Z
                conn_dict["PlaneXVecX"] = conn.pln.XAxis.X
                conn_dict["PlaneXVecY"] = conn.pln.XAxis.Y
                conn_dict["PlaneXVecZ"] = conn.pln.XAxis.Z
                conn_dict["PlaneYVecX"] = conn.pln.YAxis.X
                conn_dict["PlaneYVecY"] = conn.pln.YAxis.Y
                conn_dict["PlaneYVecZ"] = conn.pln.YAxis.Z
                
                connections_data.append(conn_dict)
            
            part_dict["Connections"] = connections_data
            
            ## probabilities
            part_dict["Probability"] = 0
            if probability_total == 1:
                part_dict["Probability"] = probabilities[part_count]
            elif probability_total == 0:
                part_dict["Probability"] = 1.0/len(parts)
            else:
                part_dict["Probability"] = probabilities[part_count]/probability_total
            
            ## collider
            if len(colliders) == 0:
                part_dict["Collider"] = MeshToString(part.geo, "Col_" + part.name + "_0")
            else:
                current_collider = colliders[part_count]
                if type(current_collider) == wasp.Collider:
                    current_collider = current_collider.transform(center_transform)
                    if len(current_collider.geometry) == 1:
                        part_dict["Collider"] = MeshToString(current_collider.geometry[0], "Col_" + part.name + "_0")
                    else:
                        collider_data = ""
                        coll_count = 0
                        for coll_geo in current_collider.geometry:
                            collider_data += MeshToString(current_collider.geometry[coll_count], "Col_" + part.name + "_" + str(coll_count))
                            coll_count += 1
                        part_dict["Collider"] = collider_data
                else:
                    current_collider.Transform(center_transform)
                    part_dict["Collider"] = MeshToString(current_collider, "Col_" + part.name + "_0")
            
            part_dict["TemplateID"] = part_count
            part_count += 1
            
            parts_data.append(part_dict)
        
        data_dict["PartData"] = parts_data
        
        rules_data = []
        for rule in rules:
            rule_dict = {}
            
            rule_dict["Part1"] = rule.part1
            rule_dict["Conn1"] = rule.conn1
            rule_dict["Part2"] = rule.part2
            rule_dict["Conn2"] = rule.conn2
            
            rules_data.append(rule_dict)
        
        data_dict["RuleData"] = rules_data
        
        groups_data = []
        for group in rule_groups:
            group_dict = json.loads(group)
            groups_data.append(group_dict)
            
        data_dict["RuleGroupsData"] = groups_data
        
        
        add_geo_data = []
        add_geo_count = 0
        for add_geo in additional_geometry:
            add_geo_dict = {}
            
            add_geo_dict["Geometry"] = MeshToString(add_geo, "Additional_" + str(add_geo_count))
            add_geo_count += 1
            
            add_geo_data.append(add_geo_dict)
        
        data_dict["AdditionalGeometry"] = add_geo_data
        
        
        full_path = filepath + "\\" + filename + ".json"
        
        if save:
            with open(full_path, "w") as outF:
                json.dump(data_dict, outF)
        
        return json.dumps(data_dict), full_path
    else:
        return -1


result = main(PART, RULES, RULE_G, COLL, PROB, ADD_GEO, PATH, NAME, SAVE)

if result != -1:
    TXT = result[0]
    FILE = result[1]