# Cryptolens Client API for Python

[![Downloads](https://pepy.tech/badge/licensing)](https://pepy.tech/project/licensing)
[![Downloads](https://pepy.tech/badge/licensing/month)](https://pepy.tech/project/licensing)
[![Downloads](https://pepy.tech/badge/licensing/week)](https://pepy.tech/project/licensing)

This library contains helper methods to verify license keys in Python.

Python docs can be found here: https://help.cryptolens.io/api/python/

**Autodesk Maya**: The Python2 version needs to be used, as described [here](https://cryptolens.io/2019/07/autodesk-maya-plugin-software-licensing/).

**Autodesk Revit / Iron Python 2.7.3**: The Python2 version needs to be used with `HelperMethods.ironpython2730_legacy = True`.

> Please check out our guide about common errors and how to solve them: https://help.cryptolens.io/faq/index#troubleshooting-api-errors

## Installation

### Python 3
```
pip install licensing
```

### Python 2
Please copy `cryptolens_python2.py` file into your project folder. The entire library is contained in that file.
> In the examples below, please disregard the imports and use only the following one:

```python
from cryptolens_python2 import *
```

If you create a plugin for Autodesk Revit or use IronPython 2.7.3 or earlier, please also add the line below right after the import:

```python
HelperMethods.ironpython2730_legacy = True
```

## Example

### Key verification

The code below will work exactly as the one explained in the [key verification tutorial](https://help.cryptolens.io/examples/key-verification).

First, we need to add the namespaces:

In Python 3:
```python
from licensing.models import *
from licensing.methods import Key, Helpers
```

In Python 2:

```python
from cryptolens_python2 import *
```

Now we can perform the actual key verification:

```python
RSAPubKey = "<RSAKeyValue><Modulus>sGbvxwdlDbqFXOMlVUnAF5ew0t0WpPW7rFpI5jHQOFkht/326dvh7t74RYeMpjy357NljouhpTLA3a6idnn4j6c3jmPWBkjZndGsPL4Bqm+fwE48nKpGPjkj4q/yzT4tHXBTyvaBjA8bVoCTnu+LiC4XEaLZRThGzIn5KQXKCigg6tQRy0GXE13XYFVz/x1mjFbT9/7dS8p85n8BuwlY5JvuBIQkKhuCNFfrUxBWyu87CFnXWjIupCD2VO/GbxaCvzrRjLZjAngLCMtZbYBALksqGPgTUN7ZM24XbPWyLtKPaXF2i4XRR9u6eTj5BfnLbKAU5PIVfjIS+vNYYogteQ==</Modulus><Exponent>AQAB</Exponent></RSAKeyValue>"
auth = "WyIyNTU1IiwiRjdZZTB4RmtuTVcrQlNqcSszbmFMMHB3aWFJTlBsWW1Mbm9raVFyRyJd=="

result = Key.activate(token=auth,\
                   rsa_pub_key=RSAPubKey,\
                   product_id=3349, \
                   key="ICVLD-VVSZR-ZTICT-YKGXL",\
                   machine_code=Helpers.GetMachineCode(v=2))

if result[0] == None or not Helpers.IsOnRightMachine(result[0], v=2):
    # an error occurred or the key is invalid or it cannot be activated
    # (eg. the limit of activated devices was achieved)
    print("The license does not work: {0}".format(result[1]))
else:
    # everything went fine if we are here!
    print("The license is valid!")
    license_key = result[0]
    print("Feature 1: " + str(license_key.f1))
    print("License expires: " + str(license_key.expires))
```

* `RSAPubKey` - the RSA public key (can be found [here](https://app.cryptolens.io/docs/api/v3/QuickStart#api-keys), in *API Keys* section).
* `token` - the access token (can be found [here](https://app.cryptolens.io/docs/api/v3/QuickStart#api-keys), in *API Keys* section).
* `product_id` - the id of the product can be found on the product page.
* `key` - the license key to be verified
* `machine_code` - the unique id of the device.

**Note:** The code above assumes that node-locking is enabled. By default, license keys are created with _Maximum Number of Machines_ set to zero, which deactivates node-locking. As a result, machines will not be registered and the call to `Helpers.IsOnRightMachine(result[0])` will return `False`. You can read more about this behaviour [here](https://help.cryptolens.io/faq/index#maximum-number-of-machines).

### Offline activation (saving/loading licenses)

Assuming the license key verification was successful, we can save the result in a file so that we can use it instead of contacting Cryptolens.

```python
# res is obtained from the code above
if result[0] != None:
    # saving license file to disk
    with open('licensefile.skm', 'w') as f:
        f.write(result[0].save_as_string())
```

When loading it back, we can use the code below:

```python
# read license file from file
with open('licensefile.skm', 'r') as f:
    license_key = LicenseKey.load_from_string(pubKey, f.read())
    
    if license_key == None or not Helpers.IsOnRightMachine(license_key, v=2):
        print("NOTE: This license file does not belong to this machine.")
    else:
        print("Feature 1: " + str(license_key.f1))
        print("License expires: " + str(license_key.expires))
```

If you want to make sure that the license file is not too old, you can specify the maximum number of days as shown below (after 30 days, this method will return NoneType).

```python
# read license file from file
with open('licensefile.skm', 'r') as f:
    license_key = LicenseKey.load_from_string(pubKey, f.read(), 30)
    
    if license_key == None or not Helpers.IsOnRightMachine(license_key, v=2):
        print("NOTE: This license file does not belong to this machine.")
    else:
        print("Feature 1: " + str(license_key.f1))
        print("License expires: " + str(license_key.expires))
```

### Floating licenses
[Floating licenses](https://help.cryptolens.io/licensing-models/floating) can be enabled by setting the floatingTimeInterval. Optionally, you can also allow customers to exceed the bound by specifying the maxOverdraft.

The code below has a floatingTimeInterval of 300 seconds and maxOverdraft set to 1. To support floating licenses with overdraft, the call to `Helpers.IsOnRightMachine(license, true, true)` needs two boolean flags to be set to true.

```python
from licensing.models import *
from licensing.methods import Key, Helpers

RSAPubKey = "<RSAKeyValue><Modulus>sGbvxwdlDbqFXOMlVUnAF5ew0t0WpPW7rFpI5jHQOFkht/326dvh7t74RYeMpjy357NljouhpTLA3a6idnn4j6c3jmPWBkjZndGsPL4Bqm+fwE48nKpGPjkj4q/yzT4tHXBTyvaBjA8bVoCTnu+LiC4XEaLZRThGzIn5KQXKCigg6tQRy0GXE13XYFVz/x1mjFbT9/7dS8p85n8BuwlY5JvuBIQkKhuCNFfrUxBWyu87CFnXWjIupCD2VO/GbxaCvzrRjLZjAngLCMtZbYBALksqGPgTUN7ZM24XbPWyLtKPaXF2i4XRR9u6eTj5BfnLbKAU5PIVfjIS+vNYYogteQ==</Modulus><Exponent>AQAB</Exponent></RSAKeyValue>"
auth = "WyIyNTU1IiwiRjdZZTB4RmtuTVcrQlNqcSszbmFMMHB3aWFJTlBsWW1Mbm9raVFyRyJd=="

result = Key.activate(token=auth,\
                   rsa_pub_key=RSAPubKey,\
                   product_id=3349, \
                   key="ICVLD-VVSZR-ZTICT-YKGXL",\
                   machine_code=Helpers.GetMachineCode(v=2),\
                   floating_time_interval=300,\
                   max_overdraft=1)

if result[0] == None or not Helpers.IsOnRightMachine(res[0], is_floating_license=True, allow_overdraft=True, v=2):
    print("An error occurred: {0}".format(result[1]))
else:
    print("Success")
    
    license_key = result[0]
    print("Feature 1: " + str(license_key.f1))
    print("License expires: " + str(license_key.expires))
```

### Create Trial Key (verified trial)

#### Idea

A [trial key](https://help.cryptolens.io/examples/verified-trials) allows your users to evaluate some or all parts of your software for a limited period of time. The goal of trial keys is to set it up in such a way that you don’t need to manually create them, while still keeping everything secure.

In Cryptolens, all trial keys are bound to the device that requested them, which helps to prevent users from using the trial after reinstalling their device.

You can define which features should count as trial by [editing feature definitions](https://help.cryptolens.io/web-interface/feature-definitions) on the product page.

#### Implementation

The code below shows how to create trial key. If the trial key is successful, `trial_key[0]` will contain the license key string. We then need to call `Key.Activate` (as shown in the earlier examples) with the obtained license key to verify the license.

```python
from licensing.models import *
from licensing.methods import Key, Helpers

trial_key = Key.create_trial_key("WyIzODQ0IiwiempTRWs4SnBKTTArYUh3WkwyZ0VwQkVyeTlUVkRWK2ZTOS8wcTBmaCJd", 3941, Helpers.GetMachineCode(v=2))

if trial_key[0] == None:
    print("An error occurred: {0}".format(trial_key[1]))


RSAPubKey = "<RSAKeyValue><Modulus>sGbvxwdlDbqFXOMlVUnAF5ew0t0WpPW7rFpI5jHQOFkht/326dvh7t74RYeMpjy357NljouhpTLA3a6idnn4j6c3jmPWBkjZndGsPL4Bqm+fwE48nKpGPjkj4q/yzT4tHXBTyvaBjA8bVoCTnu+LiC4XEaLZRThGzIn5KQXKCigg6tQRy0GXE13XYFVz/x1mjFbT9/7dS8p85n8BuwlY5JvuBIQkKhuCNFfrUxBWyu87CFnXWjIupCD2VO/GbxaCvzrRjLZjAngLCMtZbYBALksqGPgTUN7ZM24XbPWyLtKPaXF2i4XRR9u6eTj5BfnLbKAU5PIVfjIS+vNYYogteQ==</Modulus><Exponent>AQAB</Exponent></RSAKeyValue>"
auth = "WyIyNTU1IiwiRjdZZTB4RmtuTVcrQlNqcSszbmFMMHB3aWFJTlBsWW1Mbm9raVFyRyJd=="

result = Key.activate(token=auth,\
                   rsa_pub_key=RSAPubKey,\
                   product_id=3349, \
                   key=trial_key[0],\
                   machine_code=Helpers.GetMachineCode(v=2))


if result[0] == None or not Helpers.IsOnRightMachine(result[0], v=2):
    print("An error occurred: {0}".format(result[1]))
else:
    print("Success")
    
    license_key = result[0]
    print("Feature 1: " + str(license_key.f1))
    print("License expires: " + str(license_key.expires))
```

### License server or custom endpoint

To forward requests to a local license server or a different API, you can set it using the `server_address` in HelperMethods, i.e.,

```python
HelperMethods.server_address = "http://localhost:8080/api/";
```
It is important to include one */* in the end of the address as well as to attach the "api" suffix.

### Other settings

#### Proxy

If you have customers who want to use a proxy server, we recommend enabling the following setting before calling any other API method, such as Key.Activate.

```python
HelperMethods.proxy_experimental = True
```

This will ensure that the underlying HTTP library (urllib) used by Cryptolens Python SDK will use the proxy configured on the OS level. The goal is to make this default behaviour in future versions of the library, once enough feedback is collected.

#### SSL verification
SSL verification can temporarily be disabled by adding the line below before any call to Key.Activate.

```python
HelperMethods.verify_SSL = False
```

The Cryptolens Python SDK will verify that the license information has not changed since it left the server using your RSA Public Key. However, we recommend to keep this value unchanged.
