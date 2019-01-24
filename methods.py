# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 08:06:39 2019

@author: Artem Los
"""

from helpers import Helpers

class Key:
    
    def activate(token, product_id, key, machine_code, fields_to_return = 0,\
                 metadata = False, floating_time_interval = 0,\
                 max_overdraft = 0):
        
        return Helpers.send_request("key/activate", {"token":token,\
                                              "ProductId":product_id,\
                                              "key":key,\
                                              "MachineCode":machine_code,\
                                              "FieldsToReturn":fields_to_return,\
                                              "metadata":metadata,\
                                              "FloatingTimeInterval": floating_time_interval,\
                                              "MaxOverdraft": max_overdraft})
        
    