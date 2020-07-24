from datetime import datetime
from http.HttpResponse import HttpResponse


class Dispatcher:

    @staticmethod
    def dispatch(response: HttpResponse):
        print(
            datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT").__str__()
            + ' \"' + response.request.method + '\"'
            + ' \"' + response.request.first_line + '\"'
            + ' \"' + response.status_code + '\"'
        )
