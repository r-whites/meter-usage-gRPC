from crypt import methods
from os import read
from flask import Flask, Response, redirect, render_template
import grpc
from google.protobuf import json_format
from generated.services import meter_usage_pb2_grpc, meter_usage_pb2

server = Flask(__name__)
channel = grpc.insecure_channel('localhost:51510')
meter_usage_stub = meter_usage_pb2_grpc.MeterUsageStub(channel=channel)

@server.route('/api/readings', methods = ['GET'])
def meter_usage():

    def get_json_readings():
        readings = meter_usage_stub.GetReading(meter_usage_pb2.Empty())
        for reading in readings:
            to_json = json_format.MessageToJson(reading)
            print(to_json)
            yield to_json

    return Response(get_json_readings(), content_type="application/json")