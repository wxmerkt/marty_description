import xml.etree.cElementTree as ET
from xml.etree.ElementTree import Element
import trimesh

urdf = ET.ElementTree(file="urdf/marty.urdf")
root = urdf.getroot()

# Real face+base mass is 79g, i.e. density should be 1190.6894469897379 = 1190.69
density = 1190.69

for link in root.iter("link"):
    mesh_node = link.find("visual/geometry/mesh")
    filename = mesh_node.get("filename").replace("package://marty_description/", "")
    mesh = trimesh.load_mesh(filename)
    mass = mesh.mass_properties()['mass'] * density
    inertia = mesh.moment_inertia * density
    ixx = inertia[0,0]
    ixy = inertia[0,1]
    ixz = inertia[0,2]
    iyy = inertia[1,1]
    iyz = inertia[1,2]
    izz = inertia[2,2]
    inertial_tag = ET.fromstring('<inertial><mass value="' + str(mass) +
                                         '"/><inertia ixx="'+str(ixx)+'" ixy="'+str(ixy)+'" ixz="'+str(ixz) +
                                         '" iyy="'+str(iyy)+'" iyz="'+str(iyz)+'" izz="'+str(izz)+'"/></inertial>')
    link.append(inertial_tag)

urdf.write('urdf/marty_with_inertials.urdf')