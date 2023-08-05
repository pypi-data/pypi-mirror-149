# requests-http-message-signatures: A Requests auth module for HTTP Signature

**requests-http-message-signatures** is a [Requests](https://github.com/requests/requests) 
[authentication plugin](http://docs.python-requests.org/en/master/user/authentication/>) 
(`requests.auth.AuthBase` subclass) implementing the 
[IETF HTTP Signatures draft RFC](https://tools.ietf.org/html/draft-richanna-http-message-signatures). It has no
required dependencies outside the standard library. If you wish to use algorithms other than HMAC (namely, RSA and
ECDSA algorithms specified in the RFC), there is an optional dependency on
[cryptography](https://pypi.python.org/pypi/cryptography).

## Installation

```
$ pip install requests-http-message-signatures
```

## Usage

```
  import requests
  from requests_http_signature import HTTPSignatureAuth
  
  preshared_key_id = 'squirrel'
  preshared_secret = 'monorail_cat'
  url = 'http://example.com/path'
  
  requests.get(url, auth=HTTPSignatureAuth(key=preshared_secret, key_id=preshared_key_id))
```

By default, only the `Date` header is signed (as per the RFC) for body-less requests such as GET. The `Date` header
is set if it is absent. In addition, for requests with bodies (such as POST), the `Digest` header is set to the SHA256
of the request body and signed (an example of this appears in the RFC). To add other headers to the signature, pass an
array of header names in the `headers` keyword argument.

In addition to signing messages in the client, the class method `HTTPSignatureAuth.verify()` can be used to verify
incoming requests:

```
  def key_resolver(key_id, algorithm):
      return 'monorail_cat'

  HTTPSignatureAuth.verify(request, key_resolver=key_resolver)
```

### Asymmetric key algorithms (RSA and ECDSA)

For asymmetric key algorithms, you should supply the private key as the `key` parameter to the `HTTPSignatureAuth()` 
constructor as bytes in the PEM format:

```
  with open('key.pem', 'rb') as fh:
      requests.get(url, auth=HTTPSignatureAuth(algorithm="rsa-sha256", key=fh.read(), key_id=preshared_key_id))
```

When verifying, the `key_resolver()` callback should provide the public key as bytes in the PEM format as well.

## Links

* [IETF HTTP Signatures draft](https://tools.ietf.org/html/draft-richanna-http-message-signatures)
* [Project home page](https://dev.funkwhale.audio/funkwhale/requests-http-message-signatures)
* [Package distribution (PyPI)](https://pypi.org/project/requests-http-message-signatures/)
* [Based on requests-http-signature](https://github.com/pyauth/requests-http-signature)

## Bugs

Please report bugs, issues, feature requests, etc. on our [issue tracker](https://dev.funkwhale.audio/funkwhale/requests-http-message-signatures/-/issues).

## License

Licensed under the terms of the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0).
