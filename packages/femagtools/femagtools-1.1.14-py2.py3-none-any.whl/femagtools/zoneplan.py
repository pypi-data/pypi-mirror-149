from xml.etree import ElementTree as ET
import numpy as np

colors = {
    1: "lime",
    2: "magenta",
    3: "gold",
}
Q = 90
p = 12
m = 3

t = np.gcd(Q, p)
Qb = Q//t
pb = 0//t
width = Qb*10

filename = 'zoneplan.svg'
svg = ET.Element("svg", dict(
    xmlns="http://www.w3.org/2000/svg", viewBox=f"0 -10 {width} 10"))
for i in range(Qb):
    ET.SubElement(svg, "rect", {
        "x": f"{i*10}",
        "y": "-10",
        "width": "10",
        "height": f"20"
    })
ET.ElementTree(svg).write(filename)
