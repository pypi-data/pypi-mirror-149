from .connect import make_request
from .authenticate import AuthTokenManager
import requests


class pyDojo(object):
    def __init__(self, dojo_onion, dojo_api_key):
        self.api_url = "{}/v2".format(dojo_onion)
        self.dojo_api_key = dojo_api_key
        self.at = AuthTokenManager(self.api_url, dojo_api_key).new_auth_token()
        self.data = {}
        self.data["header"] = str(self.at)
        self.data["params"] = ''        

    def auth_token_refresh(self):
        return AuthTokenManager(self.api_url, self.dojo_api_key).new_auth_token()


    def list_to_param_string(self, items):
        string = ""
        for i in items:
            i = "{}|".format(i)
            string = string + i
        return string[:-1]


    def get_status(self):
        self.at = self.auth_token_refresh()
        self.data["type"] = "GET"
        self.data["url"] = "{}/{}".format(self.api_url, "status")
        return make_request(**self.data)


    def get_fees(self):
        self.at = self.auth_token_refresh()
        self.data["type"] = "GET"
        self.data["url"] = "{}/{}".format(self.api_url, "fees")
        return make_request(**self.data)


    def get_block_header(self, blockhash):
        self.at = self.auth_token_refresh()
        self.data["type"] = "GET"
        self.data["url"] = "{}/{}/{}".format(self.api_url, "header", blockhash)
        return make_request(**self.data)
    
    
    def get_transactions(self, items):
        self.at = self.auth_token_refresh()
        self.data["type"] = "GET"
        self.data["url"] = "{}/{}".format(self.api_url, "txs")
        self.data['params'] = {'active': self.list_to_param_string(items)}
        return make_request(**self.data)


    def get_xpub(self, xpub):
        self.at = self.auth_token_refresh()
        self.data["type"] = "GET"
        self.data["url"] = "{}/{}/{}".format(self.api_url, "xpub", xpub)
        return make_request(**self.data)


    def get_transaction(self, item):
        self.at = self.auth_token_refresh()
        self.data["type"] = "GET"
        self.data["url"] = "{}/{}/{}".format(self.api_url, "tx", item)
        return make_request(**self.data)


    def add_xpub(self, xpub, type, segwit=None, force=None):
        self.at = self.auth_token_refresh()
        data = {}
        self.data["type"] = "POST"
        self.data["url"] = "{}/{}".format(self.api_url, "xpub")
        self.data["payload"] = {"xpub": str(xpub), "type": type}

        if segwit is not None:
            self.data["payload"]["segwit"] = segwit
        if force is not None:
            self.data["payload"]["force"] = force
        return make_request(**self.data)


    def push_transaction(self, tx):
        self.at = self.auth_token_refresh()
        self.data["type"] = "POST"
        self.data["url"] = "{}/{}/{}".format(self.api_url, "pushtx", tx)
        return make_request(**self.data)


    def get_wallet(self, pubkeys):
        self.at = self.auth_token_refresh()
        self.data["type"] = "GET"
        self.data["url"] = "{}/{}".format(self.api_url, "wallet")
        self.data['params'] = {'active': self.list_to_param_string(pubkeys)}
        return make_request(**self.data)


    def get_multiaddr_json(self, xpubs):
        self.at = self.auth_token_refresh()
        self.data["type"] = "GET"
        self.data["url"] = "{}/{}".format(self.api_url, "multiaddr")
        self.data['params'] = {'active': self.list_to_param_string(xpubs)}
        return make_request(**self.data)
