# Tool Manager

A tool manager for uProtocol tools. At the moment the following are supported:

* [uProtocol Simulator](https://github.com/eclipse-uprotocol/up-simulator)
* [uP Client Android](https://github.com/eclipse-uprotocol/up-client-android-java)

## Requirements

The tool manager shall meet the following requirements:

* it shall download the respective tools to the `$VELOCITAS_HOME` and make them available to the velocitas project via exposed programs. (e.g. `velocitas exec up-simulator`)

* it shall read used tool versions from a configuration file stored in the project directory. (Could be stored in the `.velocitas.json`)

e.g. (`.velocitas.json`)
```json
{
    ...
    "variables": {
        "uprotocolSimulatorVersion": "0.0.1",
        "ulinkAndroidBinderVersion": "0.1.0"
    }
}
```

* it shall provide a UI (could be terminal prompts) which shows upgradeable tools and allow updates
easily
