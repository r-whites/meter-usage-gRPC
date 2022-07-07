from datetime import datetime
import csv
from . import meter_usage_pb2_grpc, meter_usage_pb2


class MeterUsageImp(meter_usage_pb2_grpc.MeterUsageServicer):

    def GetReadings(self, request, context):
        ''' Returns a stream of Reading and stops after n if defined '''

        limit = 0

        with open('./resources/meterusage.1656671982.csv', 'rt') as file:
            reader = csv.reader(file)

            # Skip the header row (assuming it is always present)
            next(reader)

            for csv_reading in reader:

                # End the stream if a valid n is given and the limit has been reached
                if request.n > 0 and limit >= request.n:
                    yield None

                reading = meter_usage_pb2.Reading(
                    time = csv_reading[0],
                    usage = float(csv_reading[1])
                )

                limit += 1
                yield reading


    def GetReadingsRange(self, request, context):
        ''' Returns a stream of Reading within a given datetime range '''

        # Coversion of timestamp strig into datetime objects for comparison
        DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

        from_date = datetime.strptime(request.from_date_ts, DATE_FORMAT)
        to_date = datetime.strptime(request.to_date_ts, DATE_FORMAT)

        with open('./resources/meterusage.1656671982.csv', 'rt') as file:
            reader = csv.reader(file)

            # Skip the header row (assuming it is always present)
            next(reader)

            for csv_reading in reader:

                # Get the current row datetime
                reading_date = datetime.strptime(csv_reading[0], DATE_FORMAT)

                # End the stream because the current row is in the future of the indicated range
                if reading_date > to_date:
                    yield None

                # Return a Reading if the datetime is container within the range
                if reading_date >= from_date and reading_date <= to_date:

                    reading = meter_usage_pb2.Reading(
                        time = csv_reading[0],
                        usage = float(csv_reading[1])
                    )

                    yield reading