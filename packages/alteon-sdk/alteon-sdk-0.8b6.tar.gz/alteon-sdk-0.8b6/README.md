
Introduction
=====================

- provide API for developers to interact with Alteon structures in Python environment via REST Backend
- access to Alteon Management & Configuration functions
- abstract configuration model to alteon elements via consistent Declarative-style Configurators

in this model a consistent object structures are exposed to user per configurator type.
each configurator handle base commands over a device (READ, READ_ALL, DELETE, UPDATE & DEPLOY)
the package handles the binding & translation between alteon device to abstract objects
it works both ways: abstract <-> alteon structure, in other words it translate 
abstract to alteon configuration and read from alteon into abstract type.
multi choices (enums) are consumed dynamically from the beans package.
developer can choose to work with string_value/int/enums directly

the SDK is requires Python >3.6

Minimum Supported Alteon Versions:
    31.0.10.0,
    32.2.2.0

device direct API, Configurators and Management are available via the Alteon client module:

```pycon
from radware.alteon.client import AlteonClient
from radware.alteon.beans.SlbNewCfgEnhRealServerTable import *

alteon_client_params = dict(
        validate_certs=False,
        user='admin',
        password='admin',
        https_port=443,
        server='172.16.1.1',
        timeout=15,
)
client = AlteonClient(**alteon_client_params)

# read bean from device:
bean = SlbNewCfgEnhRealServerTable()
bean.Index = 'real_1'
print(client.api.device.read(bean))

# work with Configurators:
client.api.mgmt.config.commit()
print(client.api.mgmt.info.software)
print(client.api.conf.type.dns_responders.read_all())
server_params = ServerParameters()
server_params.index = 'real1'
server_params.ip_address = '3.3.3.3'
client.api.conf.execute('deploy', server_params, dry_run=True, write_on_change=True, get_diff=True)
```

another way of use is directly via the desire Configurator:

```pycon
from radware.alteon.sdk.configurators.server import *

connection = AlteonConnection(**alteon_client_params)
server_configurator = ServerConfigurator(connection)

server_params = ServerParameters()
server_params.index = 'real1'
server_params.ip_address = '3.3.3.3'
server_params.availability = 5
server_params.server_ports = [56, 78]
server_params.weight = 5
server_params.server_type = EnumSlbRealServerType.remote_server
server_params.state = EnumSlbRealServerState.enabled
server_configurator.deploy(server_params)
```

OR the configuration manager:

```pycon
from radware.sdk.configurator import DeviceConfigurator, DeviceConfigurationManager
from radware.alteon.sdk.configurators.ssl_key import SSLKeyConfigurator

ssl_key_configurator = SSLKeyConfigurator(**alteon_client_params)
cfg_mng = DeviceConfigurationManager()
result = cfg_mng.execute(ssl_key_configurator, DeviceConfigurator.READ_ALL, None, passphrase=passphrase)
print(result.content_translate)
```

further details & doc will be added later 

Installation
=================

```pycon
pip install alteon-sdk
```

Design Principles
=================

-	46 configurators: some indexed & others are a summary
-	management functions for facts collection, carry out operation tasks and manage device configuration
-	Alteon direct device API 
-	Alteon client: aggregate all configuration & management modules along with device API
-	Bean package complied from MIB (auto generated)
-	Each configurator is standalone and can be initiate for an AdcConnection
-	Abstraction <-> beans automatic attributes  binding + specific processing when needed
-	Abstraction <-> Alteon configuration bi-direction translation (deploy from abstract , read alteon config into abstract)
-	Define dry_run delete procedure for "special configurators": relevant for when there is no delete procedure, mostly for global configuration
-   Identify duplicate entries within a structure

Authors
=======

Alteon SDK was created by [Leon Meguira](https://https://github.com/leonmeguira)

Copyright
=======

Copyright 2019 Radware LTD

License
=======
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and


