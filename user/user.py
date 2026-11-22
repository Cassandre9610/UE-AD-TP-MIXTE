# REST API
from flask import Flask, render_template, request, jsonify, make_response
# import requests
import json
from werkzeug.exceptions import NotFound
from flask_jwt_extended import create_access_token, get_jwt_identity, JWTManager, jwt_required

# CALLING gRPC requests
import grpc
from concurrent import futures
# import booking_pb2
# import booking_pb2_grpc
# import movie_pb2
# import movie_pb2_grpc

# CALLING GraphQL requests
# todo to complete

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret"
jwt = JWTManager(app)

PORT = 3004
HOST = '0.0.0.0'

with open('{}/data/users.json'.format("."), "r") as jsf:
   users: list = json.load(jsf)["users"]

def write(new_users):
   with open('{}/data/users.json'.format("."), 'w') as f:
      full = {}
      full['users']=users
      json.dump(full, f)


def error_not_found(message: str):
   return make_response(jsonify({"error":message}),500) # TODO 404 ?


@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the User service!</h1>"

@app.route("/json", methods=['GET'])
def get_json():
   res = make_response(jsonify(users), 200)
   return res

@app.route("/user/<userid>", methods=['GET'])
def get_by_id(userid):
   for user in users:
      if str(user["id"]) == str(userid):
         res = make_response(jsonify(user),200)
         return res
      
   return error_not_found("User ID not found")

@app.route("/user/name/<username>", methods=["GET"])
@jwt_required()
def get_by_name(username):
   current_user = json.loads(get_jwt_identity())
   if current_user["name"] != username and current_user["admin"] != True:
      return make_response({"error": "You don't have access to that information"}, 401)

   for user in users:
      if str(user["name"]) == str(username):
         res = make_response(jsonify(user), 200)
         return res
      
   return error_not_found("User name not found")


@app.route("/user/<userid>/name/<new_name>", methods=["PUT"])
def update_user(userid, new_name):
   for user in users:
      if str(user["id"]) == userid:
         user["name"] = new_name
         res = make_response(jsonify(user), 200)
         write(users)
         return res
      
   return error_not_found("User ID not found")

@app.route("/user/<userid>", methods=['DELETE'])
def delete_user(userid):
   for user in users:
      if str(user["id"]) == str(userid):
         users.remove(user)
         write(users)
         return make_response(jsonify(user), 200)
      
   return error_not_found("User ID not found")

@app.route("/user/<userid>", methods=['POST'])
def create_user(userid):
   req: dict = request.get_json()

   for user in users:
      if str(user["id"]) == str(userid):
            print(user["id"])
            print(userid)
            return make_response(jsonify({"error":"user ID already exists"}),500)

   # req["last_used"] = time.time_ns() # Pas certain de la methode
   if "admin" not in req.keys():
      req["admin"] = False
   
   users.append(req)
   write(users)
   res = make_response(jsonify({"message":"user added"}),200)
   return res

@app.route("/login", methods=["POST"])
def login():
   req = request.get_json()
   for user in users:
      if user["id"] == req["id"]:
         #TODO mdp
         token = create_access_token(identity = json.dumps(user))
         return make_response(jsonify(access_token = token), 200)

   return error_not_found("User ID not found")


if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
