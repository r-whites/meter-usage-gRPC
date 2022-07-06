from concurrent import futures
import grpc

from generated import meter_usage_pb2_grpc
from .grpc_services import MeterUsage


class Server:

    @staticmethod
    def start():
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
        server.add_insecure_port('[::]:51510')

        meter_usage_pb2_grpc.add_MeterUsageServicer_to_server(MeterUsage(), server)
        server.start()
        print("gRPC server started ..")
        server.wait_for_termination()