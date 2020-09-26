# -*- coding: utf-8 -*-
################################################################################
#  A sample wrapper script of Nutanix Rest API V2.0 with test code
#  (Work In Process)
################################################################################
import requests
import urllib3
import json
import getpass

class Nutanix_restapi_wrapper():
    def __init__(self, username, password, base_url):
        self.username = username
        self.password = password
        self.base_url = base_url

    def __supress_security(self):
        # supress the security warnings
        urllib3.disable_warnings()

    def http_get(self, api_url):
        # supress the security warnings
        self.__supress_security()
    
        s = requests.Session()
        s.auth = (self.username, self.password)
        s.headers.update({'Content-Type': 'application/json; charset=utf-8'})
        return s.get(api_url, verify=False)
        
    def http_post(self, api_url, json_data):
        # supress the security warnings
        self.__supress_security()
    
        s = requests.Session()
        s.auth = (self.username, self.password)
        s.headers.update({'Content-Type': 'application/json; charset=utf-8'})
        
        return s.post(api_url, data=json_data, verify=False)

    def http_put(self, api_url):
        #todo
        return

    def http_delete(self, api_url):
        #todo
        return


def get_bp_uuid(nutanix_api_v3, target_bp_name):
    api_url = base_url + "/blueprints/list"
    payload_dict = {
        "kind":"blueprint"
    }

    payload_json = json.dumps(payload_dict)
    response = nutanix_api_v3.http_post(api_url, payload_json)
    #print(response.text)

    d = json.loads(response.text)
    #print(json.dumps(d, indent=2))
    bps = d["entities"]
    for bp in bps:
        bp_name = bp["status"]["name"]
        bp_uuid = bp["status"]["uuid"]
        print(bp_name + ", " + bp_uuid)
        if (bp_name == target_bp_name):
            break
    return bp_uuid
            

def get_app_profile_uuid(nutanix_api_v3, bp_uuid):
    # Get Storage Container list
    api_url = base_url + "blueprints/" + bp_uuid + "/runtime_editables"
    response = nutanix_api_v3.http_get(api_url)
     
    if not response.ok:
        print(response.text)
        exit(1)

    d = json.loads(response.text)
    #print(json.dumps(d, indent=2))
    resources = d["resources"]
    for resource in resources:
        app_profile_uuid=  resource["app_profile_reference"]["uuid"]
        print("app_profile_uuid= " + app_profile_uuid)
        break
    return app_profile_uuid


def launch_bp(nutanix_api_v3, app_name, bp_uuid, app_profile_uuid):
    api_url = base_url + "/blueprints/" + bp_uuid + "/simple_launch"
    payload_dict = {
        "spec": {
            "app_name": app_name,
            "app_description": "Calm application launched via Nutanix Calm REST API",
            "app_profile_reference": {
                "kind": "app_profile",
                "name": "Default",
                "uuid": app_profile_uuid
            }
        }
    }

    payload_json = json.dumps(payload_dict)
    response = nutanix_api_v3.http_post(api_url, payload_json)
    print(response.text)

    return

if __name__ == "__main__":
    bp_name = "hm-CalmAPILab"
    app_name = "CalmAPI-app4"

    prism_host = input("Prism Host: ")
    username = input("Username: ")    
    password = getpass.getpass("password: ")

    base_url = "https://" + prism_host + ":9440/api/nutanix/v3/"

    nutanix_api_v3 = Nutanix_restapi_wrapper(username, password, base_url)
 
    bp_uuid = get_bp_uuid(nutanix_api_v3, bp_name)
    print ("bp_uuid is: " + bp_uuid)

    app_profile_uuid = get_app_profile_uuid(nutanix_api_v3, bp_uuid)

    launch_bp(nutanix_api_v3, app_name, bp_uuid, app_profile_uuid)
