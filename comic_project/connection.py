from pymongo import MongoClient


def bdConnection():
    try:
        client = MongoClient("mongodb+srv://test:test@cluster0.desoc.mongodb.net/?retryWrites=true&w=majority")
        db = client.get_database('comicsCoppel')
        collection = db.comics
        return collection
    except ConnectionError:
        print('Error de conexion')
