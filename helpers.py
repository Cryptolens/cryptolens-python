# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 10:12:13 2019

@author: Artem Los
"""
import base64
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

class Helpers:
    
    def verify_signature(response, rsaPublicKey):       
        """
        Verifies a signature from .NET RSACryptoServiceProvider.
        """
        cryptoPubKey = RSA.construct((Helpers.base642int(rsaPublicKey.modulus),\
                                      Helpers.base642int(rsaPublicKey.exponent)))
        h = SHA256.new(base64.b64decode(response.license_key.encode("utf-8")))
        verifier = PKCS1_v1_5.new(cryptoPubKey)
        return verifier.verify(h, base64.b64decode(response.signature.encode("utf-8")))
    
    
    def int2base64(num):
        return base64.b64encode(int.to_bytes(num), byteorder='big')
    
    def base642int(string):
        return int.from_bytes(base64.b64decode((string)), byteorder='big')
    