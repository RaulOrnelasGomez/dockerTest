from sqlite3 import enable_shared_cache
from flask import Flask,Response,request
from bson import json_util
import coppelUser as _user
import mrvelComics as comicFunction


app = Flask(__name__)

#
@app.route('/')
def index():
    return Response(json_util.dumps({
        "usuario" : {
            "Crear un nuevo usaurio utilice la siguiente estructura": {
                "username": "Coloca aquí tu nombre de usuario",
                "password": "Coloca aquí tu contraseña",
                "age": "Coloca aquí tu edad del usuario",
            },
            "Metodos":{
                "get":"El usuario y contraseña regresa el usuario con su respectivo token",
                "post":"Genera un nuevo usuario, que no existe previamente"
            },
            "url":"/user"
        },
        "comic_Personaje": {
            "Buscar un personaje o un comic": {
                "personaje": "Coloca aquí el nombre del personaje, en caso de esta vació devolverá la lista ordenada",
                "comic": "Escribe el nombre del comic para buscarlo",
            },
            "Metodos":{
                "get":"Mandar los campos como paramtros",
                "post":"Mandar los campos en el cuerpo de la petición (body)"
            },
            "url":"/searchComics"
        },
        "agregarComicUsuario": {
            "Buscar comic": {
                "token": "Coloca aquí el token generado al obtener las credenciales",
                "comic": "Escribe el nombre del comic para buscarlo",
            },
            "Metodos":{
                "post":"Mandar los campos en el cuerpo de la petición (body)"
            },
            "url":"/addToLayaway"
        },
        
        }),mimetype='application/json',status=200) 

#Buscador de comics
@app.route('/searchComics/',methods = ['POST', 'GET'])
def comicInfoGet():
    req = {
        "personaje":None,
        "comic":None
    }
    if request.method == 'POST':
        req = request.get_json()
    else:
        req['personaje'] = request.args.get('personaje')
        req['comic'] = request.args.get('comic')
    
    # print(req)

    value = {
        "result": -1,
        "message": "Error en la busqueda",
        "code": 409,
        "data": None
    }    

    comics = comicFunction.getMarveInformation(req)

    if comics:
        value['result'] = 1
        value['code'] = 200
        value['message'] = 'Personaje encontrado'
        value['data'] = comics
      
    return Response(json_util.dumps(value),mimetype='application/json',status=value['code'])


#Credenciales de usuario y nuevo usuario
@app.route('/user', methods=['POST','GET'])
def userInfo():

    req = {}
    resp = {}
    if request.method == 'POST':
        req = request.get_json()
        
        if _user.newUser(req):
            resp = {
                "result": 1,
                "message": "Usuario creado de manera exitosa",
                "code": 200,
                "data": None
            }
        else:
          resp = {
                "result": -1,
                "message": "El usuario ya existe",
                "code": 409,
                "data": req
            }  
    else:
        req['username'] = request.args.get('username')
        req['password'] = request.args.get('password')

        foundUser = _user.signIn(req)
        if foundUser:
            resp = {
                "id": str(_user.ObjectId(foundUser['_id'])),
                "name": foundUser['username'],
                "age": foundUser['age'],
                "token":foundUser['token'] 
            }  
            return Response(json_util.dumps(resp),mimetype="application/json",status=200)

        else:
            resp = {
                "result": -1,
                "message": "No se encontró un usuario con las credenciales ingresadas",
                "code": 401,
                "data": req
            }  
    return Response(json_util.dumps(resp),mimetype="application/json",status=resp['code'])


#Agregar comic a usuario
@app.route('/addToLayaway/',methods = ['POST'])
def addComicToUser():
    req = request.get_json()
    #Utilizaremos la funcion que se encuentra en coppelUser
    resp = _user.addComicUser(req)
    return Response(json_util.dumps(resp),mimetype="application/json",status=resp['code']) 





if __name__=='__main__':
    app.run(host="0.0.0.0", port=6000)