import json
from graphql import GraphQLError
import requests
import schedule_pb2
import schedule_pb2_grpc
import grpc

DATA_PATH = '{}/data/bookings.json'.format(".")
SCHEDULE_HOST = 'localhost:3003' #TODO env variable


def _write(new_file):
    with open(DATA_PATH, "w") as wfile:
        json.dump(new_file, wfile)


def get_booking_with_userid(_, info, _userid):
    with open(DATA_PATH, "r") as file:
        bookings = json.load(file)["bookings"]
        for booking in bookings:
            if booking["userid"] == _userid:
                return booking
        raise GraphQLError("Aucune reservation pour cet utilisateur")


def add_booking(_, info, _userid: str, _date: str, _movie_id: str): 
    with grpc.insecure_channel(SCHEDULE_HOST) as channel:
        stub = schedule_pb2_grpc.ScheduleStub(channel)

        try:
            schedule_response = stub.GetScheduleByDate(_date)
            if _movie_id not in [str(movie) for movie in schedule_response.movies]:
                raise GraphQLError("Movie not found in schedule for this date")
            
        except grpc.RpcError:
            raise GraphQLError("This date is not in the schedule")

    with open(DATA_PATH, "r") as file:
        bookings = json.load(file)["bookings"]
        for booking in bookings:
            if str(booking["userid"]) == _userid:
                for booking_date in booking["dates"]:
                    if str(booking_date["date"]) == _date:
                        if _movie_id not in [
                            str(movie) for movie in booking_date["movies"]
                        ]:
                            booking_date["movies"].append(_movie_id)
                            _write(bookings)

                        return booking

                booking["dates"].append({
                    "date": _date,
                    "movies": [_movie_id]
                })
                _write(bookings)
                return booking

        # aucune reservation pour cet user
        new_booking = {
            "userid": _userid,
            "dates": [
                {
                    "date": _date,
                    "movies": [_movie_id]
                }
            ]
        }
        bookings.append(new_booking)
        _write(bookings)
        return new_booking


def delete_booking(_, info, _userid: str, _date: str, _movie_id: str):
    with open(DATA_PATH, "r") as file:
        bookings: list = json.load(file)["bookings"]
        for booking in bookings:
            if booking["userid"] == _userid:
                for date in booking["dates"]:
                    if date["date"] == _date:
                        date["movies"] = [movie for movie in date["movies"] if movie != _movie_id]
                        #TODO check si la liste des films a changée
                        _write({"bookings": bookings})
                        return booking
            
    raise GraphQLError("aucune donnée à supprimer")