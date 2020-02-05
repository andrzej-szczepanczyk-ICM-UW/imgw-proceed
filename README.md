The documentation in html and rst still doesn't working. The authors of this module puts all efforts to complete this one.

**INTRODUCTION: (koniecznie to przeczytaj !!!!)**
we have few representations ways for nodes localisation
(lat, lon) for UM 'grid nodes' - actually, temporally in c_grid/5_pgrid
(row, col) for whole area (globalrowcol) - size (616, 448)
(row, col) only for Polands see below - size (165, 175) the most frequent presentation in these modules (namedtuplerowcol).
More details in coords_manager.py under Poland - bound variable namedtuple type

najczęstrza forma przedstawienia daty to YEAR, MONTH, DAY, HOUR tzn 4 zmienne typu integer

parametry pogodowe w formie "constant integer" reprezentują parametr pogodowy. Wyróżnione są najczęściej używane:
code_imgw_air_temp = 29
code_imgw_ground_temp_5 = 77
code_imgw_ground_temp_10 = 79
code_imgw_rel_hum = 37
Konkretna wartość dla parametru zależy od numeru kolumny w plikach, których dokładniejszy opis znajduje się tutaj:
https://dane.imgw.pl/data/dane_pomiarowo_obserwacyjne/dane_meteorologiczne/terminowe/synop/s_t_format.txt


**OPIS FUNKCJI:**

Załaduj 2-wymiarową mapę parametru pogodowego (weather feature) w reprezentacji (row, col) dla Polski.
Zostało to otrzymane na podstawie interpolacji danych ze stacji synoptycznych za pomocą interpolatora scipy.interpolate.Rbf (radial basis function)
Wartość zwracana to tablica dwuwymiarowa

**load_imgw_single(int:YEAR, int:MONTH, int:DAY, int:HOUR, int:weather_feature)**


funkcja konwertuje reprezentację global (row, col) na reprezentację (row, col) dla Polski

**globalrowcol2namedtuplerowcol(tuple:(row, col), namedtuple:Poland)**


funkcja ładująca sekwencję danych dla każdego węzła siatki w reprezentacji Poland (row, col)
start - *type datetime* - początek sekwencji
param - *type const int* - parametr pogodowy
forecast_hour_len - *type int* - długość sekwencji
funkcja zwraca tablicę 3-wymiarową.

**load_sequence_map(datetime:start, param=code_imgw_air_temp, forecast_hour_len)**


funkcja wyciągająca z funkcji  *load_sequence_map* serię danych dla konkretnego węzła siatki w reprezentacji Poland (row, col)
spacetime - tablica 3-wymiarowa wygenerowana przez *load_sequence_map*
node - tuple reprezentujące węzeł siatki według numerowania Poland nametuple
funkcja zwraca tablicę danych

**get_one_series(spacetime, node)**


**visualisation parts**


funkcja tworząca maskę danych 
my_bounds - *type namedtuple bounds* - jakie dokładnie wycięcie potrzebuję zrobić - njczęściej będzie to Polska
ta funkcja używa danych z eurostatu plików tzw. "nuts" i używam biblioteki geopandas 

**make_mask(my_bounds)**

Funkcja wizualizująca dane zinterpolowane dane IMGW dla całej powierzchni Polski.
map - ta
**visualise_rowcol_map(map, title, "temperatura", cm.brg, min, max)**

**DEMO EXAMPLE**



