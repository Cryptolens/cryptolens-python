# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 09:34:40 2019

@author: Artem Los
"""

from licensing.models import *
from licensing.methods import Key, Helpers, AI

pubKey = "<RSAKeyValue><Modulus>sGbvxwdlDbqFXOMlVUnAF5ew0t0WpPW7rFpI5jHQOFkht/326dvh7t74RYeMpjy357NljouhpTLA3a6idnn4j6c3jmPWBkjZndGsPL4Bqm+fwE48nKpGPjkj4q/yzT4tHXBTyvaBjA8bVoCTnu+LiC4XEaLZRThGzIn5KQXKCigg6tQRy0GXE13XYFVz/x1mjFbT9/7dS8p85n8BuwlY5JvuBIQkKhuCNFfrUxBWyu87CFnXWjIupCD2VO/GbxaCvzrRjLZjAngLCMtZbYBALksqGPgTUN7ZM24XbPWyLtKPaXF2i4XRR9u6eTj5BfnLbKAU5PIVfjIS+vNYYogteQ==</Modulus><Exponent>AQAB</Exponent></RSAKeyValue>"

res = Key.activate(token="WyIyNzMyIiwiYmx6NlJ6ZzdaWjFScmxFVFNCc283YTJyUG5kQURMZ0hucW1YdUZxKyJd",\
                   rsa_pub_key=pubKey,\
                   product_id=3349, key="ICVLD-VVSZR-ZTICT-YKGXL", machine_code=Helpers.GetMachineCode())

if res[0] == None or not Helpers.IsOnRightMachine(res[0]):
    print("An error occured: {0}".format(res[1]))
else:
    print("Success")
    
    license_key = res[0]
    print("Feature 1: " + str(license_key.f1))
    print("License expires: " + str(license_key.expires))
    
    
if res[0] != None:
    # saving license file to disk
    with open('licensefile.skm', 'w') as f:
        f.write(res[0].save_as_string())
        

# read license file from file
with open('licensefile.skm', 'r') as f:
    license_key = LicenseKey.load_from_string(pubKey, f.read())
    
    if not Helpers.IsOnRightMachine(license_key):
        print("NOTE: This license file does not belong to this machine.")
    else:
        print("Feature 1: " + str(license_key.f1))
        print("License expires: " + str(license_key.expires))
    
print(Helpers.GetMachineCode())


#a = AI.get_events("WyIyOTk0Iiwid1ZZUUU4bVEyd2Z1VCtGL05aREpQb0p4VEkxYThRbEw1aGRpUHg3ZiJd")