import requests
from requests.exceptions import HTTPError
import hashlib
from datetime import datetime


#Utilizando la documentación de Marvel tenemos las siguientes variables
# hashPassword = ts+privateKey+publicKey

# public key = d4be8259f3a8e6b9802267349079dce3
PUBLICKEY = 'd4be8259f3a8e6b9802267349079dce3'
# private key = 4cc59a15c1b7b4e1db35b74c19bfb3f7d75ede35
PRIVATEKEY = '4cc59a15c1b7b4e1db35b74c19bfb3f7d75ede35'
# timestamp 
TS = datetime.now()

TS =  round(datetime.timestamp(TS))

URLBASE = 'https://gateway.marvel.com:443/v1/public'

#Se hace el hash de las contraseñas y forma solicitada por el api de Marvel
HASHKEY = hashlib.md5( str(TS).encode("utf-8")+PRIVATEKEY.encode("utf-8")+PUBLICKEY.encode("utf-8"))
HASHKEY = HASHKEY.hexdigest()
#print(HASHKEY)

#Estas llaves estan de manera permanente en todas las peticiones
URLKEYS = f'&ts={TS}&apikey={PUBLICKEY}&hash={HASHKEY}'


def getComics(id):
    try:
        response = requests.get(URLBASE+f'/comics?characters={id}/?limit=100&'+URLKEYS)
        response.raise_for_status()

    except HTTPError as _httperr:
        print(f'HTTP error occurred: {_httperr}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        data = response.json() 
        result = []
        for item in data['data']['results']:
            comic = {
                "id":item['id'],
                "title":item['title'],
                "image":item['thumbnail']['path']+'.'+item['thumbnail']['extension'],
                "onsaleDate":item['dates'][0]['date']
            }
            result.append(comic)

        return result
    

# Esta funcion recibe un parametro dictionary, que posee 3 propiedades
# 1.- Nombre del Personaje
def getmMarveInformation(filter):
    character = filter['personaje']
    requieredComic = False
    QUERY = ''
    if character != '' and character != None:
        QUERY = f'name={character}'
        requiereComic = True
    else:
        QUERY = f'orderBy=name'

    try:
        response = requests.get(URLBASE+'/characters?limit=100&'+QUERY+URLKEYS)
        response.raise_for_status()
        
    except HTTPError as _httperr:
        print(f'HTTP error occurred: {_httperr}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        data = response.json() 
        resultPersonaje = []
        resultComic = []
        #Se obtiene la respuesta del servicio de Marvel
        for item in data['data']['results']:
            # Se obtienen los datos requeridos
            personaje = {
                "id":item['id'],
                "name":item['name'],
                "image":item['thumbnail']['path']+'.'+item['thumbnail']['extension'],
                "appearances":item['comics']['available']
            }
            # En caso de que se una busqueda especifica se obtienen los comics relacionados al personaje
            if requiereComic:
                resultComic = getComics(item['id'])

            resultPersonaje.append(personaje)


        return {
            "personaje":resultPersonaje,
            "comic":resultComic
        }
    return None
            


# Test-------------------------------------------
# getComics('Hulk')
# print(getCharacters(''))
# python mrvelComics.py