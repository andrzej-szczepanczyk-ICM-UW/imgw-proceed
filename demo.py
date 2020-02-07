from imgw_proceed.get_imgw import *
from imgw_proceed.plots import *
from imgw_proceed.coords_manager import *
from matplotlib.pyplot import cm

import pickle

# DEMOS:::::
# EXAMPLES OF USAGE
print("test")
YEAR, MONTH, DAY, HOUR = (2019, 3, 12, 9)
map = load_imgw_single(YEAR, MONTH, DAY, HOUR, code_imgw_air_temp)
print(map)

# visualise data
title = r'$\bf{IMGW}$' + ' Poland map at {0}\nair temperature'.format(
   datetime(YEAR, MONTH, DAY, HOUR).strftime("%Y/%m/%dT%H"))
min, max = -8, 8
visualise_rowcol_map(map, title, "temperatura", cm.brg, min, max)

#load 4h sequence of data
node = globalrowcol2namedtuplerowcol((280, 264), Poland)
spacetime = load_sequence_map(datetime(YEAR, MONTH, DAY, HOUR), param=code_imgw_air_temp, forecast_hour_len=4)
series = get_one_series(spacetime, node)
print(series)

#LOAD wrzesień 2019
#this piece of code generates whole september 2019 year
spacetime = load_sequence_map(datetime(2019, 9, 1, 0), param=code_imgw_air_temp, forecast_hour_len=30*24)

#here we have a boolean mask imported from Poland_mask.pkl
mask = pickle2mask()
from matplotlib.pyplot import imshow
#dont't worry if it looks reversed - it is good !!
imshow(mask)




