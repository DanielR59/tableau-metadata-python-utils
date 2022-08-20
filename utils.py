import json 
import os

def load_keys(filename : str)-> dict:
    """
    Carga de las llaves de configuracion para acceso a TableauServer
    """
    with open(filename,'r') as f:
        return json.load(f)

def load_pendientes_login(filename : str)-> dict:
    """
    Track de los que aun no se han logeado para tomar decision
    """
    if not os.path.exists(filename):
        return {}
    else:
        with open(filename,'r') as f:
            return json.load(f)