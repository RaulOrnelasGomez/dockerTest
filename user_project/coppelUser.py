import connectionBD as con
import secrets
import string
from bson.objectid import ObjectId


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
