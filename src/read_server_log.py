from datetime import datetime,timedelta

class ServerLog(object):

    def __init__(self, delimited_list):
        self.host = delimited_list[0]
        self.timezone = self.read_timezone(delimited_list[4])
        self.timestamp = self.read_timestamp(delimited_list[3])
        self.request = delimited_list[5]
        self.resource = self.read_resource(self.request)
        self.response_code = delimited_list[6]
        self.bytes = self.read_bytes(delimited_list[7])

    def read_bytes(self, byte_string):
        try:
            bytes = int(byte_string)
        except:
            bytes = 0 # '-' should be interpreted as 0 bytes
        return bytes

    def convert_to_GMT(self, timestamp, timezone):
        """Helper function to convert a timestamp to GMT using
        a timezone string (e.g. '-0400'). Not used in this project
        but would be required if we were merging data from different
        timezones."""
        ret = timestamp
        if timezone[0]=='+':
            ret+=timedelta(hours=int(timezone[1:4]))
        elif timezone[0]=='-':
            ret-=timedelta(hours=int(timezone[1:4]))
        return ret

    def process_timestamp(self, timestamp):
        ret = datetime.strptime(timestamp,'%d/%b/%Y:%H:%M:%S')
        return ret

    def read_timestamp(self, timestring):
        return self.process_timestamp(timestring[1:])

    def read_timezone(self, timezone):
        return timezone[0:-1]

    def read_resource(self, request):
        request_list = request.split(' ')
        if len(request_list) == 1:
            return request
        else:
            return request_list[1]

    def convert_to_string(self):
        """Method to return a string representation of the server log.
        This function essentially inverts the __init__ method and returns
        the original representation of the server log."""
        ret = ""
        ret += self.host
        ret += " - - ["
        ret += self.timestamp.strftime('%d/%b/%Y:%H:%M:%S')
        ret += " "
        ret += self.timezone
        ret += '] "'
        ret += self.request
        ret += '" '
        ret += self.response_code
        ret += " "
        ret += str(self.bytes)
        return ret
