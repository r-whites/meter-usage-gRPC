import pytest
import random
import grpc
from generated.meter_usage_pb2 import RequestReadings, RequestReadingsRange

@pytest.fixture(scope='module')
def grpc_add_to_server():
    from generated.meter_usage_pb2_grpc import add_MeterUsageServicer_to_server
    return add_MeterUsageServicer_to_server

@pytest.fixture(scope='module')
def grpc_servicer():
    from grpc_services import MeterUsageImp
    return MeterUsageImp()

@pytest.fixture(scope='module')
def grpc_stub_cls(grpc_channel):
    from generated.meter_usage_pb2_grpc import MeterUsageStub
    return MeterUsageStub


def test_readings_n_request(grpc_stub):
    N = random.randint(1, 3000)
    readings_request = RequestReadings(n=N)
    readings = grpc_stub.GetReadings(readings_request)
    assert len(list(readings)) == N 