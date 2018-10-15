#!/usr/bin/env python
import httplib
import base64
import json

class ConfluenceClient:
    
    def __init__(self, uri, username, password):
        self.uri = uri
        self.encoded = base64.b64encode("%s:%s" % (username, password)).decode("ascii")
    
    
    def convertWikiToStorage(self, value):
        headers = {
            "Authorization": "Basic %s" % self.encoded,
            "Content-type": "application/json"
            }
        body = {
            "value": value.replace("\n", "\\n"),
            "representation": "wiki"
            }
        connection = httplib.HTTPSConnection(self.uri)
        connection.request("POST", "/rest/api/contentbody/convert/storage", json.dumps(body), headers)
        response = connection.getresponse()
        responseBody = response.read()
        connection.close()
        return json.loads(responseBody)["value"]
    
    
    def updateContent(self, id, value):
        pass
        content = self.getContentById(id)
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
        connection = httplib.HTTPSConnection(self.uri)
        connection.request("PUT", "/rest/api/content/%s" % id, json.dumps(body), headers)
        response = connection.getresponse()
        connection.close()
    
    
    def getContentById(self, id):
        headers = {
            "Authorization": "Basic %s" % self.encoded, 
            "Content-type": "application/json"
        }
        connection = httplib.HTTPSConnection(self.uri)
        connection.request("GET", "/rest/api/content/%s" % id)
        response = connection.getresponse()
        responseBody = response.read()
        connection.close()
        return json.loads(responseBody)
