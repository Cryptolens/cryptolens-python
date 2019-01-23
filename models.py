# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 09:47:26 2019

@author: Artem Los
"""

class Response:
    
    def __init__(self, license_key, signature, result, message):
        self.license_key = license_key
        self.signature = signature
        self.result = result
        self.message = message
        
        
class RSAPublicKey:
    
    def __init__(self, modulus, exponent):
        self.modulus=modulus
        self.exponent = exponent
        
    def from_string(rsaPubKeyString):
        #TODO
        pass
        
        