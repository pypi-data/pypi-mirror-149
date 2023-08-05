# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['smart_on_fhir_client', 'smart_on_fhir_client.requester']

package_data = \
{'': ['*']}

install_requires = \
['PyJWT>=2.3.0,<3.0.0',
 'aiocache>=0.11.1,<0.12.0',
 'cryptography>=36.0.1,<37.0.0',
 'fhir.resources>=6.2.1,<7.0.0',
 'fhirpy>=1.3.0,<2.0.0',
 'loguru>=0.5.3,<0.6.0',
 'seito>=0.1.2,<0.2.0',
 'tenacity>=8.0.1,<9.0.0',
 'uvicorn>=0.17.0,<0.18.0']

setup_kwargs = {
    'name': 'smart-on-fhir-client',
    'version': '0.1.6',
    'description': 'Smart on fhir python client',
    'long_description': '# smart-on-fhir-client 🔥\n\nPackage allowing to request a fhir server with the smart-on-fhir protocol. \n\n> ℹ Warning\n>\n> It is not a webserver providing a webserver with a callback url\n> usually involved in the smart-on-fhir procedure\n\n\n### Tutorial\n\nFirst, we will need to create a partner. We can do this easily subclassing the `Partner` class.\n```python\nimport os\nfrom smart_on_fhir_client.partner import Partner\nfrom typing import Set\nfrom smart_on_fhir_client.strategy import Strategy\n\nclass Lifen(Partner):\n    name = \'LIFEN\'\n    supported_strategies: Set[Strategy] = {Strategy.M2M}\n    client_id: str = os.getenv("LIFEN_CLIENT_ID")\n    client_secret: str = os.getenv("LIFEN_CLIENT_SECRET")\n    token_url: str = ... # set the token url\n    fhir_url: str = ... # set the fhir url\n\n    # additional information\n    audience: str = ... # audience\n    database_reference: str = ... # optional \n    grant_type: str = "client_credentials" # set the credentials\n\nLIFEN = Lifen()\n```\n\n```python\nfrom smart_on_fhir_client.client import smart_client_factory\nfrom smart_on_fhir_client.requester.fhir_requester import fhir_client_manager\nfrom smart_on_fhir_client.strategy import Strategy\n\n# set up your own fhir server url\nfhir_client_manager.set_own_fhir_url("http://localhost:8080/fhir")\n\nasync def register():\n    async with smart_client_factory:\n        await fhir_client_manager.register_partner_async(\n            smart_client_factory.builder()\n                .for_partner(LIFEN)\n                .for_strategy(Strategy.M2M)\n                # you can register special classes for specific fhir resources\n                .register_cls_for(\'Patient\', LifenPatientResource)\n        )\n        first_patient = await fhir_client_manager.LIFEN.Patient.search().limit(10).first()\n        await first_patient.pipe_to_target_fhir_server()\n\n```\n\n\n### Features\n\nAllow to send some fetched fhir resources to another fhir server\nvia the `pipe_to_target_fhir_server`, making data transfer between two fhir\nservers easier.\n\n### Notes\nWork based heavily on fhir-py and fhir-resources python packages',
    'author': 'Marc',
    'author_email': 'marc@synapse-medicine.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
