import datetime
import time
from dateutil.parser import parse
from .connect import make_request
import pickle


class AuthTokenManager(object):
    def __init__(self, api_url, api_key):
        self.api_url = api_url
        self.api_key = api_key

    def check_time(self, time):
        time_now = datetime.datetime.now()
        elapsed = time_now - parse(time)
        if int(elapsed.seconds) >= 400:
            status = False
        else:
            status = True
        return status

    def check_auth_token(self):
        try:
            at = pickle.load(open("access_token.pickle", "rb"))
        except (OSError, IOError) as e:
            at = {"dt": None, "at": None}
            with open('access_token.pickle', 'wb') as handle:
                pickle.dump(at, handle, protocol=pickle.HIGHEST_PROTOCOL)

        with open('access_token.pickle', 'rb') as handle:
            tt = pickle.load(handle)

        if tt["at"] is None:
            status = False
            return status
        else:
            time_check = self.check_time(str(tt["dt"]))
            if time_check is False:
                status = False
                at = {"dt": None, "at": None}
                with open('access_token.pickle', 'wb') as handle:
                    pickle.dump(at, handle, protocol=pickle.HIGHEST_PROTOCOL)
            else:
                status = True

        return status

    def new_auth_token(self):
        auth_check = self.check_auth_token()
        if auth_check is False:
            response = self.auth_login()

            at = {"dt": datetime.datetime.now(),
                  "at": response['authorizations']["access_token"],
                  "rt": response['authorizations']["refresh_token"]
                  }

            with open('access_token.pickle', 'wb') as handle:
                pickle.dump(at, handle, protocol=pickle.HIGHEST_PROTOCOL)

            print("new auth token created")
            return response['authorizations']["access_token"]

        elif auth_check is True:
            print("Token is not stale... nothing to do")
            with open('access_token.pickle', 'rb') as handle:
                tt = pickle.load(handle)
            return tt["at"]

    def auth_login(self):
        data = {}
        data["type"] = "POST"
        data["url"] = "{}/{}".format(self.api_url, "auth/login/")
        data["header"] = str(self.api_key)
        data["params"] = {"apikey": self.api_key}
        data["payload"] = ''
        return make_request(**data)
