# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 08:06:39 2019

@author: Artem Los
"""

import platform
import uuid
import sys
from licensing.internal import HelperMethods
from licensing.models import *
import json

class AI:
    
    def get_events(token, limit=10, starting_after=None):
        
        """
        This method will retrieve events that were registered using Register event method.
        
        :param limit: Specifies how many events should be returned (default 10, max 100).
        :param starting_after: 	Works as a cursor (for pagination). If the last element had the id=125, then setting this to 125 will return all events coming after 125.
        """
        
        
        response = HelperMethods.send_request("ai/getevents", \
                                              {"token":token,\
                                               "limit":limit, \
                                               "startingafter":starting_after})
        
        jobj = json.loads(response)
        
        if jobj == None or jobj["result"] == "1":
            return None
        
        arr = []
        
        for item in jobj["events"]:
            arr.append(Event(**item))
        
        
        return arr
    
    
"""
class Product:
    
    def get_keys(token, product_id, page = 1, order_by = "ID ascending", search_query = ""):
        
        response = HelperMethods.send_request("product/getkeys", \
                                              {"token":token,\
                                               "productId": product_id, \
                                               "orderby":order_by, \
                                               "searchquery": search_query})
    
        jobj = json.loads(response)
        
        if jobj == None or jobj["result"] == "1":
            return None
        
"""        
    

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
    
        if response.result == 1:
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
        
        if "Windows" in platform.platform():
            return HelperMethods.get_SHA256(HelperMethods.start_process(["cmd.exe", "/C", "wmic","csproduct", "get", "uuid"]))
        elif "Mac" in platform.platform():               
            res = HelperMethods.start_process(["system_profiler","SPHardwareDataType"]).decode('utf-8')
            HelperMethods.get_SHA256(res[res.index("UUID"):].strip())
        elif "Linux" in platform.platform():
            return HelperMethods.get_SHA256(HelperMethods.start_process(["dmidecode", "-s", "system-uuid"]))
        else:
            return HelperMethods.get_SHA256(HelperMethods.start_process(["dmidecode", "-s", "system-uuid"]).decode('utf-8'))
    
    def IsOnRightMachine(license_key, is_floating_license = False, allow_overdraft=False):
        
        """
        Check if the device is registered with the license key.
        """
        
        current_mid = Helpers.GetMachineCode()
        
        if license_key.activated_machines == None:
            return False
        
        if is_floating_license:
            if len(license_key.activated_machines) == 1 and \
            (license_key.activated_machines[0].Mid[9:] == current_mid or \
             allow_overdraft and license_key.activated_machines[0].Mid[19:] == current_mid):
                return True
        else:
            for act_machine in license_key.activated_machines:
                if current_mid == act_machine.Mid:
                    return True
            
        return False
        