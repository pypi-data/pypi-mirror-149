# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['requests_http_message_signatures']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=1.8.2', 'requests>=2,<3']

setup_kwargs = {
    'name': 'requests-http-message-signatures',
    'version': '0.3.1',
    'description': 'A request authentication plugin implementing IETF HTTP Message Signatures',
    'long_description': '# requests-http-message-signatures: A Requests auth module for HTTP Signature\n\n**requests-http-message-signatures** is a [Requests](https://github.com/requests/requests) \n[authentication plugin](http://docs.python-requests.org/en/master/user/authentication/>) \n(`requests.auth.AuthBase` subclass) implementing the \n[IETF HTTP Signatures draft RFC](https://tools.ietf.org/html/draft-richanna-http-message-signatures). It has no\nrequired dependencies outside the standard library. If you wish to use algorithms other than HMAC (namely, RSA and\nECDSA algorithms specified in the RFC), there is an optional dependency on\n[cryptography](https://pypi.python.org/pypi/cryptography).\n\n## Installation\n\n```\n$ pip install requests-http-message-signatures\n```\n\n## Usage\n\n```\n  import requests\n  from requests_http_signature import HTTPSignatureAuth\n  \n  preshared_key_id = \'squirrel\'\n  preshared_secret = \'monorail_cat\'\n  url = \'http://example.com/path\'\n  \n  requests.get(url, auth=HTTPSignatureAuth(key=preshared_secret, key_id=preshared_key_id))\n```\n\nBy default, only the `Date` header is signed (as per the RFC) for body-less requests such as GET. The `Date` header\nis set if it is absent. In addition, for requests with bodies (such as POST), the `Digest` header is set to the SHA256\nof the request body and signed (an example of this appears in the RFC). To add other headers to the signature, pass an\narray of header names in the `headers` keyword argument.\n\nIn addition to signing messages in the client, the class method `HTTPSignatureAuth.verify()` can be used to verify\nincoming requests:\n\n```\n  def key_resolver(key_id, algorithm):\n      return \'monorail_cat\'\n\n  HTTPSignatureAuth.verify(request, key_resolver=key_resolver)\n```\n\n### Asymmetric key algorithms (RSA and ECDSA)\n\nFor asymmetric key algorithms, you should supply the private key as the `key` parameter to the `HTTPSignatureAuth()` \nconstructor as bytes in the PEM format:\n\n```\n  with open(\'key.pem\', \'rb\') as fh:\n      requests.get(url, auth=HTTPSignatureAuth(algorithm="rsa-sha256", key=fh.read(), key_id=preshared_key_id))\n```\n\nWhen verifying, the `key_resolver()` callback should provide the public key as bytes in the PEM format as well.\n\n## Links\n\n* [IETF HTTP Signatures draft](https://tools.ietf.org/html/draft-richanna-http-message-signatures)\n* [Project home page](https://dev.funkwhale.audio/funkwhale/requests-http-message-signatures)\n* [Package distribution (PyPI)](https://pypi.org/project/requests-http-message-signatures/)\n* [Based on requests-http-signature](https://github.com/pyauth/requests-http-signature)\n\n## Bugs\n\nPlease report bugs, issues, feature requests, etc. on our [issue tracker](https://dev.funkwhale.audio/funkwhale/requests-http-message-signatures/-/issues).\n\n## License\n\nLicensed under the terms of the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0).\n',
    'author': 'Andrey Kislyuk',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://dev.funkwhale.audio/funkwhale/requests-http-message-signatures',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
