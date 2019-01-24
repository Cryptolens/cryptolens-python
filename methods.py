# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 08:06:39 2019

@author: Artem Los
"""

from helpers import Helpers
from models import *

class Key:
    
    def activate(token, product_id, key, machine_code, fields_to_return = 0,\
                 metadata = False, floating_time_interval = 0,\
                 max_overdraft = 0):
        
        response = Response.from_string(Helpers.send_request("key/activate", {"token":token,\
                                              "ProductId":product_id,\
                                              "key":key,\
                                              "MachineCode":machine_code,\
                                              "FieldsToReturn":fields_to_return,\
                                              "metadata":metadata,\
                                              "FloatingTimeInterval": floating_time_interval,\
                                              "MaxOverdraft": max_overdraft,\
                                              "Sign":"True",\
                                              "SignMethod":1}))
        if response.result == "1":
            return (None, response.message)
        else:
            return (LicenseKey.from_response(response), response.message)
        
        
    