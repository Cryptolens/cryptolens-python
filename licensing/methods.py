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
from urllib.error import URLError, HTTPError

class Key:
    
    """
    License key related methods. More docs: https://app.cryptolens.io/docs/api/v3/Key.
    """
    
    @staticmethod
    def activate(token, rsa_pub_key, product_id, key, machine_code, fields_to_return = 0,\
                 metadata = False, floating_time_interval = 0,\
                 max_overdraft = 0):
        
        """
        Calls the Activate method in Web API 3 and returns a tuple containing
        (LicenseKey, Message). If an error occurs, LicenseKey will be None. If
        everything went well, no message will be returned.
        
        More docs: https://app.cryptolens.io/docs/api/v3/Activate
        """
        
        response = Response("","",0,"")
        
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
        except HTTPError as e:
            response = Response.from_string(e.read())
        except URLError as e:
            return (None, "Could not contact the server. Error message: " + e.reason)
        except Exception:
            return (None, "Could not contact the server. Error message: " + e.reason)
        
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
            
    @staticmethod
    def get_key(token, rsa_pub_key, product_id, key, fields_to_return = 0,\
                 metadata = False, floating_time_interval = 0):
        
        """
        Calls the GetKey method in Web API 3 and returns a tuple containing
        (LicenseKey, Message). If an error occurs, LicenseKey will be None. If
        everything went well, no message will be returned.
        
        More docs: https://app.cryptolens.io/docs/api/v3/GetKey
        """
        
        response = Response("","",0,"")
        
        try:
            response = Response.from_string(HelperMethods.send_request("key/getkey", {"token":token,\
                                                  "ProductId":product_id,\
                                                  "key":key,\
                                                  "FieldsToReturn":fields_to_return,\
                                                  "metadata":metadata,\
                                                  "FloatingTimeInterval": floating_time_interval,\
                                                  "Sign":"True",\
                                                  "SignMethod":1}))
        except HTTPError as e:
            response = Response.from_string(e.read())
        except URLError as e:
            return (None, "Could not contact the server. Error message: " + e.reason)
        except Exception:
            return (None, "Could not contact the server. Error message: " + e.reason)
        
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
     
    @staticmethod
    def create_trial_key(token, product_id, machine_code):
        """
        Calls the CreateTrialKey method in Web API 3 and returns a tuple containing
        (LicenseKeyString, Message). If an error occurs, LicenseKeyString will be None. If
        everything went well, no message will be returned.
        
        More docs: https://app.cryptolens.io/docs/api/v3/CreateTrialKey
        """
        
        response = ""
        
        try:
            response = HelperMethods.send_request("key/createtrialkey", {"token":token,\
                                                  "ProductId":product_id,\
                                                  "MachineCode":machine_code})
        except HTTPError as e:
            response = Response.from_string(e.read())
        except URLError as e:
            return (None, "Could not contact the server. Error message: " + e.reason)
        except Exception:
            return (None, "Could not contact the server. Error message: " + e.reason)
        
        jobj = json.loads(response)

        if jobj == None or not("result" in jobj) or jobj["result"] == 1:
            if jobj != None:
                return (None, jobj["message"])
            else:
               return (None, "Could not contact the server.")
           
        return (jobj["key"], "")
    
    @staticmethod
    def deactivate(token, product_id, key, machine_code, floating = False):
        """
        Calls the Deactivate method in Web API 3 and returns a tuple containing
        (Success, Message). If an error occurs, Success will be False. If
        everything went well, Sucess is true and no message will be returned.
        
        More docs: https://app.cryptolens.io/docs/api/v3/Deactivate
        """
        
        response = ""
        
        try:
            response = HelperMethods.send_request("key/deactivate", {"token":token,\
                                                  "ProductId":product_id,\
                                                  "Key" : key,\
                                                  "Floating" : floating,\
                                                  "MachineCode":machine_code})
        except HTTPError as e:
            response = Response.from_string(e.read())
        except URLError as e:
            return (None, "Could not contact the server. Error message: " + e.reason)
        except Exception:
            return (None, "Could not contact the server. Error message: " + e.reason)
        
        jobj = json.loads(response)

        if jobj == None or not("result" in jobj) or jobj["result"] == 1:
            if jobj != None:
                return (False, jobj["message"])
            else:
               return (False, "Could not contact the server.")
           
        return (True, "")

            
            
class Helpers:
    
    @staticmethod
    def GetMachineCode(v=1):
        
        """
        Get a unique identifier for this device. If you want the machine code to be the same in .NET on Windows, you
        can set v=2. More information is available here: https://help.cryptolens.io/faq/index#machine-code-generation
        """
        
        if "windows" in platform.platform().lower():
            return HelperMethods.get_SHA256(HelperMethods.start_process(["cmd.exe", "/C", "wmic","csproduct", "get", "uuid"],v))
        elif "mac" in platform.platform().lower() or "darwin" in platform.platform().lower():               
            res = HelperMethods.start_process(["system_profiler","SPHardwareDataType"])
            return HelperMethods.get_SHA256(res[res.index("UUID"):].strip())
        elif "linux" in platform.platform().lower() :
            return HelperMethods.get_SHA256(HelperMethods.compute_machine_code())
        else:
            return HelperMethods.get_SHA256(HelperMethods.compute_machine_code())
    
    @staticmethod
    def IsOnRightMachine(license_key, is_floating_license = False, allow_overdraft=False, v = 1):
        
        """
        Check if the device is registered with the license key.
        The version parameter is related to the one in GetMachineCode method.
        """
        
        current_mid = Helpers.GetMachineCode(v)
        
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
        