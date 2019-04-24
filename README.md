# Cryptolens Client API for Python

This library contains helper methods to verify license keys in Python.

Python docs can be found here: https://help.cryptolens.io/api/python/

## Installation

```
pip install licensing
```

## Example

### Key verification

The code below will work exactly as the one explained in the [key verification tutorial](https://help.cryptolens.io/examples/key-verification).

First, we need to add the namespaces:

```python
from licensing.models import *
from licensing.methods import Key, Helpers
```

Now we can perform the actual key verification:

```python
pubKey = "<RSAKeyValue><Modulus>sGbvxwdlDbqFXOMlVUnAF5ew0t0WpPW7rFpI5jHQOFkht/326dvh7t74RYeMpjy357NljouhpTLA3a6idnn4j6c3jmPWBkjZndGsPL4Bqm+fwE48nKpGPjkj4q/yzT4tHXBTyvaBjA8bVoCTnu+LiC4XEaLZRThGzIn5KQXKCigg6tQRy0GXE13XYFVz/x1mjFbT9/7dS8p85n8BuwlY5JvuBIQkKhuCNFfrUxBWyu87CFnXWjIupCD2VO/GbxaCvzrRjLZjAngLCMtZbYBALksqGPgTUN7ZM24XbPWyLtKPaXF2i4XRR9u6eTj5BfnLbKAU5PIVfjIS+vNYYogteQ==</Modulus><Exponent>AQAB</Exponent></RSAKeyValue>"

res = Key.activate(token="WyIyNTU1IiwiRjdZZTB4RmtuTVcrQlNqcSszbmFMMHB3aWFJTlBsWW1Mbm9raVFyRyJd",\
                   rsa_pub_key=pubKey,\
                   product_id=3349, key="ICVLD-VVSZR-ZTICT-YKGXL", \
                   machine_code=Helpers.GetMachineCode())

if res[0] == None or not Helpers.IsOnRightMachine(res[0]):
    print("An error occurred: {0}".format(res[1]))
else:
    print("Success")
    
    license_key = res[0]
    print("Feature 1: " + str(license_key.f1))
    print("License expires: " + str(license_key.expires))
```

* `pubKey` - the RSA public key (can be found [here](https://app.cryptolens.io/docs/api/v3/QuickStart#api-keys), in *API Keys* section).
* `token` - the access token (can be found [here](https://app.cryptolens.io/docs/api/v3/QuickStart#api-keys), in *API Keys* section).
* `product_id` - the id of the product can be found on the product page.
* `key` - the license key to be verified
* `machine_code` - the unique id of the device.

### Offline activation (saving/loading licenses)

Assuming the license key verification was successful, we can save the result in a file so that we can use it instead of contacting Cryptolens.

```python
# res is obtained from the code above
if res[0] != None:
    # saving license file to disk
    with open('licensefile.skm', 'w') as f:
        f.write(res[0].save_as_string())
```

When loading it back, we can use the code below:

```python
# read license file from file
with open('licensefile.skm', 'r') as f:
    license_key = LicenseKey.load_from_string(pubKey, f.read(), 30)
    
    if license_key != None not Helpers.IsOnRightMachine(license_key):
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
    
    if license_key != None not Helpers.IsOnRightMachine(license_key):
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

pubKey = "<RSAKeyValue><Modulus>sGbvxwdlDbqFXOMlVUnAF5ew0t0WpPW7rFpI5jHQOFkht/326dvh7t74RYeMpjy357NljouhpTLA3a6idnn4j6c3jmPWBkjZndGsPL4Bqm+fwE48nKpGPjkj4q/yzT4tHXBTyvaBjA8bVoCTnu+LiC4XEaLZRThGzIn5KQXKCigg6tQRy0GXE13XYFVz/x1mjFbT9/7dS8p85n8BuwlY5JvuBIQkKhuCNFfrUxBWyu87CFnXWjIupCD2VO/GbxaCvzrRjLZjAngLCMtZbYBALksqGPgTUN7ZM24XbPWyLtKPaXF2i4XRR9u6eTj5BfnLbKAU5PIVfjIS+vNYYogteQ==</Modulus><Exponent>AQAB</Exponent></RSAKeyValue>"

res = Key.activate(token="WyIyNjA1IiwiTjhZQUpIYXJPaVdBV0ozQUlKVC9tamdDbFZDRzhZRHpaU243L2R2eCJd",\
                   rsa_pub_key=pubKey,\
                   product_id=3349, key="MTMPW-VZERP-JZVNZ-SCPZM", \
                   machine_code=Helpers.GetMachineCode(),\
                   floating_time_interval=300,\
                   max_overdraft=1)

if res[0] == None or not Helpers.IsOnRightMachine(res[0], is_floating_license=True, allow_overdraft=True):
    print("An error occurred: {0}".format(res[1]))
else:
    print("Success")
    
    license_key = res[0]
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

trial_key = Key.create_trial_key("WyIzODQ0IiwiempTRWs4SnBKTTArYUh3WkwyZ0VwQkVyeTlUVkRWK2ZTOS8wcTBmaCJd", 3941, Helpers.GetMachineCode())

if trial_key[0] == None:
    print("An error occurred: {0}".format(trial_key[1]))


pubKey = "<RSAKeyValue><Modulus>sGbvxwdlDbqFXOMlVUnAF5ew0t0WpPW7rFpI5jHQOFkht/326dvh7t74RYeMpjy357NljouhpTLA3a6idnn4j6c3jmPWBkjZndGsPL4Bqm+fwE48nKpGPjkj4q/yzT4tHXBTyvaBjA8bVoCTnu+LiC4XEaLZRThGzIn5KQXKCigg6tQRy0GXE13XYFVz/x1mjFbT9/7dS8p85n8BuwlY5JvuBIQkKhuCNFfrUxBWyu87CFnXWjIupCD2VO/GbxaCvzrRjLZjAngLCMtZbYBALksqGPgTUN7ZM24XbPWyLtKPaXF2i4XRR9u6eTj5BfnLbKAU5PIVfjIS+vNYYogteQ==</Modulus><Exponent>AQAB</Exponent></RSAKeyValue>"

res = Key.activate(token="WyIyNTU1IiwiRjdZZTB4RmtuTVcrQlNqcSszbmFMMHB3aWFJTlBsWW1Mbm9raVFyRyJd",\
                   rsa_pub_key=pubKey,\
                   product_id=3941, key=trial_key[0], \
                   machine_code=Helpers.GetMachineCode())

if res[0] == None or not Helpers.IsOnRightMachine(res[0]):
    print("An error occurred: {0}".format(res[1]))
else:
    print("Success")
    
    license_key = res[0]
    print("Feature 1: " + str(license_key.f1))
    print("License expires: " + str(license_key.expires))
```
