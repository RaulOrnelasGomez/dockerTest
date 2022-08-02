import connectionBD as con
import secrets
import string
from bson.objectid import ObjectId
import mrvelComics as comicFunction

bd = con.bdConnection()

def newUser(credentials):

    numDocuments = bd.count_documents({"username":credentials['username'],"password":credentials['password']})
    print("numDocuments",numDocuments)
    if numDocuments == 0:
        resultInsert = bd.insert_one(credentials)
        return resultInsert.acknowledged
    else:
        return False


def signIn(credentials):

    #Generamos un token en ese momento
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(30))
    #En caso de que existe el usuario le colocamos el nuevo token 
    filter = {"username":credentials['username'],"password":credentials['password']}
    bd.update_one(filter, {"$set":{"token":password}})

    #Regresamos el usuario encontrado ya con el nuevo token, en que de que no
    #la función va a regresar un None
    return bd.find_one(filter)

def findByToken(token):
    return bd.find_one({"token":token})


def addComicUser(req):
    resp = {}
    #Se busca por el token del usuario, porque en teória si ya existe en la base
    # es porque ya tiene usuario y contraseña y utilizaremos el token para validaciones
    usuario = findByToken(req['token'])
    if usuario:
        #Si existe se procede al inset
        comics = comicFunction.getComics(-1,req['comic'])
        if comics:
            resultado = bd.update_one({ "token": req['token'] }, { "$push": { "comics": {"$each": comics} } })
            if resultado.acknowledged:
                resp = {
                    "result": 1,
                    "message": "Comics encontrados y añadidos de manera exitosa",
                    "code": 200,
                    "data": {
                       "comicAgregados": comics
                    }
                }
            else:
                resp = {
                    "result": -1,
                    "message": "Ocurrió un error al tratar de guardar la informarción, intente de nuevo por favor",
                    "code": 409,
                    "data": {
                        "idTransaccion":resultado.upserted_id
                    }
                }
        else:
            resp = {
                    "result": -1,
                    "message": "No se encontraron comics con la palabra "+req['comic']+", agrega el comic para que lo busquemos",
                    "code": 409,
                    "data": None
                }
    else:
        resp = {
                "result": -1,
                "message": "El usaurio no es valido",
                "code": 401,
                "data": None
            }
    return resp