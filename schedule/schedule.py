import grpc
from concurrent import futures
import schedule_pb2
import schedule_pb2_grpc
import json
import copy
import requests
import os


MOVIE_SERVICE_HOST = os.environ.get('MOVIE_SERVICE_HOST') or "localhost:3001"

class ScheduleServicer(schedule_pb2_grpc.ScheduleServicer):

    def __init__(self):
        with open('{}/data/times.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["schedule"]


    def check_if_movie_exists(self, movie_id:str):
        query = '''query GetMovie($id: String!) {
                    movie_with_id(_id: $id) {
                        id
                    }
                }'''
        res = requests.post(f"http://{MOVIE_SERVICE_HOST}/graphql", json = {
            "query": query,
            "variables": {"id": movie_id}
        })

        return res.json()["data"]["movie_with_id"] is not None and len(res.json()["data"]["movie_with_id"]) > 0


    def GetSchedule(self, request, context):
        return self._db_to_schedules()


    def GetScheduleByDate(self, request, context):
        for day in self.db:
            if day["date"] == request.date:
                return self._make_day(day)
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details('Date is not in schedule')
        return self._make_day({"date": "", "movies": []})


    def GetDatesByMovieId(self, request, context):
        return_list: list = []
        for day in self.db:
            if day["movies"].count(request.id) > 0 :
                return_list.append(day["date"])
    
        return schedule_pb2.Dates(date = return_list)


    def CreateSchedule(self, request, context):
        if not self.check_if_movie_exists(request.movie):
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('Movie does not exists')
            return self._make_day({"date": "", "movies": []})
    
        for day in self.db:
            if day["date"] == request.date:
                if day["movies"].count(request.movie) == 0:
                    day["movies"].append(request.movie)
                    return self._make_day(day)
                else :
                    context.set_code(grpc.StatusCode.ALREADY_EXISTS)
                    context.set_details('Movie aready scheduled for this date')
                    return self._make_day({"date": "", "movies": []})
        # aucune date ne correspond
        new_day = {
            "date": request.date,
            "movies": [request.movie]
        }
        self.db.append(new_day)
        self._write()
        return self._make_day(new_day)


    def DeleteMovieFromDate(self, request, context):
        old_schedule: list[dict] = self.db
        new_schedule = []
        res = self._make_day({"date": "", "movies": []})
        
        for day in old_schedule :
            new_day = copy.deepcopy(day)
            if new_day["date"] == request.date :
                new_day["movies"] = [movie for movie in new_day["movies"] if movie != request.movie]
                res = self._make_day(new_day)
            
            if len(new_day["movies"]) > 0 :
                new_schedule.append(new_day)
    
        if new_schedule == old_schedule:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Movie not found in this date')
            return self._make_day({"date": "", "movies": []})

        self.db = new_schedule
        self._write()
        return res


    def DeleteScheduleByDate(self, request, context):
        print("suppression par date")
        old_schedule = copy.deepcopy(self.db)
        self.db = [day for day in old_schedule if day["date"] != request.date]
        if self.db == old_schedule:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Date not found in schedule')
            return schedule_pb2.Schedules(schedule = [])
        self._write()
        return self._db_to_schedules()


    def _write(self):
        with open('{}/data/times.json'.format("."), "w") as jsf:
            json.dump({"schedule": self.db}, jsf)


    def _make_day(self, day):
        return schedule_pb2.Day(date = day["date"], movies = day["movies"])


    def _db_to_schedules(self):
        schedules = []
        for day in self.db :
            schedules.append(schedule_pb2.Day(date = day["date"], movies = day["movies"]))
        return schedule_pb2.Schedules(schedule = schedules)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    schedule_pb2_grpc.add_ScheduleServicer_to_server(ScheduleServicer(), server)
    server.add_insecure_port('[::]:3002')
    server.start()
    print("Server started on port 3002")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
