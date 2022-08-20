from utils import load_keys
from tableaumetadatautils import myTableauApi







keys = load_keys('keys.json')




a = myTableauApi(server_url=keys['SERVER'],personalAccessTokenName=keys['TOKEN_NAME'],personalAccessTokenSecret=keys['TOKEN'],site_name=keys['SITE'], api_version=keys['API_VERSION'])

print(a.temp_token)


# a.get_database_tables("postgres")