FROM python:3.15.2-alpine

WORKDIR /app

# copy the requirements file in the workdir
COPY requirements.txt /app/

# install the Python requirements
RUN pip install -r requirements.txt

# copy the app files and directories
COPY schedule/ /app/

RUN python -m grpc_tools.protoc -I=. --python_out=. --grpc_python_out=. schedule.proto

# start movie.py when the container is started
CMD ["python3", "schedule.py"]
