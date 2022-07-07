from re import A
import grpc
from flask import Flask, Response, request
from generated import meter_usage_pb2, meter_usage_pb2_grpc
from google.protobuf import json_format

app = Flask(__name__)
channel = grpc.insecure_channel('localhost:51510')
meter_usage_stub = meter_usage_pb2_grpc.MeterUsageStub(channel=channel)

def get_json_meter_usage_stream(readings):
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


@app.route('/api/readings', methods = ['GET'])
def meter_usage():

    readings_request = meter_usage_pb2.RequestReadings(n=int(request.args['n'])) \
                       if 'n' in request.args else meter_usage_pb2.RequestReadings()

    readings = meter_usage_stub.GetReadings(readings_request)
    return Response(get_json_meter_usage_stream(readings=readings), content_type="application/json")


@app.route('/api/readings/range', methods = ['GET'])
def meter_usage_range():

    request_range = meter_usage_pb2.RequestReadingsRange(
        from_date_ts = "2019-01-17 00:00:00",
        to_date_ts = "2019-01-17 23:59:00"
    )

    readings = meter_usage_stub.GetReadingsRange(request_range)
    
    return Response(get_json_meter_usage_stream(readings=readings), content_type="application/json")
