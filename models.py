# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 09:47:26 2019

@author: Artem Los
"""
import xml.etree.ElementTree
import json

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
        