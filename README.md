# nutanix-restapi-wrapper

## Nutanix Rest API Versions and Base URL

* v2.0
  * https://{Prims Host}:9440/PrismGateway/services/rest/v2.0/
  * https://{Prims Host}:9440/api/nutanix/v2.0/
* V3
  * https://{PrismCentral Host}/api/nutanix/v3/


## Resources

* Code Samples: https://www.nutanix.dev/code_samples/
* API references: https://www.nutanix.dev/reference/prism_element/v2/
* API Explorer: https://{Prism Host}:9440/api/nutanix/v2/api_explorer/index.htm
* Community: https://next.nutanix.com/api-31


## Sample API Specification

Nutanix API reference: https://www.nutanix.dev/reference/prism_element/v2/

### 1. Create a new Volume Group

#### URL: https://xxx.xxx.xxx.xxx:9440/api/nutanix/v2.0/volume_groups/

#### Required parameters
* disk_list []
   * create_spec
      * container_uuid
      * size_mb
* name

#### Sample Payload:
```
{
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
        "size_mb": 20480
      }
    },
    {
      "create_spec": {
        "container_uuid": "91ad254b-80f8-42e3-9d2c-a4a55884e923",
        "size_mb": 30720
      }
    }
  ],
  "name": "test-vg-by-api-4"
}
```

Result:

![result](resources/CreateVG_result.png)

### 2. Attach a Volume Group to a VM

#### URL: https://xxx.xxx.xxx.xxx:9440/api/nutanix/v2.0/volume_groups/{uuid}/attach

#### Required Parameters

* operation: ATTACH (Fixed value)
* uuid: uuid of volume group
* vm_uuid

#### Sample Payload:
```
{
  "operation": "ATTACH",
  "uuid": "63a1482f-83a8-4aed-91f4-9fe52b1a52b4",
  "vm_uuid": "0262fc6a-8e4b-498c-81b6-6f2a21e5e3af"
}
```

Result:

![Result](resources/AttachVGroup2VM.png)

### 3. Add Disks to an existing Volume Group

#### URL: https://xxx.xxx.xxx.xxx:9440/api/nutanix/v2.0/volume_groups/{volume_group_uuid}/disks

#### Required Parameters

* create_spec
  * container_uuid
  * size_mb
* volume_group_uuid

#### Sample Payload

```
{
  "create_spec": {
    "container_uuid": "91ad254b-80f8-42e3-9d2c-a4a55884e923",
    "size_mb": 40960
  },
  "volume_group_uuid": "63a1482f-83a8-4aed-91f4-9fe52b1a52b4"
}
```

### 4. Add client IP/iqn to the Volume Group

#### URL: https://xxx.xxx.xxx.xxx:9440/api/nutanix/v2.0/volume_groups/{volume_group_uuid}/open

#### Required Parameters
* iscsi_client
  * client_address: client IP or iqn
* operation: "ATTACH" (fixed value)
* uuid: uuid of Voluume Group

#### Sample Payload
```
{
  "iscsi_client": {
  "client_address": "iqn.1994-05.com.redhat:78597e13914"
  },
  "operation": "ATTACH",
  "uuid": "54ee3438-40fd-44ca-b628-95534bd3add3"
}
```
