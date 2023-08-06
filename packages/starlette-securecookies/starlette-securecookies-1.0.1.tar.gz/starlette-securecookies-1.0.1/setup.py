# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['securecookies']

package_data = \
{'': ['*']}

install_requires = \
['cryptograpy>=0.0.0,<0.0.1', 'starlette>=0.6.1']

setup_kwargs = {
    'name': 'starlette-securecookies',
    'version': '1.0.1',
    'description': 'Secure cookie middleware for Starlette applications.',
    'long_description': '# starlette-securecookies\n\n![GitHub Workflow Status](https://img.shields.io/github/workflow/status/thearchitector/starlette-securecookies/CI?label=tests&style=flat-square)\n![PyPI - Downloads](https://img.shields.io/pypi/dw/starlette-securecookies?style=flat-square)\n![GitHub](https://img.shields.io/github/license/thearchitector/starlette-securecookies?style=flat-square)\n[![Buy a tree](https://img.shields.io/badge/Treeware-%F0%9F%8C%B3-lightgreen?style=flat-square)](https://ecologi.com/eliasgabriel?r=6128126916bfab8bd051026c)\n\nCustomizable middleware for adding automatic cookie encryption and decryption to Starlette applications.\n\n## How it works?\n\n```mermaid\nsequenceDiagram\n    Browser->>+Middleware: Encrypted cookies\n    Middleware->>+Application: Filtered / Decrypted cookies\n    Application->>-Middleware: Plaintext cookies\n    Middleware->>-Browser: Encrypted \'Set-Cookie\' headers\n```\n\nFor any incoming cookies:\n\n1. Requests sent from the client\'s browser to your application are intercepted by `SecureCookiesMiddleware`.\n2. All `Cookie` headers are parsed and filter. Only cookies in the `included_cookies` and `excluded_cookies` parameters are parsed. All cookies are included by default.\n3. The cookies are decrypted. If cookie cannot be decrypted, or is otherwise invalid, it is discarded by default (`discard_invalid=True`).\n4. Any included and valid encrypted cookies in the ASGI request scope are replaced by the decrypted ones.\n5. The request scope is passed to any future middleware, and eventually your application. Cookies can be read normally anywhere downstream.\n\nFor any outgoing cookies:\n\n7. Your application sets cookies with `response.set_cookie` as usual.\n8. All responses returned by your application are intercepted by `SecureCookiesMiddleware`.\n9. Cookies in the `included_cookies` and `excluded_cookies` parameters are re-encrypted, and their attributes (like `"SameSite"` and `"HttpOnly"`) are overridden by the parameters set in `SecureCookiesMiddleware`.\n10. The cookies in the response are replaced by the re-encrypted cookies, and the response is propagated to Starlette to return to the client\'s browser.\n\n## Installation\n\n```sh\n$ poetry add starlette-securecookies\n# or\n$ python -m pip install --user starlette-securecookies\n```\n\n## Usage\n\nThis is a Starlette-based middleware, so it can be used in any Starlette application or Starlette-based application (like [FastAPI](https://fastapi.tiangolo.com/advanced/middleware/) or [Starlite](https://starlite-api.github.io/starlite/usage/7-middleware/)).\n\nFor example,\n\n```python\nfrom starlette.applications import Starlette\nfrom starlette.middleware import Middleware\n\nfrom securecookies import SecureCookiesMiddleware\n\nmiddleware = [\n    Middleware(\n        SecureCookiesMiddleware, secrets=["SUPER SECRET SECRET"]\n    )\n]\n\napp = Starlette(routes=..., middleware=middleware)\n```\n\n## License\n\nThis software is licensed under the [BSD 3-Clause License](LICENSE).\n\nThis package is Treeware. If you use it in production, consider buying the world a tree to thank me for my work. By contributing to my forest, you’ll be creating employment for local families and restoring wildlife habitats.\n',
    'author': 'Elias Gabriel',
    'author_email': 'me@eliasfgabriel.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/thearchitector/starlette-securecookies',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
