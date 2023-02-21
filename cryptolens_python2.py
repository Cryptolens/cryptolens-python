import datetime
import socket
import json

import os

"""
The code below should not be changed.
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 10:12:13 2019

@author: Artem Los
"""
import base64
import urllib2
import urllib
import hashlib
from subprocess import Popen, PIPE
from urllib2 import URLError, HTTPError

class HelperMethods:
    
    server_address = "https://app.cryptolens.io/api/"
    ironpython2730_legacy = False
    
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
        for _ in xrange(0, xLen):
            x, m = divmod(x, 256)
            Xrev.append(chr(m))
        return "".join(reversed(Xrev))

    @staticmethod
    def OS2IP(X):
        return int(X.encode("hex"), 16)
    
    @staticmethod
    def _OS2IP(X):
        x = 0
        a = 1
        l = len(X)
        for i in xrange(1, l+1):
            x += ord(X[l - i])*a
            a *= 256
        return x
	
    @staticmethod
    def RSAVP1((n,e), s):
        if s < 0 or n-1 < s:
            return None
        return pow(s, e, n)

    @staticmethod
    def EMSA_PKCS1_V15_ENCODE(M, emLen):
        import hashlib
        h = hashlib.sha256()
        h.update(M)
        H = h.digest()

        T = "".join([chr(x) for x in [0x30, 0x31, 0x30, 0x0d, 0x06, 0x09, 0x60, 0x86, 0x48, 0x01, 0x65, 0x03, 0x04, 0x02, 0x01, 0x05, 0x00, 0x04, 0x20]]) + H
        tLen = len(T)
        if emLen < tLen + 11:
            return None
        PS = "".join([chr(0xff) for _ in range(emLen - tLen - 3)])
        return "".join([chr(0x0), chr(0x1), PS, chr(0x0), T])

    @staticmethod
    def RSAASSA_PKCS1_V15_VERIFY((n,e), M, S):
        s = HelperMethods.OS2IP(S)
        m = HelperMethods.RSAVP1((n,e), s)
        if m is None: return False
        EM = HelperMethods.I2OSP(m, 256)
        if EM is None: return False
        EM2 = HelperMethods.EMSA_PKCS1_V15_ENCODE(M, 256)
        if EM2 is None: return False

        try:
            import hmac
            return hmac.compare_digest(EM, EM2)
        except (ImportError, AttributeError):
            return EM == EM2

    
    @staticmethod
    def verify_signature(response, rsaPublicKey):       
        """
        Verifies a signature from .NET RSACryptoServiceProvider.
        """
		
        modulus = base64.b64decode(rsaPublicKey.modulus)
        exponent = base64.b64decode(rsaPublicKey.exponent)
        message = base64.b64decode(response.license_key)
        signature = base64.b64decode(response.signature)

        n = HelperMethods.OS2IP(modulus)
        e = HelperMethods.OS2IP(exponent)

        return HelperMethods.RSAASSA_PKCS1_V15_VERIFY((n,e), message, signature)

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

        if HelperMethods.ironpython2730_legacy:
            return HelperMethods.send_request_ironpythonlegacy(HelperMethods.server_address + method, \
                                        urllib.urlencode(params))
        else:
            return urllib2.urlopen(HelperMethods.server_address + method, \
                                        urllib.urlencode(params)).read().decode("utf-8")

    @staticmethod
    def send_request_ironpythonlegacy(uri, parameters):
        """
        IronPython 2.7.3 and earlier has a built in problem with
        urlib2 library when verifying certificates. This code calls a .NET
        library instead.
        """
        from System.Net import WebRequest
        from System.IO import StreamReader
        from System.Text import Encoding

        request = WebRequest.Create(uri)
        
        request.ContentType = "application/x-www-form-urlencoded"
        request.Method = "POST" #work for post
        bytes = Encoding.ASCII.GetBytes(parameters)
        request.ContentLength = bytes.Length
        reqStream = request.GetRequestStream()
        reqStream.Write(bytes, 0, bytes.Length)
        reqStream.Close()
            
        response = request.GetResponse()
        result = StreamReader(response.GetResponseStream()).ReadToEnd()
        return result


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
    
import platform
import uuid
import sys
import json

class Key:
    
    """
    License key related methods. More docs: https://app.cryptolens.io/docs/api/v3/Key.
    """
    
    @staticmethod
    def activate(token, rsa_pub_key, product_id, key, machine_code, fields_to_return = 0,\
                 metadata = False, floating_time_interval = 0,\
                 max_overdraft = 0, friendly_name=None):
        
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
                                                  "FriendlyName" : friendly_name,\
                                                  "ModelVersion" : 2,\
                                                  "Sign":"True",\
                                                  "SignMethod":1}))
        except HTTPError as e:
            response = Response.from_string(e.read())
        except URLError as e:
            return (None, "Could not contact the server. Error message: " + str(e))
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
            return (None, "Could not contact the server. Error message: " + str(e))
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
            response = e.read()
        except URLError as e:
            return (None, "Could not contact the server. Error message: " + str(e))
        except Exception:
            return (None, "Could not contact the server.")
        
        jobj = json.loads(response)

        if jobj == None or not("result" in jobj) or jobj["result"] == 1:
            if jobj != None:
                return (None, jobj["message"])
            else:
               return (None, "Could not contact the server.")

        try:   
            return (jobj["key"], "")
        except:
            return (None, "An unexpected error occurred")
    
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
            response = e.read()
        except URLError as e:
            return (None, "Could not contact the server. Error message: " + str(e))
        except Exception:
            return (None, "Could not contact the server.")
        
        jobj = json.loads(response)

        if jobj == None or not("result" in jobj) or jobj["result"] == 1:
            if jobj != None:
                return (False, jobj["message"])
            else:
               return (False, "Could not contact the server.")
           
        return (True, "")

            
            
class Helpers:
    
    @staticmethod
    def GetMachineCode():
        
        """
        Get a unique identifier for this device.
        """
        
        if "windows" in platform.platform().lower():
            return HelperMethods.get_SHA256(HelperMethods.start_process(["cmd.exe", "/C", "wmic","csproduct", "get", "uuid"]))
        elif "darwin" in platform.platform().lower():               
            res = HelperMethods.start_process(["system_profiler","SPHardwareDataType"]).decode('utf-8')
            return HelperMethods.get_SHA256(res[res.index("UUID"):].strip())
        elif "linux" in platform.platform(HelperMethods.compute_machine_code()):
            return HelperMethods.get_SHA256(HelperMethods.compute_machine_code())
        else:
            return HelperMethods.get_SHA256(HelperMethods.compute_machine_code())
    
    @staticmethod
    def IsOnRightMachine(license_key, is_floating_license = False, allow_overdraft=False, custom_machine_code = None):
        
        """
        Check if the device is registered with the license key.
        """

        current_mid = ""
        
        if custom_machine_code == None:
            current_mid = Helpers.GetMachineCode()
        else:
            current_mid = custom_machine_code
        
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

import xml.etree.ElementTree
import json
import base64
import datetime
import copy
import time

class ActivatedMachine:
    def __init__(self, IP, Mid, Time, FriendlyName = ""):
        self.IP = IP
        self.Mid = Mid
        
        # TODO: check if time is int, and convert to datetime in this case.
        self.Time = Time
        self.FriendlyName = FriendlyName

class LicenseKey:
    
    def __init__(self, ProductId, ID, Key, Created, Expires, Period, F1, F2,\
                 F3, F4, F5, F6, F7, F8, Notes, Block, GlobalId, Customer, \
                 ActivatedMachines, TrialActivation, MaxNoOfMachines, \
                 AllowedMachines, DataObjects, SignDate, RawResponse):
        
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
        self.raw_response = RawResponse

    @staticmethod    
    def from_response(response):
        
        if response.result == "1":
            raise ValueError("The response did not contain any license key object since it was unsuccessful. Message '{0}'.".format(response.message))
        
        obj = json.loads(base64.b64decode(response.license_key).decode('utf-8'))
        
        return LicenseKey(obj["ProductId"], obj["ID"], obj["Key"], datetime.datetime.fromtimestamp(obj["Created"]),\
                          datetime.datetime.fromtimestamp(obj["Expires"]), obj["Period"], obj["F1"], obj["F2"], \
                          obj["F3"], obj["F4"],obj["F5"],obj["F6"], obj["F7"], \
                          obj["F8"], obj["Notes"], obj["Block"], obj["GlobalId"],\
                          obj["Customer"], LicenseKey.__load_activated_machines(obj["ActivatedMachines"]), obj["TrialActivation"], \
                          obj["MaxNoOfMachines"], obj["AllowedMachines"], obj["DataObjects"], \
                          datetime.datetime.fromtimestamp(obj["SignDate"]), response)
    
    def save_as_string(self):
        """
        Save the license as a string that can later be read by load_from_string.
        """
        res = copy.copy(self.raw_response.__dict__)
        res["licenseKey"] = res["license_key"]
        res.pop("license_key", None)
        return json.dumps(res)
    
    @staticmethod
    def load_from_string(rsa_pub_key, string, signature_expiration_interval = -1):
        """
        Loads a license from a string generated by save_as_string.
        Note: if an error occurs, None will be returned. An error can occur
        if the license string has been tampered with or if the public key is
        incorrectly formatted.
        
        :param signature_expiration_interval: If the license key was signed,
        this method will check so that no more than "signatureExpirationInterval" 
        days have passed since the last activation.
        """
        
        response = Response("","","","")
        
        try:
            response = Response.from_string(string)
        except Exception as ex:
            return None
        
        if response.result == "1":
            return None
        else:
            try:
                pubKey = RSAPublicKey.from_string(rsa_pub_key)
                if HelperMethods.verify_signature(response, pubKey):
                    
                    licenseKey = LicenseKey.from_response(response)
                    
                    if signature_expiration_interval > 0 and \
                    (licenseKey.sign_date + datetime.timedelta(days=1*signature_expiration_interval) < datetime.datetime.utcnow()):
                        return None
                    
                    return licenseKey
                else:
                    return None
            except Exception:
                return None

    @staticmethod        
    def __load_activated_machines(obj):
        
        if obj == None:
            return None
        
        arr = []
        
        for item in obj:
            arr.append(ActivatedMachine(**item))
        
        return arr

class Response:
    
    def __init__(self, license_key, signature, result, message):
        self.license_key = license_key
        self.signature = signature
        self.result = result
        self.message = message

    @staticmethod    
    def from_string(responseString):
        obj = json.loads(responseString)
        
        licenseKey = ""
        signature = ""
        result = 0
        message = ""
        
        if "licenseKey" in obj:
            licenseKey = obj["licenseKey"]
            
        if "signature" in obj:
            signature = obj["signature"]
        
        if "message" in obj:
            message = obj["message"]
            
        if "result" in obj:
            result = obj["result"]
        else:
            result = 1
        
        return Response(licenseKey, signature, result, message)

class RSAPublicKey:
    
    def __init__(self, modulus, exponent):
        self.modulus = modulus
        self.exponent = exponent

    @staticmethod 
    def from_string(rsaPubKeyString):
        """
        The rsaPubKeyString can be found at https://app.cryptolens.io/User/Security.
        It should be of the following format:
            <RSAKeyValue><Modulus>...</Modulus><Exponent>AQAB</Exponent></RSAKeyValue>
        """
        rsaKey = xml.etree.ElementTree.fromstring(rsaPubKeyString)
        return RSAPublicKey(rsaKey.find('Modulus').text, rsaKey.find('Exponent').text)
