import os
import grpc
from flask import Flask, Response, request
from . import meter_usage_pb2, meter_usage_pb2_grpc
from google.protobuf import json_format

app = Flask(__name__)
is_deployed = os.environ.get('FLASK_ENV') == 'production'
channel_address = 'dns:///grpc-server:51510' if is_deployed else 'localhost:51510'
channel = grpc.insecure_channel(channel_address)
meter_usage_stub = meter_usage_pb2_grpc.MeterUsageStub(channel=channel)

def get_json_meter_usage_stream(readings):
    ''' Returns a string stream encoding a list of json objects based on a stream of Reading '''

    try:
        # Keep a reference to a previous reading to correctly encode the end of the list
        prev_reading = next(readings)
    except StopIteration:
        # Enters when there are no readings, yields a empty list
        yield '[]'
        raise StopIteration

    # There is at least one reading, yields start of the list
    yield '['

    # Yields subsequent comma-separated json readings
    for reading in readings:
        to_json = json_format.MessageToJson(prev_reading)
        yield to_json + ','
        prev_reading = reading

    # prev_reading is the last element, yields together with list ending
    yield json_format.MessageToJson(prev_reading) + ']'


@app.route('/api/readings', methods = ['GET'])
def meter_usage():
    ''' Returns a stream of bytes encoding a json list of readings '''

    # Decide type of gRPC request based on the presence of n
    readings_request = meter_usage_pb2.RequestReadings(n=int(request.args['n'])) \
                       if 'n' in request.args else meter_usage_pb2.RequestReadings()

    readings = meter_usage_stub.GetReadings(readings_request)
    return Response(get_json_meter_usage_stream(readings=readings), content_type="application/json")


@app.route('/api/readings/range', methods = ['GET'])
def meter_usage_range():
    ''' Returns a stream of bytes encoding a json list of readings within a date range'''

    # For simplicty's sake, the request is fixed on server side, it can be constructed from GET query params
    request_range = meter_usage_pb2.RequestReadingsRange(
        from_date_ts = "2019-01-17 00:00:00",
        to_date_ts = "2019-01-17 23:59:00"
    )

    readings = meter_usage_stub.GetReadingsRange(request_range)
    
    return Response(get_json_meter_usage_stream(readings=readings), content_type="application/json")
