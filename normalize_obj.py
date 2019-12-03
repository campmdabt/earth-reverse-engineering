import sys
import math
import numpy as np
from pathlib import Path
from tqdm import tqdm

lat = math.radians(float(sys.argv[1]))
lon = math.radians(float(sys.argv[2]))

sin_lat = math.sin(lat)
cos_lat = math.cos(lat)
sin_lon = math.sin(lon)
cos_lon = math.cos(lon)

earth_radius = 6378137
T = np.array([cos_lat * cos_lon, cos_lat * sin_lon, sin_lat]) * earth_radius
Rz = np.array([[cos_lon, sin_lon, 0], [-sin_lon, cos_lon, 0], [0, 0, 1]])
Ry = np.array([[cos_lat, 0, sin_lat], [0, 1, 0], [-sin_lat, 0, cos_lat]])
R = Ry @ Rz

input_file = Path(sys.argv[3])
output_file = input_file.with_name(input_file.stem + '.2.obj')

with input_file.open() as in_, output_file.open('w') as out:
    for line in tqdm(in_):
        if line.startswith("v "):
            vertex = np.fromstring(line[2:], sep=' ')
            vertex = R @ (vertex - T)
            line = "v {} {} {}\n".format(*vertex)

        out.write(line)
