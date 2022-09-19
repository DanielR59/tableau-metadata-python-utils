from typing_extensions import Literal
import requests
import xmltodict
import tableauserverclient as TSC
from .exceptions.errores import DatabaseNameNotFound, LoginError, SiteNameError



class myTableauApi:
    def __init__(
        self,
        server_url: str,
        personalAccessTokenName: str,
        personalAccessTokenSecret: str,
        site_name: str,
        api_version: str,
    ) -> None:

        # ? Agregar funcion para actualizar el token de acceso temporal?
        # TODO: Cambiar el mensaje mamalon xd
        self.server_url = server_url
        self.api_version = api_version
        self.__default_message = "Mensaje super mamalon ultra fantastico"
        if self.server_url.endswith("/"):
            self.endpoint = self.server_url + f"api/{self.api_version}"
        else:
            self.endpoint = self.server_url + f"/api/{self.api_version}"
        self.__personalAccessTokenName = personalAccessTokenName
        self.__personalAccessTokenSecret = personalAccessTokenSecret
        self.site_name = site_name

        self.temp_token = self.__login(
            endpoint=self.endpoint,
            personalAccessTokenName=self.__personalAccessTokenName,
            personalAccessTokenSecret=self.__personalAccessTokenSecret,
            site_name=self.site_name,
        )

        self.__tableau_auth = TSC.PersonalAccessTokenAuth(
            token_name=personalAccessTokenName,
            personal_access_token=personalAccessTokenSecret,
            site_id=site_name,
        )
        self.__server = TSC.Server(self.server_url, use_server_version=True)

        self.site_luid = self._getsite_luid(
            site_name=self.site_name,
        )

    def __login(
        self,
        endpoint: str,
        personalAccessTokenName: str,
        personalAccessTokenSecret: str,
        site_name: str,
    ) -> str:

        # ? Mantener privado?

        if endpoint.endswith("/"):
            endpoint += "auth/signin"
        else:
            endpoint += "/auth/signin"

        headerList = {
            "Accept": "*/*",
            "Content-Type": "application/xml",
        }

        payload = f"""<tsRequest>	<credentials	 personalAccessTokenName="{personalAccessTokenName}" personalAccessTokenSecret="{personalAccessTokenSecret}" >		<site contentUrl="{site_name}" />	</credentials></tsRequest>"""

        response = requests.request("POST", endpoint, headers=headerList, data=payload)

        if response.ok:
            respuesta = xmltodict.parse(response.text)
            return respuesta["tsResponse"]["credentials"]["@token"]

        else:
            raise LoginError

    def _getsite_luid(
        self,
        site_name: str,
    ) -> str:

        # ? Metodo privado?

        with self.__server.auth.sign_in(self.__tableau_auth):

            query = self.__server.metadata.query(
                """
            query siteid {
    	tableauSites{
  	
            name
            luid
        }
        }
            
            """
            )

            for element in query["data"]["tableauSites"]:
                if (
                    element["name"] == site_name
                    or element["name"].replace(" ", "").lower() == site_name
                ):

                    luid = element["luid"]
                    print(luid)
                    return luid

            else:
                raise SiteNameError

    def get_database_luid(self, database_name: str) -> str:
        # TODO: Agregar un metodo para cuando haya 0 coincidencias devolver sugerencias de nombres
        # TODO: Agregar una exepcion cuando encuentre mas de una coincidencia

        with self.__server.auth.sign_in(self.__tableau_auth):

            query = self.__server.metadata.query(
                """
            query hola {

                databases{
                    name 
                    luid
            
                }
            }
            """
            )
        databases = [a_dict["name"] for a_dict in query["data"]["databases"]]
        luids = [a_dict["luid"] for a_dict in query["data"]["databases"]]

        coincidences = 0
        for name in databases:
            if name == database_name:
                coincidences += 1

        if coincidences == 0:
            print("No encontre la base cainal uwu")
            raise DatabaseNameNotFound
        elif coincidences == 1:
            index = databases.index(database_name)
            return luids[index]

        elif coincidences > 1:

            print(
                "Hay mas de una coincidencia cainal, por favor especifica el luid de la base que buscas"
            )
            return None

    def get_database_tables(self, database_name: str, database_luid: str = None) -> str:

        # TODO: refactor
        # TODO: Terminar este pedo
        with self.__server.auth.sign_in(self.__tableau_auth):

            if database_luid:

                query = self.__server.metadata.query(
                    'query hola {databases(filter : {luid : "'
                    + database_luid
                    + """ "}){

                        tables{
                            name
                            luid
                        }
                    }

                    """
                )

            else:

                query = self.__server.metadata.query(
                    """
                query hola {

                    databases{
                        name 
                        luid
                
                    }
                }
                """
                )
            databases = [a_dict["name"] for a_dict in query["data"]["databases"]]
            luids = [a_dict["luid"] for a_dict in query["data"]["databases"]]

            coincidences = 0
            for name in databases:
                if name == database_name:
                    coincidences += 1

            if coincidences == 0:
                print("No encontre la base cainal uwu")
                return None
            elif coincidences == 1:
                index = databases.index(database_name)
                return luids[index]

            elif coincidences > 2:

                print(
                    "Hay mas de una coincidencia cainal, por favor especifica el luid de la base que buscas"
                )
                return None

    def _get_table_columns_luid(self):
        pass

    def set_database_quality_warning(
        self,
        database_name: str,
        database_luid: str = None,
        message: str = None,
        quality_warning_type: Literal[
            "DEPRECATED", "WARNING", "STALE", "SENSITIVE_DATA", "MAINTENANCE"
        ] = "MAINTENANCE",
        isActive: bool = True,
        isSevere: bool = True,
    ):

        # TODO: Agregar excepciones cuando se corra el metodo mas de una vez seguida

        if message:
            pass
        else:
            message = self.__default_message

        headersList = {
            "Accept": "*/*",
            "Content-Type": "application/xml",
            "X-Tableau-Auth": f"{self.temp_token}",
        }

        payload = f"""<tsRequest>\n	<dataQualityWarning type="{quality_warning_type}" isActive="{str(isActive).lower()}" message="{message}" isSevere="{str(isSevere).lower()}"/>\n</tsRequest>"""

        if database_luid:

            reqUrl = f"{self.endpoint}/api/{self.api_version}/sites/{self.site_luid}/dataQualityWarnings/database/{database_luid}"
            response = requests.request(
                "POST", reqUrl, data=payload, headers=headersList
            )
            print(response.ok)

        else:

            database_luid = self.get_database_luid(database_name=database_name)

            reqUrl = f"{self.endpoint}/api/{self.api_version}/sites/{self.site_luid}/dataQualityWarnings/database/{database_luid}"
            response = requests.request(
                "POST", reqUrl, data=payload, headers=headersList
            )

            print(response.ok)

    def delete_database_quality_warning(
        self, database_name: str, database_luid: str = None
    ) -> None:

        # TODO: Agregar excepciones cuando se corra el metodo mas de una vez seguida

        headersList = {
            "Accept": "*/*",
            "X-Tableau-Auth": f"{self.temp_token}",
        }

        payload = ""

        if database_luid:

            reqUrl = f"{self.endpoint}/api/{self.api_version}/sites/{self.site_luid}/dataQualityWarnings/database/{database_luid}"
            response = requests.request(
                "DELETE", reqUrl, data=payload, headers=headersList
            )
            print(response.ok)

        else:

            database_luid = self.get_database_luid(database_name=database_name)

            reqUrl = f"{self.endpoint}/api/{self.api_version}/sites/{self.site_luid}/dataQualityWarnings/database/{database_luid}"
            response = requests.request(
                "DELETE", reqUrl, data=payload, headers=headersList
            )

            print(response.ok)
