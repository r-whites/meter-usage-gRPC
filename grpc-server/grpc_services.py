import imp
import os
import csv
from generated.services import meter_usage_pb2_grpc, meter_usage_pb2


class MeterUsage(meter_usage_pb2_grpc.MeterUsage):

    def GetReading(self, request, context):

        with open('./resources/meterusage.1656671982.csv', 'rt') as file:
            reader = csv.reader(file)
            next(reader)

            for csv_reading in reader:
                print(csv_reading)
                reading = meter_usage_pb2.Reading(
                    time = csv_reading[0],
                    usage = float(csv_reading[1])
                )
                yield reading