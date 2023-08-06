# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['OpenApiDriver']

package_data = \
{'': ['*']}

install_requires = \
['openapi-core',
 'openapi-spec-validator',
 'prance',
 'requests',
 'robotframework-datadriver>=1.6.1',
 'robotframework-openapi-libcore>=1.4.0',
 'robotframework>=4']

setup_kwargs = {
    'name': 'robotframework-openapidriver',
    'version': '3.2.1',
    'description': 'A library for contract-testing OpenAPI / Swagger APIs.',
    'long_description': '---\n---\n\n# OpenApiDriver for Robot Framework®\n\nOpenApiDriver is an extension of the Robot Framework® DataDriver library that allows\nfor generation and execution of test cases based on the information in an OpenAPI\ndocument (also known as Swagger document).\nThis document explains how to use the OpenApiDriver library.\n\nFor more information about Robot Framework®, see http://robotframework.org.\n\nFor more information about the DataDriver library, see\nhttps://github.com/Snooz82/robotframework-datadriver.\n\n---\n\n> Note: OpenApiDriver is currently in early development so there are currently\nrestrictions / limitations that you may encounter when using this library to run\ntests against an API. See [Limitations](#limitations) for details.\n\n---\n\n## Installation\n\nIf you already have Python >= 3.8 with pip installed, you can simply run:\n\n`pip install --upgrade robotframework-openapidriver`\n\n---\n\n## OpenAPI (aka Swagger)\n\nThe OpenAPI Specification (OAS) defines a standard, language-agnostic interface\nto RESTful APIs, see https://swagger.io/specification/\n\nThe OpenApiDriver module implements a reader class that generates a test case for\neach endpoint, method and response that is defined in an OpenAPI document, typically\nan openapi.json or openapi.yaml file.\n\n> Note: OpenApiDriver is designed for APIs based on the OAS v3\nThe library has not been tested for APIs based on the OAS v2.\n\n---\n\n## Getting started\n\nBefore trying to use OpenApiDriver to run automatic validations on the target API\nit\'s recommended to first ensure that the openapi document for the API is valid\nunder the OpenAPI Specification.\n\nThis can be done using the command line interface of a package that is installed as\na prerequisite for OpenApiDriver.\nBoth a local openapi.json or openapi.yaml file or one hosted by the API server\ncan be checked using the `prance validate <reference_to_file>` shell command:\n\n```shell\nprance validate http://localhost:8000/openapi.json\nProcessing "http://localhost:8000/openapi.json"...\n -> Resolving external references.\nValidates OK as OpenAPI 3.0.2!\n\nprance validate /tests/files/petstore_openapi.yaml\nProcessing "/tests/files/petstore_openapi.yaml"...\n -> Resolving external references.\nValidates OK as OpenAPI 3.0.2!\n```\n\nYou\'ll have to change the url or file reference to the location of the openapi\ndocument for your API.\n\n> Note: Although recursion is technically allowed under the OAS, tool support is limited\nand changing the API to not use recursion is recommended.\nAt present OpenApiLibCore has limited support for parsing OpenAPI documents with\nrecursion in them.\n\nIf the openapi document passes this validation, the next step is trying to do a test\nrun with a minimal test suite.\nThe example below can be used, with `source` and `origin` altered to fit your situation.\n\n``` robotframework\n*** Settings ***\nLibrary            OpenApiDriver\n...                    source=http://localhost:8000/openapi.json\n...                    origin=http://localhost:8000\nTest Template      Validate Using Test Endpoint Keyword\n\n*** Test Cases ***\nTest Endpoint for ${method} on ${endpoint} where ${status_code} is expected\n\n*** Keywords ***\nValidate Using Test Endpoint Keyword\n    [Arguments]    ${endpoint}    ${method}    ${status_code}\n    Test Endpoint\n    ...    endpoint=${endpoint}    method=${method}    status_code=${status_code}\n\n```\n\nRunning the above suite for the first time is likely to result in some\nerrors / failed tests.\nYou should look at the Robot Framework `log.html` to determine the reasons\nfor the failing tests.\nDepending on the reasons for the failures, different solutions are possible.\n\nDetails about the OpenApiDriver library parameters that you may need can be found\n[here](https://marketsquare.github.io/robotframework-openapidriver/openapidriver.html).\n\nThe OpenApiDriver also support handling of relations between resources within the scope\nof the API being validated as well as handling dependencies on resources outside the\nscope of the API. In addition there is support for handling restrictions on the values\nof parameters and properties.\n\nDetails about the `mappings_path` variable usage can be found\n[here](https://marketsquare.github.io/robotframework-openapi-libcore/advanced_use.html).\n\n---\n\n## Limitations\n\nThere are currently a number of limitations to supported API structures, supported\ndata types and properties. The following list details the most important ones:\n- Only JSON request and response bodies are currently supported.\n- The unique identifier for a resource as used in the `paths` section of the\n    openapi document is expected to be the `id` property on a resource of that type.\n- Limited support for query strings and headers.\n- Limited support for authentication\n    - `username` and `password` can be passed as parameters to use Basic Authentication\n    - A [requests AuthBase instance](https://docs.python-requests.org/en/latest/api/#authentication)\n        can be passed and it will be used as provided.\n    - No support for per-endpoint authorization levels (just simple 401 validation).\n- byte, binary, date, date-time string formats not supported yet.\n\n',
    'author': 'Robin Mackaij',
    'author_email': None,
    'maintainer': 'Robin Mackaij',
    'maintainer_email': None,
    'url': 'https://github.com/MarketSquare/robotframework-openapidriver',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
