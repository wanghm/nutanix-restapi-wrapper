# -*- coding: utf-8 -*-
################################################################################
#  A sample wrapper script of Nutanix Rest API V2.0 with test code
#  (Work In Process)
################################################################################
import requests
import urllib3
import json
import getpass

class Nutanix_restapi_v2_wrapper():
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

        

def test1_1(nutanix_api_v2):
    # Get VG list
    api_url = base_url + "volume_groups"
    response = nutanix_api_v2.http_get(api_url)
     
    if not response.ok:
        print(response.text)
        exit(1)

    d = json.loads(response.text)
    #print(json.dumps(d, indent=2))
    print("")
    print("volume_group_uuid                   , volume_group_name")
    print("-------------------------------------------------------")
    volume_groups = d["entities"]
    for volume_group in volume_groups:
        volume_group_name = volume_group["name"]
        volume_group_uuid = volume_group["uuid"]
        print(volume_group_uuid + ", " + volume_group_name)

def test1_2(nutanix_api_v2):
    # Get vm list
    api_url = base_url + "vms"
    response = nutanix_api_v2.http_get(api_url)
     
    if not response.ok:
        print(response.text)
        exit(1)

    d = json.loads(response.text)
    #print(json.dumps(d, indent=2))
    print("")
    print("vm_uuid                             , vm_name")
    print("-------------------------------------------------------")
    vms = d["entities"]
    for vm in vms:
        vm_name = vm["name"]
        vm_uuid = vm["uuid"]
        print(vm_uuid + ", " + vm_name)


def test2(nutanix_api_v2):
    # Create a new Volume Group
    api_url = base_url + "volume_groups"
    payload_dict = {
        "description": "Created by Nutanix API v2.0",
        "disk_list": [
            {
            "create_spec": {
                "container_uuid": "91ad254b-80f8-42e3-9d2c-a4a55884e923",
                "size_mb": 10240
               }
            },
            {
            "create_spec": {
                "container_uuid": "91ad254b-80f8-42e3-9d2c-a4a55884e923",
                "size_mb": 30720
                }
            }
        ],
        "name": "test-vg-by-api-888"
    }
    payload_json = json.dumps(payload_dict)
    response = nutanix_api_v2.http_post(api_url, payload_json)
    print(response.text)

def test3(nutanix_api_v2):
    # Attach a Volume Group to a VM
    api_url = base_url + "volume_groups/63a1482f-83a8-4aed-91f4-9fe52b1a52b4/attach"
    payload_dict = {
        "operation": "ATTACH",
        "uuid": "63a1482f-83a8-4aed-91f4-9fe52b1a52b4",
        "vm_uuid": "0262fc6a-8e4b-498c-81b6-6f2a21e5e3af"
    }
    payload_json = json.dumps(payload_dict)
    response = nutanix_api_v2.http_post(api_url, payload_json)
    print(response.text)

def test4(nutanix_api_v2):
    # AAdd Disks to an existing Volume Group
    api_url = base_url + "volume_groups/63a1482f-83a8-4aed-91f4-9fe52b1a52b4/disks"
    payload_dict = {
        "create_spec": {
        "container_uuid": "91ad254b-80f8-42e3-9d2c-a4a55884e923",
        "size_mb": 40960
        },
        "volume_group_uuid": "63a1482f-83a8-4aed-91f4-9fe52b1a52b4"
    }
    payload_json = json.dumps(payload_dict)
    response = nutanix_api_v2.http_post(api_url, payload_json)
    print(response.text)

if __name__ == "__main__":
    prism_host = input("Prism Host: ")
    username = input("Username: ")
    password = getpass.getpass("password: ")

    base_url = "https://" + prism_host + ":9440/api/nutanix/v2.0/"

    nutanix_api_v2 = Nutanix_restapi_v2_wrapper(username, password, base_url)
 
    # test1-1: get volume group list
    test1_1(nutanix_api_v2)

    # test1-2: get vm list
    test1_2(nutanix_api_v2)
    
    # test2: create a volume group
    #test2(nutanix_api_v2)

    # test3: Attach a Volume Group to a VM
    #test3(nutanix_api_v2)

    # test4: Add Disks to an existing Volume Group
    #test4(nutanix_api_v2)

