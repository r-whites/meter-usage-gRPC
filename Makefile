SHELL := /bin/bash

define HELP

proto-compile	Compiles the proto files into Python server and client stub
api-run-dev		Runs the api Flask app on localhost in development mode
grpc-run		Runs the gRPC server on localhost

endef

export HELP

help:
	@echo "$$HELP"

proto-compile-server:
	python3 -m grpc_tools.protoc -I proto --python_out=./grpc-server --grpc_python_out=./grpc-server ./proto/*.proto; \
	sed -i -E 's/\(^import.*_pb2\)/from . \1/g' ./grpc-server/*_pb2_grpc.py;

proto-compile-client:
	python3 -m grpc_tools.protoc -I proto --python_out=./api --grpc_python_out=./api ./proto/*.proto; \
	sed -i -E 's/\(^import.*_pb2\)/from . \1/g' ./api/*_pb2_grpc.py;
	
run-client:
	export FLASK_APP=api/app.py; \
	export FLASK_ENV=development; \
	flask run;

run-server:
	python -m grpc-server.server;
