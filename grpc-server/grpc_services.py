from datetime import datetime
import csv
from generated import meter_usage_pb2_grpc, meter_usage_pb2


class MeterUsage(meter_usage_pb2_grpc.MeterUsage):

    def GetReadings(self, request, context):

        limit = 0

        with open('./resources/meterusage.1656671982.csv', 'rt') as file:
            reader = csv.reader(file)
            next(reader)

            for csv_reading in reader:

                if request.n > 0 and limit >= request.n:
                    yield None

                reading = meter_usage_pb2.Reading(
                    time = csv_reading[0],
                    usage = float(csv_reading[1])
                )

                limit += 1
                yield reading


    def GetReadingsRange(self, request, context):

        DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

        from_date = datetime.strptime(request.from_date_ts, )
        to_date = datetime.strptime(request.to_date_ts, DATE_FORMAT)

        with open('./resources/meterusage.1656671982.csv', 'rt') as file:
            reader = csv.reader(file)
            next(reader)

            for csv_reading in reader:

                reading_date = datetime.strptime(csv_reading[0], DATE_FORMAT)

                if reading_date > to_date:
                    yield None

                if reading_date >= from_date and reading_date <= to_date:

                    reading = meter_usage_pb2.Reading(
                        time = csv_reading[0],
                        usage = float(csv_reading[1])
                    )

                    yield reading