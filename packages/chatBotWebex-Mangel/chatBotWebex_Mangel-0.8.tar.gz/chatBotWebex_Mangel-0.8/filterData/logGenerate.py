import logging
import os


class logGenerate():

    # Se encarga de validar y crear el log como de agregar el dato requerido.
    def setLogHistory(logName, command, data, adicionalData="", folderName="history"):
        logging.basicConfig(filename=os.getcwd()+'/'+folderName+"/" +
                            logName+'.log', level="INFO", format="%(asctime)s - %(message)s")
        logging.info(command + " - " + data + " - " + adicionalData)

    # Se encarga de indicar dentro del log que se finalizo la historia actual.
    def setFinishLogHistory():
        logging.info("-"*50)