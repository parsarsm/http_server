class HttpRequest:

    def __init__(self, raw_request_data):
        self.first_line = None
        self.method = ''
        self.version = ''
        self.path = ''
        self.header = {}
        self.body = ''
        self.invalid = False

        self._build_request(raw_request_data)

    def _build_request(self, raw_request_data):
        try:
            lines = raw_request_data.split('\r\n')
            self.first_line = lines[0]
            self.method, self.path, self.version = lines.pop(0).split()
            in_header = True
            for line in lines:
                if line == '':
                    in_header = False
                elif in_header:
                    k, v = line.split(': ')
                    self.header[k] = v
                else:
                    self.body += line
        except Exception:
            self.invalid = True
