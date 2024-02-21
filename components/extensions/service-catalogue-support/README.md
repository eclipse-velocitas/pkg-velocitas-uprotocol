# Service Catalgoue Support

Adds support for functional interfaces of a uApp/uService towards a service defined within a service catalogue (e.g. [COVESA uServices](https://github.com/COVESA/uservices/)). **Format below is not finalized and needs to be discussed once this toolchain component is developed.**

**CONCEPT SHOULD BE ALIGNED WITH gRPC**


## Usage in AppManifest.json

```json
{
    "type": "service-catalogue-consumer",
    "config": {
        "src": "https://github.com/COVESA/uservices.git",
        "services": [
            "Chassis",
            "Horn"
        ]
    }
}
```
