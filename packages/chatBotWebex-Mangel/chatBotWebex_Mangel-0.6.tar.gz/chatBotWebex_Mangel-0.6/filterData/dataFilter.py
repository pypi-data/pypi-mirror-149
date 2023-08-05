import os
import json
import re


class FilterData :
        
        #Se encarga de capturar el archivo Json
        def getJsonSites():
            with open(os.path.join(os.path.dirname(__file__),'..'+ '/SITES_EDGES_BANCOLOMBIA.json') , 'r') as archive:
                data = json.load(archive)
                return data

        #Se encargar crear una lista con el resultado de filtrar por siteTyte
        def filterbySiteType(siteType, data):

            filterdata = [element for element in data if siteType.strip().lower()
                        in element['siteType'].strip().lower()]
            return filterdata


        #Se encarga de generar la tabla de coincidencia a través del dato indicado.
        def filterData(number, data):

            filterList = [element for element in data if re.findall(number + '$', element['siteCode'])
                                                                    or number in element['siteCode']
                                                                    or number in element['siteName'].strip().lower()]

            return filterList


        #Se encarga de buscar el objeto final a través de la tabla de coincidencias en base de la selección indicada por el cliente.
        def getDataSite(selection, siteList):
            
            siteList = list()
            site = ""
            count = 1
            
            for element in siteList:
                if count == int(selection):
                    site = element
                count += 1

            return site

