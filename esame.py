class ExamException(Exception):
    pass


class CSVTimeSeriesFile():
    
    def __init__(self, name):
        self.name = name
        
    def get_data(self):
        lista = []
        last_time = -1
        try:
            
            #Controllo se il file esiste e successivamente controllo se riesco a leggere il file
            file = open(self.name, 'r')
            file.read()
            file.close()
        except:
            
            raise ExamException("Errore nell'apertura del file")
        file = open(self.name, 'r')
        for line in file:
            
            tmp = line.split(',')
            try:
                
                #Controllo se riesco a convertire i valori del csv, se non si riesce a convertirli allora li salto
                lista.append([int(float(tmp[0])), float(tmp[1])])
            except:
                
                continue
            if  last_time >= int(float(tmp[0])):
                #Controllo se ci sono dati inseriti male temporalmente
                raise ExamException("Errore, dati inseriti male")
            last_time = int(float(tmp[0]))
        file.close()
        return lista


def compute_daily_max_difference(time_series):
    if len(time_series) == 0:
        return []
    current_day = time_series[0][0] - (time_series[0][0] % 86400)
    list=[]
    valori_finali = []
    for line in time_series:
        if (line[0] - (line[0] % 86400)) == current_day:
            #Tutti i numeri che vengono inseriti in questa lista appartengono alla stessa giornata
            list.append(line[1])
        else:
            #Se si cambia la giornata, dico qual è la nuova giornata e poi calcolo la differenza massima
            current_day = line[0] - (line[0] % 86400)
            if len(list) == 1:
                #Se esiste solo una misurazione per quella giornata allora non si può calcolare la differenza massima
                valori_finali.append(None)
            else:
                valori_finali.append(max(list) - min(list))
            #Devo aggiungere il nuovo elemento della giornata
            list = [line[1]]
    #Devo calcolare la differenza massima dell'ultima giornata
    if len(list) == 1:
        valori_finali.append(None)
    else:
        valori_finali.append(max(list) - min(list))
    return valori_finali