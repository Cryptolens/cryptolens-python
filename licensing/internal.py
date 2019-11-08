# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 10:12:13 2019

@author: Artem Los
"""
import base64
import urllib.request
import hashlib
from subprocess import Popen, PIPE

class HelperMethods:
    
    server_address = "https://app.cryptolens.io/api/"
    
    @staticmethod
    def get_SHA256(string):
        """
        Compute the SHA256 signature of a string.
        """
        return hashlib.sha256(string.encode("utf-8")).hexdigest()
    
    @staticmethod
    def I2OSP(x, xLen):
        if x > (1 << (8 * xLen)):
            return None
        Xrev = []
        for _ in range(0, xLen):
            x, m = divmod(x, 256)
            Xrev.append(m)
        return bytes(reversed(Xrev))
    
    @staticmethod
    def OS2IP(X):
        import binascii
        h = binascii.hexlify(X)
        return int(h, 16)
       
    @staticmethod
    def RSAVP1(pair, s):
        n, e = pair
        if s < 0 or n-1 < s:
            return None
        return pow(s, e, n)
    
    @staticmethod
    def EMSA_PKCS1_V15_ENCODE(M, emLen):
        import hashlib
        h = hashlib.sha256()
        h.update(M)
        H = h.digest()
    
        T = bytes([0x30, 0x31, 0x30, 0x0d, 0x06, 0x09, 0x60, 0x86, 0x48, 0x01, 0x65, 0x03, 0x04, 0x02, 0x01, 0x05, 0x00, 0x04, 0x20]) + H
        tLen = len(T)
        if emLen < tLen + 11:
            return None
            PS = bytes([0xff for _ in range(emLen - tLen - 3)])
        return b"".join([b"\x00\x01", PS, b"\x00", T])

    @staticmethod
    def RSAASSA_PKCS1_V15_VERIFY(pair, M, S):
        n, e = pair
        s = OS2IP(S)
        m = RSAVP1((n,e), s)
        if m is None: return False
        EM = I2OSP(m, 256)
        if EM is None: return False
        EM2 = EMSA_PKCS1_V15_ENCODE(M, 256)  # Can return None, but it's OK since EM is not None
        return EM == EM2
    
    @staticmethod
    def verify_signature(response, rsaPublicKey):       
        """
        Verifies a signature from .NET RSACryptoServiceProvider.
        """
        
        n = OS2IP(base64.b64decode(rsaPublicKey.modulus))
        e = OS2IP(base64.b64decode(rsaPublicKey.exponent))
        
        message = base64.b64decode(response.license_key.encode("utf-8"))
        response = base64.b64decode(response.signature.encode("utf-8"))
        
        return RSAASSA_PKCS1_V15_VERIFY((n,e), message, signature)
    
    @staticmethod
    def int2base64(num):
        return base64.b64encode(int.to_bytes(num), byteorder='big')
    
    @staticmethod
    def base642int(string):
        return int.from_bytes(base64.b64decode((string)), byteorder='big')
    
    @staticmethod
    def send_request(method, params):
        """
        Send a POST request to method in the Web API with the specified
        params and return the response string.
        
            method: the path of the method, eg. key/activate
            params: a dictionary of parameters
        """    
        return urllib.request.urlopen(HelperMethods.server_address + method, \
                                      urllib.parse.urlencode(params)\
                                      .encode("utf-8")).read().decode("utf-8")
        
    @staticmethod 
    def start_process(command):
        
        process = Popen(command, stdout=PIPE)
        (output, err) = process.communicate()
        exit_code = process.wait()
        return output.decode("utf-8")

    @staticmethod
    def get_dbus_machine_id():
        try:
            with open("/etc/machine-id") as f:
                return f.read().strip()
        except:
            pass
        try:
            with open("/var/lib/dbus/machine-id") as f:
                return f.read().strip()
        except:
            pass
        return ""

    @staticmethod
    def get_inodes():
        import os
        files = ["/bin", "/etc", "/lib", "/root", "/sbin", "/usr", "/var"]
        inodes = []
        for file in files:
            try:
                inodes.append(os.stat(file).st_ino)
            except: 
                pass
        return "".join([str(x) for x in inodes])

    @staticmethod
    def compute_machine_code():
        return HelperMethods.get_dbus_machine_id() + HelperMethods.get_inodes()
    