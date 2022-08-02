import mimetypes
from flask import Flask, jsonify, request,Response
from connection import * 
from bson import json_util
import mrvelComics as comicFunction

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome"


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

    comics = comicFunction.getmMarveInformation(req)

    if comics:
        value['result'] = 1
        value['code'] = 200
        value['message'] = 'Personaje encontrado'
        value['data'] = comics

    
    # print(value)
        
    return Response(json_util.dumps(value),mimetype='application/json',status=value['code'])



if __name__=='__main__':
    app.run(host="0.0.0.0", port=5000)