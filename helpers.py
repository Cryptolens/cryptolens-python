# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 10:12:13 2019

@author: Artem Los
"""
import base64

class Helpers:
    
    def int2base64(num):
        return base64.b64encode(Helpers.pack_bigint(num))
    
    def base642int(string):
        return Helpers.unpack_bigint(base64.b64decode((string)))
    
    
    #https://stackoverflow.com/a/14764681/1275924
    def pack_bigint(i):
        b = bytearray()
        while i:
            b.append(i & 0xFF)
            i >>= 8
        return b
    
    def unpack_bigint(b):
        b = bytearray(b) # in case you're passing in a bytes/str
        return sum((1 << (bi*8)) * bb for (bi, bb) in enumerate(b)) 