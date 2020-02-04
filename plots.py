#!/opt/miniconda37/bin/python
import matplotlib.pyplot as plt
from get_imgw import *
from coords_manager import *
from pickle import load

GLOBAL_PATH = '/na/gpfs1/ARCHIWUM/ASzczepan/predictor-corrector-frosts'

#TODO do poprawienia
mask=None

def pickle2mask():
    metadane, mask = load(open("Poland_mask.pkl", 'rb'))
    return mask

#### VISUALISATION PART ####
def visualise_rowcol_map(statistical_space, title, y_label_name, cmp, min, max):

    x_corner, y_corner = Poland.xmin, Poland.ymin
    LATgrid, LONgrid = get_latlons_ver2(statistical_space, x_corner, y_corner)

    ss = flat_array(statistical_space)

    plt.rcParams.update({'font.weight': 'bold', 'font.size': 10.0, 'axes.titlesize': 14})
    plt.xlabel("longitude")
    plt.ylabel("latitude")

    plt.title(str(title), size='xx-large')

    my_norm = plt.Normalize(min, max)
    my_linspace_levels = np.linspace(min, max, num=max-min+1)
    my_linspace_func = np.linspace(min, max, num=5*(max-min)+1)
    FUNC = plt.contourf(LATgrid, LONgrid, statistical_space, norm=my_norm, cmap=cmp, levels=my_linspace_func)
    LEVELS = plt.contour(FUNC, norm=my_norm, levels=my_linspace_levels, colors='g')

    cbar = plt.colorbar(FUNC, norm=my_norm, extend='both')
    cbar.ax.set_ylabel(y_label_name)
    cbar.add_lines(LEVELS)

    all_lat_stations, all_lon_stations, labels = load_imgw_pl_stations()
    lat_stations, lon_stations, labels = load_imgw_pl_stations(filter=True)
    plt.scatter(all_lat_stations, all_lon_stations, color="black", marker="+", s=8)
    for lat, lon, label in zip(lat_stations, lon_stations, labels):
        plt.text(lat+0.1, lon-0.1, label, color="black", fontsize=6)

    plt.show()
    plt.clf()



def visualise_pickle2mask():
    x_corner, y_corner = Poland.xmin, Poland.ymin
    mask = pickle2mask()
    lat, lon = get_latlons(mask, x_corner, y_corner)
    LATgrid, LONgrid = get_latlons_ver2(mask, x_corner, y_corner)
    FUNC = plt.contourf(LATgrid, LONgrid, mask)
    plt.show()