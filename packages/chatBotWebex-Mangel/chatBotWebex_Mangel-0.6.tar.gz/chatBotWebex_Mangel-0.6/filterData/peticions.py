import requests
import json
from datetime import datetime


class Peticions :

    #metodo encargado de consumir el endpoint getEdge de Velocloud
    def getEdge(edgeID, url, token):

        payload = {"id": edgeID}
        header = {'Content-Type': 'application/json',
                'Authorization': token}
        response = requests.post(url + 'edge/getEdge', data=json.dumps(payload), headers=header)

        if response.status_code == 200:
            result = response.json()
            return result 


    #metodo encargado de consumir el endpoint getEdgeLinkMetrics de Velocloud
    def getEdgeLinkMetrics(edgeID, url, token, date= datetime.now().isoformat()+'Z'):

        print(date)

        payload = {
            "id": edgeID,
            "interval": {
                "start": date
            }
        }
        header = {'Content-Type': 'application/json',
                'Authorization': token}
        response = requests.post(url + 'metrics/getEdgeLinkMetrics', data=json.dumps(payload), headers=header)

        if response.status_code == 200:
            result = response.json()
            return result


    #metodo encargado de consumir el endpoint getEdgeAppLinkSeries de Velocloud
    def getEdgeAppLinkSeries(edgeID, url, token, date= datetime.now().isoformat()+'Z'):

        payload = {
            "id": edgeID,
            "interval": {
                "start":  date
            }
        }
        header = {'Content-Type': 'application/json',
                'Authorization': token}
        response = requests.post(url + 'metrics/getEdgeAppLinkSeries', data=json.dumps(payload), headers=header)

        if response.status_code == 200:
            result = response.json()
            return result

    #metodo para testear la instalación del package
    def test(number):
        print(number)