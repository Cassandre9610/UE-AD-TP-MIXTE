from uuid import uuid4
from pymongo import MongoClient, ReturnDocument

# MongoDB connection
client = MongoClient("mongodb://root:example@localhost:27017/")
db = client["movies"]
movies_collection = db["movies"]
actors_collection = db["actors"]

def movies(_,info):
    return list(movies_collection.find())


def movie_with_id(_,info,_id):
    return movies_collection.find_one({"_id": _id})

            
def movie_with_title(_,info,_title):
    return list(movies_collection.find({"title": {"$regex": _title}}))


def add_movie(_,info,_title,_director,_rating):
    newmovie = {
        "_id": str(uuid4()),
        "title": _title,
        "director": _director,
        "rating": _rating
    }
    movies_collection.insert_one(newmovie)
    return newmovie


def update_movie_rate(_,info,_id,_rate):
    return movies_collection.find_one_and_update(
        {"_id": _id},
        {"$set": {"rating": _rate}},
        return_document=ReturnDocument.AFTER,
    )


def update_movie_title(_,info,_id,_title):
    return movies_collection.find_one_and_update(
        {"_id": _id},
        {"$set": {"title": _title}},
        return_document=ReturnDocument.AFTER,
    )


def update_movie_director(_,info,_id,_director):
    return movies_collection.find_one_and_update(
        {"_id": _id},
        {"$set": {"director": _director}},
        return_document=ReturnDocument.AFTER,
    )


def resolve_actors_in_movie(movie, info):
    return list(actors_collection.find({"films": movie["_id"]}))


def delete_movie(_, info, _id):
    result = movies_collection.delete_one({"_id": _id})
    if result.deleted_count == 0:
        return {
            "success": False,
            "message": "Movie not found",
        }

    return {
        "success": True,
        "message": "Movie deleted successfully",
    }