FROM python:3.9-slim-buster

RUN mkdir /server

COPY grpc-server/ /server/grpc-server/

WORKDIR /server/grpc-server

RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

RUN python3 -m grpc_tools.protoc -I proto --python_out=./generated --grpc_python_out=./generated ./proto/*.proto; \
	sed -i -E 's/\(^import.*_pb2\)/from . \1/g' ./generated/*.py

EXPOSE 51510
CMD [ "python3", "-m", "server" ]