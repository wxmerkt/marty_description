import xml.etree.cElementTree as ET
import copy

urdf = ET.ElementTree(file="marty.urdf")
root = urdf.getroot()

for link in root.iter("link"):
    visual = link.find("visual")
    collision = copy.deepcopy(visual)
    collision.tag = 'collision'
    link.append(collision)

urdf.write("marty_with_collision.urdf")