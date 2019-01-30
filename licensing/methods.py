# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 08:06:39 2019

@author: Artem Los
"""

import platform
import sys
from licensing.internal import HelperMethods
from licensing.models import *

class Key:
    
    """
    License key related methods. More docs: https://app.cryptolens.io/docs/api/v3/Key.
    """
    
    def activate(token, rsa_pub_key, product_id, key, machine_code, fields_to_return = 0,\
                 metadata = False, floating_time_interval = 0,\
                 max_overdraft = 0):
        
        """
        Calls the Activate method in Web API 3 and returns a tuple containing
        (LicenseKey, Message). If an error occurs, LicenseKey will be None. If
        everything went well, no message will be returned.
        
        More docs: https://app.cryptolens.io/docs/api/v3/Activate
        """
        
        response = Response("","","","")
        
        try:
            response = Response.from_string(HelperMethods.send_request("key/activate", {"token":token,\
                                                  "ProductId":product_id,\
                                                  "key":key,\
                                                  "MachineCode":machine_code,\
                                                  "FieldsToReturn":fields_to_return,\
                                                  "metadata":metadata,\
                                                  "FloatingTimeInterval": floating_time_interval,\
                                                  "MaxOverdraft": max_overdraft,\
                                                  "Sign":"True",\
                                                  "SignMethod":1}))
        except Exception:
            return (None, "Could not contact the server.")
        
        pubkey = RSAPublicKey.from_string(rsa_pub_key)
    
        if response.result == "1":
            return (None, response.message)
        else:
            try:
                if HelperMethods.verify_signature(response, pubkey):
                    return (LicenseKey.from_response(response), response.message)
                else:
                    return (None, "The signature check failed.")
            except Exception:
                return (None, "The signature check failed.")
            
            
class Helpers:
    
    def GetMachineCode():
        
        """
        Get a unique identifier for this device.
        """
        
        res = []
        res.append(platform.machine())
        res.append(platform.machine())
        res.append(platform.processor())
        res.append(platform.system())
        res.append(platform.architecture()[1])
        # safer than using architecture()[0]
        # see https://docs.python.org/3/library/platform.html#platform.architecture
        res.append(str(sys.maxsize > 2**32))
        
        return HelperMethods.get_SHA256(":".join(res))
    
    def IsOnRightMachine(license_key):
        
        """
        Check if the device is registered with the license key.
        """
        
        current_mid = Helpers.GetMachineCode()
        
        if license_key.activated_machines == None:
            return False
        
        for act_machine in license_key.activated_machines:
            
            if current_mid == act_machine.Mid:
                return True
            
        return False
        