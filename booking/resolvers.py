import json
from graphql import GraphQLError
import schedule_pb2_grpc
import schedule_pb2
import grpc
import os

DATA_PATH = '{}/data/bookings.json'.format(".")
SCHEDULE_HOST = os.environ.get('SCHEDULE_HOST') or 'localhost:3002'


def _read():
    with open(DATA_PATH, "r") as file:
        bookings = json.load(file)["bookings"]
        return bookings


def _write(new_file):
    with open(DATA_PATH, "w") as wfile:
        json.dump(new_file, wfile)


def get_booking_with_userid(_, info, _userid):
    bookings = _read()
    for booking in bookings:
        if booking["userid"] == _userid:
            return booking
    raise GraphQLError("Aucune reservation pour cet utilisateur")


def get_booking_with_date(_, info, _date):
    bookings = _read()
    data = []
    for booking in bookings:
        dates = []
        for booking_date in booking["dates"]: 
            if str(booking_date["date"]) == str(_date):
                dates.append(booking_date)
        if len(dates) > 0:
            data.append({"userid": booking["userid"], "dates": dates})
    return data


def get_booking_with_movie(_, info, _movie_id):
    bookings = _read()
    data = []
    for booking in bookings:
        dates = [
            {
                "date": booking_date["date"],
                "movies": booking_date["movies"]
            }
            for booking_date in booking["dates"]
            if any(str(booked_movie) == str(_movie_id) for booked_movie in booking_date["movies"])
        ]
        data.append({"userid": booking["userid"], "dates": dates})
    return data


def get_movies_with_userid_and_date(_, info, _user_id, _date):
    bookings = _read()
    for booking in bookings:
        if str(booking["userid"]) == str(_user_id):
            for d in booking["dates"]:
                if str(d["date"]) == str(_date):
                    return d["movies"]
    raise GraphQLError("Aucun film trouvé")


def add_booking(_, info, _userid: str, _date: str, _movie_id: str): 
    with grpc.insecure_channel(SCHEDULE_HOST) as channel:
        stub = schedule_pb2_grpc.ScheduleStub(channel)

        try:
            schedule_response = stub.GetScheduleByDate(schedule_pb2.Date(date = _date))
            print("done")
            if _movie_id not in [str(movie) for movie in schedule_response.movies]:
                raise GraphQLError("Movie not found in schedule for this date")
            
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise GraphQLError("This date is not in the schedule")
            raise e

    bookings = _read()
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


def delete_movie_from_date(_, info, _userid: str, _date: str, _movie_id: str):
    bookings: list = _read()
    for index_booking, booking in enumerate(bookings):
        if str(booking["userid"]) == str(_userid):
            for index_booking_date, booking_date in enumerate(booking["dates"]):
                if str(booking_date["date"]) == str(_date):
                    for index_booked_movie, booked_movie in enumerate(booking_date["movies"]):
                        if str(booked_movie) == str(_movie_id):
                            booking_date["movies"].pop(index_booked_movie)
                            if not booking_date["movies"]:
                                booking["dates"].pop(index_booking_date)
                            if not booking["dates"]:
                                bookings.pop(index_booking)
                            _write(bookings)
                            return booking
            
    raise GraphQLError("aucune donnée à supprimer")


def delete_user_from_booking(_, info, _userid):
    bookings = _read()
    for booking in bookings:
        if str(booking["userid"]) == str(_userid):
            bookings.remove(booking)
            _write(bookings)
            return booking
    raise GraphQLError("aucune donnée à supprimer")