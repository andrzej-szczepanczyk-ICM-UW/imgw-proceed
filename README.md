The documentation in html and rst still doesn't working. The authors of this module puts all efforts to complete this one.

**INTRODUCTION: (koniecznie to przeczytaj !!!!)**

we have few representations ways for nodes localisation

(lat, lon) for UM 'grid nodes' - actually, temporally in c_grid/5_pgrid

(row, col) for whole area (globalrowcol) - size (616, 448)

(row, col) only for Polands see below - size (165, 175) the most frequent presentation in these modules (namedtuplerowcol).

More details in *coords_manager.py* under Poland - bound variable namedtuple type


**DEMO EXAMPLE**
W pliku demo.py prezentuję przykład użycia funkcji. Jeżeli pobierzesz projekt i to Jeżeli chciesz użyć funkcji w innym skrypcie python
to musisz funkcje importować w taki sam sposób jak w demo.py i w tym samym miejscu co demo.py w celu uniknięcia błędów importowania.


najczęstrza forma przedstawienia daty to YEAR, MONTH, DAY, HOUR tzn 4 zmienne typu integer

parametry pogodowe w formie "constant integer" reprezentują parametr pogodowy. Wyróżnione są najczęściej używane:
*code_imgw_air_temp = 29*

*code_imgw_ground_temp_5 = 77*

*code_imgw_ground_temp_10 = 79*

*code_imgw_rel_hum = 37*

Konkretna wartość dla parametru zależy od numeru kolumny w plikach, których dokładniejszy opis znajduje się tutaj:
https://dane.imgw.pl/data/dane_pomiarowo_obserwacyjne/dane_meteorologiczne/terminowe/synop/s_t_format.txt

**zawartość katalogów**

*dane imgw/2019*

pomiary ze stacji synoptycznych (jeżeli brakuje danychto można je dociągnąć z https://dane.imgw.pl/data/dane_pomiarowo_obserwacyjne/dane_meteorologiczne/terminowe/synop/)

*dane imgw/*.csv*

lokalizacje stacji synoptycznych 

*nuts*

pliki służące do wycinania maski polski i nie tylko! Jeżeli brakuje plików należy je ściągnąć stąd:

https://ec.europa.eu/eurostat/web/gisco/geodata/reference-data/administrative-units-statistical-units/nuts 

**OPIS FUNKCJI: użytych w demo.py**

**---load and transform---**

*get_imgw.py:*
**load_imgw_single(int:YEAR, int:MONTH, int:DAY, int:HOUR, int:weather_feature)**

Załaduj 2-wymiarową mapę parametru pogodowego (weather feature) w reprezentacji (row, col) dla Polski.
Zostało to otrzymane na podstawie interpolacji danych ze stacji synoptycznych za pomocą interpolatora scipy.interpolate.Rbf (radial basis function)
Wartość zwracana to tablica dwuwymiarowa


*coords_manager.py*
**globalrowcol2namedtuplerowcol(tuple:(row, col), namedtuple:Poland)**

funkcja konwertuje reprezentację global (row, col) na reprezentację (row, col) dla Polski

*get_imgw.py:*
**load_sequence_map(datetime:start, param=code_imgw_air_temp, forecast_hour_len)**

funkcja ładująca sekwencję danych dla każdego węzła siatki w reprezentacji Poland (row, col)
start - *type datetime* - początek sekwencji
param - *type const int* - parametr pogodowy
forecast_hour_len - *type int* - długość sekwencji
funkcja zwraca tablicę 3-wymiarową.


*get_imgw.py*
**get_one_series(spacetime, node)**

funkcja wyciągająca z funkcji  *load_sequence_map* serię danych dla konkretnego węzła siatki w reprezentacji Poland (row, col)
*spacetime* - tablica 3-wymiarowa wygenerowana przez *load_sequence_map*
*node* - tuple reprezentujące węzeł siatki według numerowania Poland nametuple
funkcja zwraca tablicę danych




**---visualisation---**

*plots.py*
**make_mask(my_bounds)**

funkcja tworząca maskę danych 
my_bounds - *type namedtuple bounds* - jakie dokładnie wycięcie potrzebuję zrobić - njczęściej będzie to Polska
ta funkcja używa danych z eurostatu plików tzw. "nuts" i używam biblioteki geopandas 




*plots.py*
**visualise_rowcol_map(map, title, str:y_label_name, cm.brg, min, max)**

Funkcja wizualizująca dane zinterpolowane dane IMGW dla całej powierzchni Polski.
map




