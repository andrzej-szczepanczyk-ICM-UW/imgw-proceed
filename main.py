from get_imgw import *
from pickle_database import *
from plots import *
import matplotlib.cm as cm
from datetime import datetime

# DEMOS:::::
# EXAMPLES OF USAGE

YEAR, MONTH, DAY, HOUR = (2017, 3, 12, 9)
map = load_imgw_single(YEAR, MONTH, DAY, HOUR, code_imgw_air_temp)
print(map)

# visualise datas
title = r'$\bf{IMGW}$' + ' Poland map at {0}\nair temperature'.format(
   datetime(YEAR, MONTH, DAY, HOUR).strftime("%Y/%m/%dT%H"))
min, max = -8, 8
visualise_rowcol_map(map, title, "temperatura", cm.brg, min, max)

#load 4h sequence of datas
node = globalrowcol2namedtuplerowcol((282, 264), Poland)
spacetime = load_sequence_map(datetime(YEAR, MONTH, DAY, HOUR), param=code_imgw_air_temp, forecast_hour_len=4)
series = get_one_series(spacetime, node)
print(series)

#LOAD wrzesień 2019
spacetime = load_sequence_map(datetime(2019, 9, 1, 0), param=code_imgw_air_temp, forecast_hour_len=30*24)


mask = pickle2mask()
from matplotlib.pyplot import imshow
print(mask)
#dont't worry if it looks reversed - it is good !!
imshow(mask)




