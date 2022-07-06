SHELL := /bin/bash

define HELP

proto-compile	Compiles the proto files into Python server and client stub
api-run-dev		Runs the api Flask app on localhost in development mode
grpc-run		Runs the gRPC server on localhost

endef

export HELP

help:
	@echo "$$HELP"

proto-compile:
	python3 -m grpc_tools.protoc -I proto --python_out=./generated --grpc_python_out=./generated ./proto/*.proto; \
	sed -i -E 's/\(^import.*_pb2\)/from . \1/g' ./generated/*.py
	
api-run-dev:
	export FLASK_APP=api/app.py; \
	export FLASK_ENV=development; \
	flask run;

grpc-run:
	python -m grpc-server;
