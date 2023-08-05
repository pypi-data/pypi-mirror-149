# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ctrader_open_api', 'ctrader_open_api.messages']

package_data = \
{'': ['*']}

install_requires = \
['Twisted==21.7.0', 'protobuf==3.20.1']

setup_kwargs = {
    'name': 'ctrader-open-api',
    'version': '0.9.1',
    'description': 'A Python package for interacting with cTrader Open API',
    'long_description': '# OpenApiPy\n\n\n[![PyPI version](https://badge.fury.io/py/ctrader-open-api.svg)](https://badge.fury.io/py/ctrader-open-api)\n![versions](https://img.shields.io/pypi/pyversions/ctrader-open-api.svg)\n[![GitHub license](https://img.shields.io/github/license/spotware/OpenApiPy.svg)](https://github.com/spotware/OpenApiPy/blob/main/LICENSE)\n\nA Python package for interacting with cTrader Open API.\n\nThis package uses Twisted and it works asynchronously.\n\n- Free software: MIT\n- Documentation: https://spotware.github.io/OpenApiPy/.\n\n\n## Features\n\n* Works asynchronously by using Twisted\n\n* Methods return Twisted deferreds\n\n* It contains the Open API messages files so you don\'t have to do the compilation\n\n* Makes handling request responses easy by using Twisted deferreds\n\n## Insallation\n\n```\npip install ctrader-open-api\n```\n\n# Usage\n\n```python\n\nfrom ctrader_open_api import Client, Protobuf, TcpProtocol, Auth, EndPoints\nfrom ctrader_open_api.messages.OpenApiCommonMessages_pb2 import *\nfrom ctrader_open_api.messages.OpenApiCommonMessages_pb2 import *\nfrom ctrader_open_api.messages.OpenApiMessages_pb2 import *\nfrom ctrader_open_api.messages.OpenApiModelMessages_pb2 import *\nfrom twisted.internet import reactor\n\nhostType = input("Host (Live/Demo): ")\nhost = EndPoints.PROTOBUF_LIVE_HOST if hostType.lower() == "live" else EndPoints.PROTOBUF_DEMO_HOST\nclient = Client(host, EndPoints.PROTOBUF_PORT, TcpProtocol)\n\ndef onError(failure): # Call back for errors\n    print("Message Error: ", failure)\n\ndef connected(client): # Callback for client connection\n    print("\\nConnected")\n    # Now we send a ProtoOAApplicationAuthReq\n    request = ProtoOAApplicationAuthReq()\n    request.clientId = "Your application Client ID"\n    request.clientSecret = "Your application Client secret"\n    # Client send method returns a Twisted deferred\n    deferred = client.send(request)\n    # You can use the returned Twisted deferred to attach callbacks\n    # for getting message response or error backs for getting error if something went wrong\n    # deferred.addCallbacks(onProtoOAApplicationAuthRes, onError)\n    deferred.addErrback(onError)\n\ndef disconnected(client, reason): # Callback for client disconnection\n    print("\\nDisconnected: ", reason)\n\ndef onMessageReceived(client, message): # Callback for receiving all messages\n    print("Message received: \\n", Protobuf.extract(message))\n\n# Setting optional client callbacks\nclient.setConnectedCallback(connected)\nclient.setDisconnectedCallback(disconnected)\nclient.setMessageReceivedCallback(onMessageReceived)\n# Starting the client service\nclient.startService()\n# Run Twisted reactor\nreactor.run()\n\n```\n\nPlease check documentation or samples for a complete example.\n\n## Dependencies\n\n* <a href="https://pypi.org/project/twisted/">Twisted</a>\n* <a href="https://pypi.org/project/protobuf/">Protobuf</a>\n',
    'author': 'Spotware',
    'author_email': 'connect@spotware.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/spotware/openApiPy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
