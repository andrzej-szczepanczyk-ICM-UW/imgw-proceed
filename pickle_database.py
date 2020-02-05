from pickle import *
import os
import numpy as np

GLOBAL_PATH = os.getcwd()

#TODO zrobić pickle z metadanymi tzn. header w którym bedą podstawowe informacje odnośnie danych zawierających co jest w środku
#TODO UM - anticipation, parametr, stashcode,
#TODO IMGW - określenie zbioru danych obserwacyjnych - w header tylko identyfikator zbioru danych a w oddzielnym pliku zbiór danych interpolowanych jakim interpolarotem z jakiej biblioteki z jakimi parametrami.


def params2filepath(model, y, m, param_brief, my_cwd):
    if model == "imgw":
        filename = "{0}_{1}_{2}_{3}.pkl".format(model, str(y), str(m), param_brief.replace(".", "p").replace(" ", "-"))
        filepath = os.path.join(my_cwd, param_brief.replace(".", "p").replace(" ", "-"), str(y), str(m), filename)
    else:
        pass

    return filepath

