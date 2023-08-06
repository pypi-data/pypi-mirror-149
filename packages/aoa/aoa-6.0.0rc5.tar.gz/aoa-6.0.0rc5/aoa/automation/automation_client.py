from requests.auth import HTTPBasicAuth

import requests
import json


class AutomationClient():

    def __init__(self, url, auth_mode="basic", auth_user=None, auth_pass=None):
        self.url = url

        if auth_mode == "basic":
            self.auth = HTTPBasicAuth(auth_user, auth_pass)

        elif auth_mode == "kerberos":
            from requests_kerberos import HTTPKerberosAuth
            self.auth=HTTPKerberosAuth()

        else:
            raise Exception("Auth mode: {} not supported.".format(auth_mode))

    def trigger_workflow(self, event):
        resp = requests.post(
            url=self.url,
            auth=self.auth,
            headers={'Content-Type': 'application/json'},
            data=json.dumps(event)
        )

        resp.raise_for_status()

        try:
            return resp.json()
        except ValueError:
            return resp.text
