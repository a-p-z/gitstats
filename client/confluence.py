#!/usr/bin/env python3
import http.client
import base64
import json


class ConfluenceClient:

    def __init__(self, uri, username, password):
        self.uri = uri
        self.encoded = base64.b64encode("%s:%s" % (username, password)).decode("ascii")

    def convert_wiki_to_storage(self, value):
        headers = {
            "Authorization": "Basic %s" % self.encoded,
            "Content-type": "application/json"
        }
        body = {
            "value": value.replace("\n", "\\n"),
            "representation": "wiki"
        }
        connection = http.client.HTTPSConnection(self.uri)
        connection.request("POST", "/rest/api/contentbody/convert/storage", json.dumps(body), headers)
        response = connection.getresponse()
        response_body = response.read()
        connection.close()
        return json.loads(response_body)["value"]

    def update_content(self, _id, value):
        pass
        content = self.get_content_by_id(_id)
        version = content["version"]["number"] + 1
        headers = {
            "Authorization": "Basic %s" % self.encoded,
            "Content-type": "application/json"
        }
        body = {
            "body": {
                "storage": {
                    "value": value.replace("\n", "\\n"),
                    "representation": "storage"
                }
            },
            "version": {
                "number": version}
        }
        connection = http.client.HTTPSConnection(self.uri)
        connection.request("PUT", "/rest/api/content/%s" % id, json.dumps(body), headers)
        response = connection.getresponse()
        connection.close()

    def get_content_by_id(self, _id):
        headers = {
            "Authorization": "Basic %s" % self.encoded,
            "Content-type": "application/json"
        }
        connection = http.client.HTTPSConnection(self.uri)
        connection.request("GET", "/rest/api/content/%s" % _id)
        response = connection.getresponse()
        response_body = response.read()
        connection.close()
        return json.loads(response_body)
