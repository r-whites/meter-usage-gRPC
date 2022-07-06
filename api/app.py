from crypt import methods
from flask import Flask, Response, jsonify
import grpc
from google.protobuf import json_format
from generated import meter_usage_pb2_grpc, meter_usage_pb2

app = Flask(__name__)
channel = grpc.insecure_channel('localhost:51510')
meter_usage_stub = meter_usage_pb2_grpc.MeterUsageStub(channel=channel)

@app.route('/api/readings', methods = ['GET'])
def meter_usage():

    def get_json_readings():
        readings = meter_usage_stub.GetReading(meter_usage_pb2.Empty())
        for reading in readings:
            to_json = json_format.MessageToJson(reading)
            yield to_json

    return Response(get_json_readings(), content_type="application/json")