from datetime import datetime

from http.HttpRequest import HttpRequest


class HttpResponse:
    STATIC_FILE_PATH = 'files/'
    BASE_STATIC_FILE_PATH = './files'
    ACCEPTED_FILE_EXTENSIONS = \
        {
            'jpeg': 'image/jpg',
            'png': 'image/png',
            'txt': 'txt/plain',
            'html': 'text/html',
            'jpg': 'image/jpg'
        }

    HEADERS = {
        400: 'HTTP/1.0 400 Bad Request\n'
             'Connection: close\n'
             'Content-Type: text/html\n',
        501: 'HTTP/1.0 501 Not Implemented\n'
             'Connection: close\n'
             'Content-Type: text/html\n',
        405: 'HTTP/1.0 405 Method Not Allowed\n'
             'Connection: close\n'
             'Content-Type: text/html\n'
             'Allow: GET\n',
        200: 'HTTP/1.0 200 OK\n'
             'Connection: close\n'
             'Content-Type: ?\n',
        404: 'HTTP/1.0 404 Not Found\n'
             'Connection: close\n'
             'Content-Type: text/html\n',
        'CONTENT_LENGTH': 'Content-Length: ?\n',
        'GZIP': 'Content-Encoding: gzip\n',
        'DATE': 'Date: ?\n',
        'END_OF_HEADER': '\n'
    }

    BODIES = {
        400: b'<!DOCTYPE html><html lang="en"><body> 400 Bad Request! - Request is not acceptable </body></html>',
        501: b'<!DOCTYPE html><html lang="en"><body> 501 Not Implemented! - We don\'t support this request method </body></html>',
        405: b'<!DOCTYPE html><html lang="en"><body> 405 Method Not Allowed! - You can only use GET method </body></html>',
        404: b'<!DOCTYPE html><html lang="en"><body> 404 Not Found - File was not found</body></html>',
    }

    def __init__(self, request: HttpRequest):
        self.status_code = None
        self.request = request
        self.header = ''
        self.body = b''
        self.file = None
        self.file_extension = None

        self._build_response()

    def _build_response(self):
        if self.request.invalid:
            self.header += self.HEADERS[400]
            self.body += self.BODIES[400]
        elif self.request.method not in ('GET', 'HEAD', 'POST', 'PUT', 'DELETE'):
            self.header += self.HEADERS[501]
            self.body += self.BODIES[501]
        elif self.request.method != 'GET':
            self.header += self.HEADERS[405]
            self.body += self.BODIES[405]
        elif self._is_valid_path():
            self.header += self.HEADERS[200].replace('?', self.ACCEPTED_FILE_EXTENSIONS[self.file_extension])
            self.body += self.file
        else:
            self.header += self.HEADERS[404]
            self.body += self.BODIES[404]

        if 'gzip' in self.request.header.get('Accept-Encoding', '').lower():
            self._gzip_response()

        self.header += self.HEADERS['DATE'] \
            .replace(
            '?',
            datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT").__str__())
        self.header += self.HEADERS['CONTENT_LENGTH'].replace('?', str(len(self.body)))
        self.header += self.HEADERS['END_OF_HEADER']
        self.status_code = ' '.join(self.header.split('\n')[0].split()[1:])

    def _is_valid_path(self):
        if self.request.path == '/':
            self.file = self._create_root_page()
            self.file_extension = 'html'
            return True

        file_path = self.BASE_STATIC_FILE_PATH + self.request.path
        try:
            f = open(file_path, 'rb')
            self.file = f.read()
            f.close()
            self.file_extension = self.request.path.split('.')[-1]
            return True
        except Exception as e:
            return False

    def render(self):
        header = self.header.encode()
        body = self.body.encode() if isinstance(self.body, str) else self.body
        return header + body

    def _gzip_response(self):
        import gzip
        self.body = gzip.compress(self.body.encode() if isinstance(self.body, str) else self.body)
        self.header += self.HEADERS['GZIP']

    def _create_root_page(self):
        from pathlib import Path
        paths = list(map(str, list(Path(self.BASE_STATIC_FILE_PATH + "/").rglob("*.*"))))

        def path_to_link_method(x):
            return \
                '<div><a href=\"' + x[len(self.STATIC_FILE_PATH):] + '\">' + x[len(
                    self.STATIC_FILE_PATH):] + '</a></div>'

        string = "\n".join(list(map(path_to_link_method, paths)))
        return string.encode()
