from pickle import *
import os
import numpy as np

GLOBAL_PATH = '/na/gpfs1/ARCHIWUM/ASzczepan/predictor-corrector-frosts'

#TODO zrobić pickle z metadanymi tzn. header w którym bedą podstawowe informacje odnośnie danych zawierających co jest w środku
#TODO UM - anticipation, parametr, stashcode,
#TODO IMGW - określenie zbioru danych obserwacyjnych - w header tylko identyfikator zbioru danych a w oddzielnym pliku zbiór danych interpolowanych jakim interpolarotem z jakiej biblioteki z jakimi parametrami.


def params2filepath(model, y, m, param_brief, my_cwd, anticipation=0):
    if model == "um":
        filename = "{0}_{1}_{2}_{3}_anticipation{4}h.pkl".format(model, str(y), str(m),\
               param_brief.replace(".", "p").replace(" ", "-"), anticipation)
        filepath = os.path.join(my_cwd, param_brief.replace(".", "p").replace(" ", "-"), str(y), str(m), filename)
        #filename = "{0}_{1}_{2}_{3}.pkl".format(model, str(y), str(m), param_brief.replace(".", "p").replace(" ", "-"))
        #filepath = os.path.join(my_cwd, param_brief.replace(".", "p").replace(" ", "-"), str(y), str(m), filename)
    elif model == "imgw":
        filename = "{0}_{1}_{2}_{3}.pkl".format(model, str(y), str(m), param_brief.replace(".", "p").replace(" ", "-"))
        filepath = os.path.join(my_cwd, param_brief.replace(".", "p").replace(" ", "-"), str(y), str(m), filename)
    else:
        pass

    return filepath


def put_pickle(spacetime, model, parameter, YEAR, MONTH, anticipation=0):

    y, m = YEAR, MONTH
    if model=='um':
        from tests.test_get_um import um_code2description
        param_brief = str(um_code2description(parameter))
    elif model=='imgw':
        from tests.test_get_imgw import imgw_code2description
        param_brief = str(imgw_code2description(parameter))
    else:
        param_prief = 'false'

    my_cwd = "/na/gpfs1/ARCHIWUM/ASzczepan/predictor-corrector-frosts/pickles_datas"
    filepath = params2filepath(model, y, m, param_brief, my_cwd, anticipation=anticipation)
    file = open(filepath, "wb")
    dump(spacetime, file)

    print("{} datas with shape {} are HERE: {}".format(model, np.array(spacetime.shape), filepath))


def filter_data(data, DAY, HOUR):
    if isinstance(DAY, int) and isinstance(HOUR, int):
        return data[DAY-1][HOUR]
    elif isinstance(DAY, list) and isinstance(HOUR, list):
        data = np.array(data)
        return data[DAY[0]-1:DAY[-1]+1-1, HOUR[0]:HOUR[-1]+1]
    else:
        #TODO insert exception !!! !!!
        return "not implemented"



def get_pickle(model, parameter,  y, m, DAY=None, HOUR=None, anticipation=0):
    my_cwd = "/na/gpfs1/ARCHIWUM/ASzczepan/predictor-corrector-frosts/pickles_datas"

    if model=='um':
        from get_um import um_code2description
        param_brief = str(um_code2description(parameter))
    elif model=='imgw':
        from tests.test_get_imgw import imgw_code2description
        param_brief = str(imgw_code2description(parameter))
    else:
        #throw exception !!!!! !!!!!
        param_brief = 'false'

    filepath = params2filepath(model, y, m, param_brief, my_cwd, anticipation=anticipation)
    file = open(str(filepath), "rb")
    data = np.array(load(file))
    file.close()

    if DAY==None and HOUR==None:
        return data
    else:
        #TODO ze względu na paradygmaty programowania powinniśmy zachować "shape"
        #TODO UWAGA !!!! !!!! to zadziała tylko przy założeniu że mam cały miesiąc załadowany do pliku
        return filter_data(data, DAY, HOUR)




