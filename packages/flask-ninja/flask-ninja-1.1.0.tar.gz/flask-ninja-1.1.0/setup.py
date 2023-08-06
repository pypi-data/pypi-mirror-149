# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flask_ninja']

package_data = \
{'': ['*']}

install_requires = \
['Flask>=1.1.2',
 'docstring-parser>=0.14.1,<0.15.0',
 'pydantic>=1.9.0,<2.0.0',
 'pytest-snapshot>=0.9.0,<0.10.0']

setup_kwargs = {
    'name': 'flask-ninja',
    'version': '1.1.0',
    'description': 'Flask Ninja is a web framework for building APIs with Flask and Python 3.9+ type hints.',
    'long_description': '# Flask Ninja\n\n**Flask Ninja** is a web framework for building APIs with Flask and Python 3.9+ type hints.\n\nKey features:\n\n- Easy: Designed to be easy to use and intuitive.\n- Fast to code: Type hints and automatic docs lets you focus only on business logic.\n- Standards-based: Based on the open standards for APIs: OpenAPI (previously known as Swagger) and JSON Schema.\n- Models based: Pydantic models support and automatic (de)serialization of requests/responses.\n- Secure: Natively supports various authentication methods for the requests.\n\n## Installation\n\n```\npip install flask-ninja\n```\n\n## Usage\n\nIn your flask project where you create flask app:\n\n```Python\nfrom flask import Flask\nfrom flask_ninja import NinjaAPI\nfrom pydantic import BaseModel\n\napp = Flask(__name__)\napi = NinjaAPI(app)\n\nclass Response(BaseModel):\n    """Response model containing results of various number operations."""\n    sum: int\n    difference: int\n    product: int\n    power: int\n\n@api.get("/compute")\ndef compute(a: int, b: int) -> Response:\n    """Computes results of various number operations.\n\n    This endpoint returns a result of the following operations:\n    - sum\n    - difference\n    - product\n    - power\n\n    :param int a: First number\n    :param int b: Second number number\n    """\n    return Response(\n        sum=a + b,\n        difference=a - b,\n        product=a * b,\n        power=a ** b\n    )\n\nif __name__ == "__main__":\n    app.run()\n```\n\n**That\'s it !**\n\nNow you\'ve just created an API that:\n\n- receives an HTTP GET request at `/compute`\n- takes, validates and type-casts GET parameters `a` and `b`\n- validates the returned Response object and serializes it into JSON\n- generates an OpenAPI schema for defined operation\n\n### Interactive API docs\n\nNow go to <a href="http://127.0.0.1:8000/docs" target="_blank">http://127.0.0.1:5000/docs</a>\n\nYou will see the automatic interactive API documentation (provided by <a href="https://github.com/swagger-api/swagger-ui" target="_blank">Swagger UI</a>):\n',
    'author': 'Michal Korbela',
    'author_email': 'michal.korbela@kiwi.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
