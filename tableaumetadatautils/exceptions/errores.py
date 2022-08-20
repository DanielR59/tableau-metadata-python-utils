import os

# TODO: Mejorar las exepciones de los errores
# TODO: Agregar excepciones cuando se hay mas de una coincidencia en la base de datos

class LoginError(Exception):
    """There was an error trying to login, please check your credentials"""
    
    def __str__(self) -> str:
        return "Mamo loguenadose xd"


class SiteNameError(Exception):
    """Al chile no lo encuentro"""

    def __str__(self) -> str:
        return "No encuentra el sitio carnal uwu, reportarlo al github con el nobre pa arreglarlo"
        

class DatabaseNameNotFound(Exception):
    """Pos no encontre la base de datos, intentaré meter coincidencias despues"""

    def __str__(self) -> str:
        return "No encontre el nombre tal cual lo especificaste uwu"