from concurrent import futures
import grpc

from generated import meter_usage_pb2_grpc
from .grpc_services import MeterUsage


class Server:

    ''' Helper class to initialize and start the gRPC server '''

    @staticmethod
    def start():
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))

        # Indicate the use of a non-TLS port connection (ony for testing)
        server.add_insecure_port('[::]:51510')
        
        meter_usage_pb2_grpc.add_MeterUsageServicer_to_server(MeterUsage(), server)
        server.start()
        print("gRPC server started ..")
        server.wait_for_termination()