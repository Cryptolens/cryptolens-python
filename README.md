# Cryptolens Client API for Python

This library contains helper methods to verify license keys in Python. 

## Installation

```
pip install licensing
```

## Example

### Key verification

The code below will work exactly as the one explained in the [key verification tutorial](https://help.cryptolens.io/examples/key-verification).

First, we need to add the namespaces:

```python
from licensing.helpers import Helpers
from licensing.models import Response, RSAPublicKey
from licensing.methods import Key
```

Now we can perform the actual key verification:

```python
pubKey = "<RSAKeyValue><Modulus>sGbvxwdlDbqFXOMlVUnAF5ew0t0WpPW7rFpI5jHQOFkht/326dvh7t74RYeMpjy357NljouhpTLA3a6idnn4j6c3jmPWBkjZndGsPL4Bqm+fwE48nKpGPjkj4q/yzT4tHXBTyvaBjA8bVoCTnu+LiC4XEaLZRThGzIn5KQXKCigg6tQRy0GXE13XYFVz/x1mjFbT9/7dS8p85n8BuwlY5JvuBIQkKhuCNFfrUxBWyu87CFnXWjIupCD2VO/GbxaCvzrRjLZjAngLCMtZbYBALksqGPgTUN7ZM24XbPWyLtKPaXF2i4XRR9u6eTj5BfnLbKAU5PIVfjIS+vNYYogteQ==</Modulus><Exponent>AQAB</Exponent></RSAKeyValue>"

res = Key.activate(token="WyIyNTU1IiwiRjdZZTB4RmtuTVcrQlNqcSszbmFMMHB3aWFJTlBsWW1Mbm9raVFyRyJd",\
                   rsa_pub_key=pubKey,\
                   product_id=3349, key="ICVLD-VVSZR-ZTICT-YKGXL", machine_code="test")

if res[0] == None:
    print("An error occured: {0}".format(res[1]))
else:
    print("Success")
```

* `pubKey` - the RSA public key (can be found [here](https://app.cryptolens.io/docs/api/v3/QuickStart#api-keys), in *API Keys* section).
* `token` - the access token (can be found [here](https://app.cryptolens.io/docs/api/v3/QuickStart#api-keys), in *API Keys* section).
* `product_id` - the id of the product can be found on the product page.
* `key` - the license key to be verified
* `machine_code` - the unique id of the device (we are working on adding a method similar to `Helpers.GetMachineCode()`).
