# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 09:47:26 2019

@author: Artem Los
"""
import xml.etree.ElementTree
import json
import base64

class LicenseKey:
    
    def __init__(self, ProductId, ID, Key, Created, Expires, Period, F1, F2,\
                 F3, F4, F5, F6, F7, F8, Notes, Block, GlobalId, Customer, \
                 ActivatedMachines, TrialActivation, MaxNoOfMachines, \
                 AllowedMachines, DataObjects, SignDate):
        
        self.product_id = ProductId
        self.id = ID
        self.key = Key
        self.created = Created
        self.expires = Expires
        self.period = Period
        self.f1 = F1
        self.f2 = F2
        self.f3 = F3
        self.f4 = F4
        self.f5 = F5
        self.f6 = F6
        self.f7 = F7
        self.f8 = F8
        self.notes = Notes
        self.block = Block
        self.global_id = GlobalId
        self.customer = Customer
        self.activated_machines = ActivatedMachines
        self.trial_activation = TrialActivation
        self.max_no_of_machines = MaxNoOfMachines
        self.allowed_machines = AllowedMachines
        self.data_objects = DataObjects
        self.sign_date = SignDate
        
    def from_response(response):
        
        if response.result == "1":
            raise ValueError("The response did not contain any license key object since it was unsuccessful. Message '{0}'.".format(response.message))
        
        obj = json.loads(base64.b64decode(response.license_key).decode('utf-8'))
        
        return LicenseKey(obj["ProductId"], obj["ID"], obj["Key"], obj["Created"],\
                          obj["Expires"], obj["Period"], obj["F1"], obj["F2"], \
                          obj["F3"], obj["F4"],obj["F5"],obj["F6"], obj["F7"], \
                          obj["F8"], obj["Notes"], obj["Block"], obj["GlobalId"],\
                          obj["Customer"], obj["ActivatedMachines"], obj["TrialActivation"], \
                          obj["MaxNoOfMachines"], obj["AllowedMachines"], obj["DataObjects"], \
                          obj["SignDate"])

class Response:
    
    def __init__(self, license_key, signature, result, message):
        self.license_key = license_key
        self.signature = signature
        self.result = result
        self.message = message
        
    def from_string(responseString):        
        obj = json.loads(responseString)        
        return Response(obj["licenseKey"], obj["signature"], obj["result"],obj["message"])
        
class RSAPublicKey:
    
    def __init__(self, modulus, exponent):
        self.modulus=modulus
        self.exponent = exponent
        
    def from_string(rsaPubKeyString):
        """
        The rsaPubKeyString can be found at https://app.cryptolens.io/User/Security.
        It should be of the following format:
            <RSAKeyValue><Modulus>...</Modulus><Exponent>AQAB</Exponent></RSAKeyValue>
        """
        rsaKey = xml.etree.ElementTree.fromstring(rsaPubKeyString)
        return RSAPublicKey(rsaKey.find('Modulus').text, rsaKey.find('Exponent').text)
        