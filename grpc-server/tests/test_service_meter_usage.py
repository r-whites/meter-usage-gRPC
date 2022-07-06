import pytest
import grpc
from generated.meter_usage_pb2 import Empty

@pytest.fixture(scope='module')
def grpc_add_to_server():
    from generated.meter_usage_pb2_grpc import add_MeterUsageServicer_to_server
    return add_MeterUsageServicer_to_server

@pytest.fixture(scope='module')
def grpc_servicer():
    from generated.meter_usage_pb2_grpc import MeterUsageServicer
    return MeterUsageServicer()

@pytest.fixture(scope='module')
def grpc_stub_cls(grpc_channel):
    from generated.meter_usage_pb2_grpc import MeterUsageStub
    return MeterUsageStub