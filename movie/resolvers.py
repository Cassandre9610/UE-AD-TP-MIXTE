import os
from uuid import uuid4
from pymongo import MongoClient, ReturnDocument

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI", "mongodb://root:example@mongo-movie:27017/")
client = MongoClient(MONGO_URI)
db = client["moviedb"]
movies_collection = db["movies"]
actors_collection = db["actors"]

def movies(_,info):
    return list(movies_collection.find())


def movie_with_id(_,info,_id):
    return movies_collection.find_one({"id": _id})

            
def movie_with_title(_,info,_title):
    return list(movies_collection.find({"title": {"$regex": _title}}))


def add_movie(_,info,_title,_director,_rating):
    newmovie = {
        "id": str(uuid4()),
        "title": _title,
        "director": _director,
        "rating": _rating
    }
    movies_collection.insert_one(newmovie)
    return newmovie


def update_movie_rate(_,info,_id,_rate):
    return movies_collection.find_one_and_update(
        {"id": _id},
        {"$set": {"rating": _rate}},
        return_document=ReturnDocument.AFTER,
    )


def update_movie_title(_,info,_id,_title):
    return movies_collection.find_one_and_update(
        {"id": _id},
        {"$set": {"title": _title}},
        return_document=ReturnDocument.AFTER,
    )


def update_movie_director(_,info,_id,_director):
    return movies_collection.find_one_and_update(
        {"id": _id},
        {"$set": {"director": _director}},
        return_document=ReturnDocument.AFTER,
    )


def resolve_actors_in_movie(movie, info):
    return list(actors_collection.find({"films": movie["id"]}))


def delete_movie(_, info, _id):
    result = movies_collection.delete_one({"id": _id})
    if result.deleted_count == 0:
        return {
            "success": False,
            "message": "Movie not found",
        }

    return {
        "success": True,
        "message": "Movie deleted successfully",
    }