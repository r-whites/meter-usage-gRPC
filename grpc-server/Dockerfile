FROM python:3.9-slim-buster

RUN mkdir /server

COPY ./grpc-server/ /server/
COPY ./proto/ /server/proto/
COPY ./resources/ /resources

WORKDIR /server

RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

RUN python3 -m grpc_tools.protoc -I proto --python_out=./ --grpc_python_out=./ ./proto/*.proto \
	&& sed -i -E 's/(^import.*_pb2)/from . \1/g' ./*_pb2_grpc.py
