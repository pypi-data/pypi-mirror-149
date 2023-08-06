# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_api']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0', 'defusedxml>=0.7.1,<0.8.0', 'pytest>=7.1.1,<8.0.0']

setup_kwargs = {
    'name': 'pytest-api',
    'version': '0.1.3',
    'description': 'An ASGI middleware to populate OpenAPI Specification examples from pytest functions',
    'long_description': '# PyTest-API: Populate OpenAPI Examples from Python Tests\n\n![purpose](https://img.shields.io/badge/purpose-testing-green.svg)\n![PyPI](https://img.shields.io/pypi/v/pytest-api.svg)\n\nPyTest-API is an [ASGI middleware](https://asgi.readthedocs.io/en/latest/specs/main.html#middleware) that populates [OpenAPI-Specification](https://github.com/OAI/OpenAPI-Specification/) examples from [pytest](https://pypi.org/project/pytest/) functions. \n\n\n## Installation\n\n```\npoetry add --dev pytest-api\n```\n\n## How to use it:\n\nStarting with `test_main.py` file: \n\n```python\nfrom .main import spec\n\n\n@spec.describe(route="/behavior-example/")\ndef test_example_body(client):\n    """\n    GIVEN behavior in body\n    WHEN example behavior endpoint is called with POST method\n    THEN response with status 200 and body OK is returned\n    """\n    assert client.post(\n        "/behavior-example/", json={"name": "behavior"},\n        headers={"spec-example": test_example_body.id}\n    ).json() == {"message": "OK"}\n```\n\nImpliment solution in `/main.py` file:\n\n```python\nfrom fastapi import FastAPI\nfrom pydantic import BaseModel\n\nfrom pytest_api import ASGIMiddleware\n\napp = FastAPI()\nspec = ASGIMiddleware\n\napp.add_middleware(spec)\n\napp.openapi = spec.openapi_behaviors(app)\n\n\nclass Behavior(BaseModel):\n    name: str\n\n\n@app.post("/behavior-example/")\nasync def example_body(behavior: Behavior):\n    return {"message": "OK"}\n```\n\nRun FastAPI app:\n```bash\npoetry run uvicorn test_app.main:app --reload\n```\n\nOpen your browser to http://localhost:8000/docs#/ too find the doc string is populated into the description.\n\n![Your doc string will now be populated into the description.](./OpenAPI.png)\n\n## Implimentation Details\n\nUnder the hood the `ASGIMiddleware` uses the `describe` decorator to store the `pytest` function by its `id`: \n\n```python\ndef wrap_behavior(*args, **kwargs):\n                try:\n                    BEHAVIORS[route]\n                except KeyError as e:\n                    if route in e.args:\n                        BEHAVIORS[route] = {str(id(func)): func}\n                BEHAVIORS[route][str(id(func))] = func\n```\n\nWhen `pytest` calls your API the `SpecificationResponder` is looking for the coresponding `id` in the `headers` of the request:\n\n```python\n    def handle_spec(self, headers):\n        behaviors = BEHAVIORS[self.path]\n        self.should_update_example = headers.get("spec-example", "") in behaviors\n        self.should_update_description = (\n            headers.get("spec-description", "") in behaviors\n        )\n\n        if self.should_update_example:\n            self.func = behaviors[headers.get("spec-example")]\n        elif self.should_update_description:\n            self.func = behaviors[headers.get("spec-description")]\n```\n\nThis is possible thanks to python\'s first-class `functions` i.e. [Closure_(computer_programming)](https://en.wikipedia.org/wiki/Closure_(computer_programming)).',
    'author': 'Andrew Sturza',
    'author_email': 'sturzaam@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sturzaam/pytest-api',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
