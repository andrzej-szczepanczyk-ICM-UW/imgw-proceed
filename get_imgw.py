#!/opt/miniconda37/bin/python
import os, sys, json
import numpy as np
import csv
from datetime import datetime, timedelta
import pandas as pd
from coords_manager import *


"""
imgw parameters - it is exatly number of column from special file
"""
#IMGW codes
#29	air temperature
#77	ground temperature 5 m
#79	ground temperature 10 m
#37	relative humidity
code_imgw_air_temp = 29
code_imgw_ground_temp_5 = 77
code_imgw_ground_temp_10 = 79
code_imgw_rel_hum = 37

"""
list of cities for particular visualisation - this is a of list of synoptic imgw stations - polish notation
"""
#malgosia_list = ["KOŁOBRZEG-DŹWIRZYNO",  "ŁEBA", "LĘBORK", "GDAŃSK", "ELBLĄG", "KĘTRZYN",\
#                 "SUWAŁKI", "TORUŃ", "CZĘSTOCHOWA", "KATOWICE", "KRAKÓW", "SANDOMIERZ",\
#                 "BIELSKO-BIAŁA", "ZAMOŚĆ", "ZAKOPANE", "KASPROWY WIERCH"]

"""
list of cities for particular visualisation - this is a of list of synoptic imgw stations - simplified notation
"""
malgosia_list = ["KOLOBRZEG", "KOLOBRZEG-DZWIRZYNO",  "LEBA", "LEBORK", "GDANSK-SWIBNO", "ELBLAG", "KETRZYN",\
                 "SUWALKI", "TORUN", "CZESTOCHOWA", "KATOWICE", "KRAKOW", "SANDOMIERZ",\
                 "BIELSKO-BIALA", "JELENIA GORA", "KASPROWY WIERCH", "SWINOUJSCIE", "SNIEZKA"]


'''
from stacje_meteorologiczne.csv 
load meteorologic stations. return as dataframe
'''
def load_imgw_coordinates_station():
    """
    load coordinates of stations from stacje_meteorologiczne.csv
    :param filter: filter set of imgw stations
    :param labels: Return labels - names of cities or not.
    :return: DataFrame
    """
    path = GLOBAL_PATH+"/dane_imgw/stacje_meteorologiczne.csv"
    dataframe = pd.read_csv(path, encoding='utf-8', low_memory=False, header=None)

    dataframe[0] = dataframe[0].astype(str)
    dataframe[3] = dataframe[3].astype(float)/10000
    dataframe[2] = dataframe[2].astype(float)/10000
    return dataframe


'''
load weather data from concrete moment time (exactly one hour) as a Pandas DataFrame
convert this DataFrame to Tuple
:param year:
:param month:
:param day:
:param hour:
:param parameter: parameter code accordingly with number of column in csv file
:param latlon_form: True-latlon, False-rowcol form
:return: tuple with 3 arrays,  [lat, lon] and value
'''
def load_imgw_data(year, month, day, hour, parameter):

    path = GLOBAL_PATH+"/dane_imgw/"+str(year)
    namefiles = os.listdir(path)
    namefiles.sort()
    direct_paths = [os.path.join(path, namefile) for namefile in namefiles]

    big_frame = pd.DataFrame()
    for f, namefile in zip(direct_paths, namefiles):
        dataframe = pd.read_csv(f, encoding='latin', low_memory=False, header=None)
        dataframe_f = dataframe[(dataframe[2] == year) & (dataframe[3] == month) & (dataframe[4] == day) & (dataframe[5] == hour)]
        big_frame = big_frame.append(dataframe_f)

    big_frame[0] = big_frame[0].astype(str)
    cut_big_frame = big_frame[[0, parameter]]

    coordinates_array = load_imgw_coordinates_station()
    result = cut_big_frame.set_index(0).join(coordinates_array.set_index(0), lsuffix='_caller', rsuffix='_other')

    lat = np.array(result[2].values.tolist())
    lon = np.array(result[3].values.tolist())

    val = np.array(result[parameter].values.tolist())
    return lat, lon, val

def load_imgw_pl_stations(filter=False):
    path = GLOBAL_PATH+'/dane_imgw/pl_stacje.csv'
    dataframe = pd.read_csv(path, encoding='utf-8', low_memory=False, delimiter=";")
    if filter is True:
        dataframe = dataframe[np.isin(dataframe['stname'], malgosia_list)]

    return dataframe['lon'], dataframe['lat'], dataframe['stname']

'''
load a sequence map of imgw data in rowcol Poland representation
'''
def load_sequence_map(start, param=code_imgw_air_temp, forecast_hour_len=48):
    spacetime = np.full((forecast_hour_len, Poland.xlen, Poland.ylen), 0.0)
    for it in range(forecast_hour_len):
        n = start+timedelta(hours=it)
        spacetime[it] = load_imgw_single(n.year, n.month, n.day, n.hour, param=param)
        print("y={} m={} d={} H={} loaded".format(n.year, n.month, n.day, n.hour))
    return spacetime





'''
load a series for concrete localisation in rowcol Poland way
'''
def get_one_series(spacetime, rowcol):
    return spacetime[:, rowcol[0], rowcol[1]].flatten()

'''
make a map of weather parameter in a based of a IMGW synoptic stations
'''
def load_imgw_single(YEAR, MONTH, DAY, HOUR, param=code_imgw_air_temp):
    lat_imgw, lon_imgw, nointerpolated_value_imgw = load_imgw_data(YEAR, MONTH, DAY, HOUR, param)
    row_imgw, col_imgw = latlon2rowcol(lat_imgw, lon_imgw)
    from scipy.interpolate import Rbf
    rbf = Rbf(row_imgw, col_imgw, nointerpolated_value_imgw, epsilon=0.02)
    tiy = np.linspace(Poland.xmin, Poland.xmax, Poland.xlen)
    tix = np.linspace(Poland.ymin, Poland.ymax, Poland.ylen)
    YI, XI = np.meshgrid(tix, tiy)
    interpolated_value_imgw = rbf(XI, YI)
    return  np.array(interpolated_value_imgw)

