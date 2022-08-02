from sqlite3 import enable_shared_cache
from flask import Flask,Response,request
from bson import json_util
import coppelUser as _user

app = Flask(__name__)

@app.route('/')
def index():
    return Response(json_util.dumps(
        {
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
        }),mimetype='application/json',status=200) 

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



if __name__=='__main__':
    app.run(host="0.0.0.0", port=6000)