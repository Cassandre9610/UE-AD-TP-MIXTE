# REST API
import json
import os
import time
from flask_jwt_extended import create_access_token, get_jwt_identity, JWTManager, jwt_required
from flask import Flask, request, jsonify, make_response
from pymongo import MongoClient, ReturnDocument

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI", "mongodb://root:example@mongo-user:27017/")
client = MongoClient(MONGO_URI)
db = client["userdb"]
users_collection = db["users"]


app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret"
jwt = JWTManager(app)

PORT = 3004
HOST = '0.0.0.0'


def error_not_found(message: str):
   return make_response(jsonify({"error":message}),404)


@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the User service!</h1>"


@app.route("/json", methods=['GET'])
@jwt_required()
def get_json():
   current_user = json.loads(get_jwt_identity())
   if current_user.get("admin") != True:
      return make_response({"error": "You don't have access to that information"}, 401)
   return make_response(jsonify(list(users_collection.find({}, {"_id": 0}))), 200)


@app.route("/user/<userid>", methods=['GET'])
@jwt_required()
def get_by_id(userid):
   current_user = json.loads(get_jwt_identity())
   if current_user["id"] != userid and current_user.get("admin") != True:
      return make_response({"error": "You don't have access to that information"}, 401)

   user = users_collection.find_one({"id": userid}, {"_id": 0})
   if user is None:
      return error_not_found("User ID not found")
   return make_response(jsonify(user), 200)


@app.route("/user/name/<username>", methods=["GET"])
@jwt_required()
def get_by_name(username):
   current_user = json.loads(get_jwt_identity())
   if current_user["name"] != username and current_user.get("admin") != True:
      return make_response({"error": "You don't have access to that information"}, 401)

   user = users_collection.find_one({"name": username}, {"_id": 0})
   if user is None:
      return error_not_found("User name not found")
   return make_response(jsonify(user), 200)


@app.route("/user/<userid>/name/<new_name>", methods=["PUT"])
@jwt_required()
def update_user(userid, new_name):
   current_user = json.loads(get_jwt_identity())
   if current_user["id"] != userid and current_user.get("admin") != True:
      return make_response({"error": "You don't have access to that information"}, 401)

   updated = users_collection.find_one_and_update(
         {"id": userid},
         {"$set": {"name": new_name}},
         projection={"_id": 0},
         return_document=ReturnDocument.AFTER,
      )
   if not updated :
      return error_not_found("User ID not found")
   return make_response(jsonify(updated), 200)


@app.route("/user/<userid>", methods=['DELETE'])
@jwt_required()
def delete_user(userid):
   current_user = json.loads(get_jwt_identity())
   if current_user["id"] != userid and current_user.get("admin") != True:
      return make_response({"error": "You don't have access to that information"}, 401)

   result = users_collection.delete_one({"id": userid})
   if result.deleted_count == 0:
      return make_response(jsonify({
         "success": False,
            "message": "User not found",
      }), 404)

   return make_response(jsonify({
      "success": True,
      "message": "User deleted successfully",
   }), 200)


@app.route("/user/<userid>", methods=['POST'])
def create_user(userid):
   req: dict = request.get_json()

   if users_collection.find_one({"id": userid}) is not None:
      return make_response(jsonify({"error":"user ID already exists"}),500)
   
   newuser = {
      "id": userid,
      "name": req["name"],
      "admin": False if "admin" not in req.keys() else req["admin"],
      "last_active": time.time_ns()
   }
   
   users_collection.insert_one(newuser.copy())
   return make_response(jsonify(newuser), 201)


@app.route("/login", methods=["POST"])
def login():
   req = request.get_json()
   user = users_collection.find_one({"id": req["id"]}, {"_id": 0})
   if user:
      token = create_access_token(identity = json.dumps(user))
      return make_response(jsonify(access_token = token), 200)

   return error_not_found("User ID not found")


if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
