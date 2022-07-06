import grpc
from flask import Flask, Response
from generated import meter_usage_pb2, meter_usage_pb2_grpc
from google.protobuf import json_format

app = Flask(__name__)
channel = grpc.insecure_channel('localhost:51510')
meter_usage_stub = meter_usage_pb2_grpc.MeterUsageStub(channel=channel)

@app.route('/api/readings', methods = ['GET'])
def meter_usage():

    def get_json_readings():
        readings = meter_usage_stub.GetReading(meter_usage_pb2.Empty())
        
        try:
            prev_reading = next(readings)
        except StopIteration:
            yield '[]'
            raise StopIteration

        yield '['

        for reading in readings:
            to_json = json_format.MessageToJson(reading)
            yield to_json + ','
            prev_reading = reading

        yield json_format.MessageToJson(prev_reading) + ']'

        
    return Response(get_json_readings(), content_type="application/json")
