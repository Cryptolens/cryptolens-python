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
                 max_overdraft = 0, friendly_name = None):
        
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
                                                  "ModelVersion": 3 ,\
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
                    if metadata:
                        
                        try:
                            metadata_s = HelperMethods.verify_signature_metadata(response.metadata["signature"], pubkey)
                        
                            if metadata_s[0]:
                                return (LicenseKey.from_response(response), response.message, json.loads(metadata_s[1]))
                            else:
                                return (LicenseKey.from_response(response), response.message, "Signature check for metadata object failed.")
                        except:
                            return (LicenseKey.from_response(response), response.message, "Signature check for metadata object failed.")

                                
                    else:
                        return (LicenseKey.from_response(response), response.message)
                else:
                    return (None, "The signature check failed.")
            except Exception as ex:
                return (None, "An error occured: {0}".format(ex))
            
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
                                                  "ModelVersion": 3 ,\
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
    def create_trial_key(token, product_id, machine_code, friendly_name= ""):
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
                                                  "MachineCode":machine_code,\
                                                  "FriendlyName":friendly_name})
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
           
        return (jobj["key"], "")
    
    @staticmethod
    def create_key(token, product_id, period = 0,\
                   f1=False,\
                   f2=False,\
                   f3=False,\
                   f4=False,\
                   f5=False,\
                   f6=False,\
                   f7=False,\
                   f8=False,\
                   notes="",\
                   block=False,\
                   customer_id=0,\
                   new_customer=False,\
                   add_or_use_existing_customer=False,\
                   trial_activation=False,\
                   max_no_of_machines=0,\
                   no_of_keys=1,\
                   name = None,\
                   email = None,\
                   company_name=None,\
                   enable_customer_association = False,\
                   allow_activation_management = False ):
        """
        This method allows you to create a new license key. The license can
        either be standalone or associated to a specific customer. It is also
        possible to add a new customer and associate it with the newly created
        license using NewCustomer parameter. If you would like to avoid
        duplicates based on the email, you can use the AddOrUseExistingCustomer
        parameter.
        
        The parameters "name", "email", "company_name", "enable_customer_association"
        and "allow_activation_management" are used to create a new customer (or update an existing one)
        and automatically associate it with the newly created license. Please note that you need to use an
        access token with both "CreateKey" and "AddCustomer" permissions. Moreover, either
        the parameter "new_customer" or "add_or_use_existing_customer" need to be set to True.
        
        More docs: https://app.cryptolens.io/docs/api/v3/CreateKey/
        """
        
        response = ""
        
        try:
            response = HelperMethods.send_request("key/createkey", {"token":token,\
                                                  "ProductId":product_id,\
                                                  "Period":period,\
                                                  "F1": f1,\
                                                  "F2": f2,\
                                                  "F3": f3,\
                                                  "F4": f4,\
                                                  "F5": f5,\
                                                  "F6": f6,\
                                                  "F7": f7,\
                                                  "F8": f8,\
                                                  "Notes": notes,\
                                                  "Block": block,\
                                                  "CustomerId": customer_id,\
                                                  "NewCustomer": new_customer,\
                                                  "AddOrUseExistingCustomer": add_or_use_existing_customer,\
                                                  "TrialActivation": trial_activation,\
                                                  "MaxNoOfMachines": max_no_of_machines,\
                                                  "NoOfKeys":no_of_keys,\
                                                  "Name": name,\
                                                  "Email": email,\
                                                  "CompanyName": company_name,\
                                                  "EnableCustomerAssociation": enable_customer_association,\
                                                  "AllowActivationManagement": allow_activation_management})
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
           
        return (jobj, "")
    
    
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
    
    
    @staticmethod
    def extend_license(token, product_id, key, no_of_days):
        """
        This method will extend a license by a certain amount of days.
        If the key algorithm in the product is SKGL, the key string will
        be changed if necessary. Otherwise, if SKM15 is used, the key will
        stay the same. More about the way this method works in Remarks.
        
        More docs: https://app.cryptolens.io/docs/api/v3/ExtendLicense
        """
        
        response = ""
        
        try:
            response = HelperMethods.send_request("key/ExtendLicense", {"token":token,\
                                                  "ProductId":product_id,\
                                                  "Key" : key,\
                                                  "NoOfDays" : no_of_days})
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
           
        return (True, jobj["message"])
    
    @staticmethod
    def change_customer(token, product_id, key, customer_id):
        """
        This method will change the customer associated with a license.
        If the customer is not specified (for example, if CustomerId=0) or
        the customer with the provided ID does not exist, any customer that
        was previously associated with the license will be dissociated.
        
        More docs: https://app.cryptolens.io/docs/api/v3/ChangeCustomer
        """
        
        response = ""
        
        try:
            response = HelperMethods.send_request("key/ChangeCustomer", {"token":token,\
                                                  "ProductId":product_id,\
                                                  "Key" : key,\
                                                  "CustomerId" : customer_id})
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
           
        return (True, jobj["message"])
    
    @staticmethod
    def unblock_key(token, product_id, key):
        """
        This method will unblock a specific license key to ensure that it can
        be accessed by the Key.Activate method.
        To do the reverse, you can use the BlockKey method.
        
        More docs: https://app.cryptolens.io/docs/api/v3/UnblockKey
        """
        
        response = ""
        
        try:
            response = HelperMethods.send_request("/key/UnblockKey", {"token":token,\
                                                  "ProductId":product_id,\
                                                  "Key" : key})
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
           
        return (True, jobj["message"])
    
    def block_key(token, product_id, key):
        """
        This method will block a specific license key to ensure that it will
        no longer be possible to activate it. Note, it will still be possible
        to access the license key using the GetKey method.
        To do the reverse, you can use the Unblock Key method.
        
        More docs: https://app.cryptolens.io/docs/api/v3/BlockKey
        """
        
        response = ""
        
        try:
            response = HelperMethods.send_request("/key/BlockKey", {"token":token,\
                                                  "ProductId":product_id,\
                                                  "Key" : key})
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
           
        return (True, jobj["message"])
    
    def machine_lock_limit(token, product_id, key, number_of_machines):
        """
        This method will change the maximum number of machine codes that
        a license key can have.
        
        More docs: https://app.cryptolens.io/docs/api/v3/MachineLockLimit
        """
        
        response = ""
        
        try:
            response = HelperMethods.send_request("/key/MachineLockLimit", {"token":token,\
                                                  "ProductId":product_id,\
                                                  "Key" : key,\
                                                  "NumberOfMachines": number_of_machines})
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
           
        return (True, jobj["message"])
    
    def change_notes(token, product_id, key, notes):
        """
        This method will change the content of the notes field of
        a given license key.
        
        More docs: https://app.cryptolens.io/docs/api/v3/ChangeNotes
        """
        
        response = ""
        
        try:
            response = HelperMethods.send_request("/key/ChangeNotes", {"token":token,\
                                                  "ProductId":product_id,\
                                                  "Key" : key,\
                                                  "Notes": notes})
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
           
        return (True, jobj["message"])
    
    def change_reseller(token, product_id, key, reseller_id):
        """
        This method will change the reseller of a license. If the reseller is
        not specified (for example, if ResellerId=0) or the reseller with the
        provided ID does not exist, any reseller that was previously associated
        with the license will be dissociated.
        
        More docs: https://app.cryptolens.io/docs/api/v3/ChangeReseller
        """
        
        response = ""
        
        try:
            response = HelperMethods.send_request("/key/ChangeReseller", {"token":token,\
                                                  "ProductId":product_id,\
                                                  "Key" : key,\
                                                  "ResellerId": reseller_id})
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
           
        return (True, jobj["message"])
    
    def create_key_from_template(token, license_template_id):
        """
        This method will create a license key based on a License Template.
        If you want to see all the defined license templates through the API,
        this can be accomplished with Get License Templates. An alternative is
        to call the Create Key method, which allows you to specify all the
        parameters yourself. Note: the "feature lock" field in the access token
        can be used to restrict which license tempalte id can be used.
        
        More docs: https://app.cryptolens.io/docs/api/v3/CreateKeyFromTemplate
        """
        
        response = ""
        
        try:
            response = HelperMethods.send_request("/key/CreateKeyFromTemplate", {"token":token,\
                                                  "LicenseTemplateId": license_template_id})
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
           
        return (jobj["key"], jobj["rawResponse"], jobj["message"])
    
    def add_feature(token, product_id, key, feature):
        """
        This method will set a certain feature (F1..F8) to true.
        If the key algorithm in the product is SKGL, the key string will be
        changed if necessary. Otherwise, if SKM15 is used, the key will stay 
        the same. To do the reverse, please see RemoveFeature.
        
        More docs: https://app.cryptolens.io/docs/api/v3/AddFeature
        """
        
        response = ""
        
        try:
            response = HelperMethods.send_request("/key/AddFeature", {"token":token,\
                                                  "ProductId":product_id,\
                                                  "Key" : key,\
                                                  "Feature" : feature})
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
           
        return (True, jobj["message"])
    
    def remove_feature(token, product_id, key, feature):
        """
        This method will set a certain feature (F1..F8) to false. If the key
        algorithm in the product is SKGL, the key string will be changed if
        necessary. Otherwise, if SKM15 is used, the key will stay the same.
        To do the reverse, please see AddFeature.
        
        More docs: https://app.cryptolens.io/docs/api/v3/RemoveFeature
        """
        
        response = ""
        
        try:
            response = HelperMethods.send_request("/key/RemoveFeature", {"token":token,\
                                                  "ProductId":product_id,\
                                                  "Key" : key,\
                                                  "Feature" : feature})
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
           
        return (True, jobj["message"])

class AI:
    
    @staticmethod
    def get_web_api_log(token, product_id = 0, key = "", machine_code="", friendly_name = "",\
                        limit = 10, starting_after = 0, ending_before=0, order_by=""):
        
        """
        This method will retrieve a list of Web API Logs. All events that get
        logged are related to a change of a license key or data object, eg. when
        license key gets activated or when a property of data object changes. More details
        about the method that was called are specified in the State field.
        
        More docs: https://app.cryptolens.io/docs/api/v3/GetWebAPILog
        """
        
        response = ""
                
        try:
            response = HelperMethods.send_request("ai/getwebapilog", {"token":token,\
                                                  "ProductId":product_id,\
                                                  "Key":key,\
                                                  "MachineCode":machine_code,\
                                                  "FriendlyName":friendly_name,\
                                                  "Limit": limit,\
                                                  "StartingAfter": starting_after,\
                                                  "OrderBy" : order_by,\
                                                  "EndingBefore": ending_before})
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
           
        return (jobj["logs"], "")

    @staticmethod
    def get_events(token, limit = 10, starting_after = 0, product_id = 0,\
                        key = "", metadata = ""):
        
        """
        This method will retrieve events that were registered using Register event method.
        
        More docs: https://app.cryptolens.io/api/ai/GetEvents
        """
        
        response = ""
                
        try:
            response = HelperMethods.send_request("ai/GetEvents", {"token":token,\
                                                  "ProductId":product_id,\
                                                  "Key" : key,\
                                                  "Limit": limit,\
                                                  "StartingAfter": starting_after})
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
           
        return (jobj["events"], "")
    
    @staticmethod
    def register_event(token, product_id=0, key="", machine_code="", feature_name ="",\
                       event_name="", value=0, currency="", metadata=""):
        """
        This method will register an event that has occured in either
        the client app (eg. start of a certain feature or interaction
        within a feature) or in a third party provider (eg. a payment
        has occured, etc).

        Note: You can either use this method standalone (eg. by only
        providing a machine code/device identifier) or together with
        Cryptolens Licensing module (which requires productId and
        optionally keyid to be set). The more information that is
        provided, the better insights can be provided.
        
        More docs: https://app.cryptolens.io/api/ai/RegisterEvent
        """
        
        response = ""
        
        try:
            response = HelperMethods.send_request("/ai/RegisterEvent", {"token":token,\
                                                  "ProductId":product_id,\
                                                  "Key" : key,\
                                                  "MachineCode" : machine_code,\
                                                  "FeatureName" : feature_name,\
                                                  "EventName": event_name,\
                                                  "Value" : value,\
                                                  "Currency": currency,\
                                                  "Metadata" : metadata})
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
           
        return (True, jobj["message"])
            
class Message:
    
    @staticmethod
    def get_messages(token, channel="", time=0):
        
        """
        This method will return a list of messages that were broadcasted.
        You can create new messages here. Messages can be filtered based on the time and the channel.
        
        More docs: https://app.cryptolens.io/docs/api/v3/GetMessages
        """
        
        try:
            response = HelperMethods.send_request("/message/getmessages/", {"token":token, "Channel": channel, "Time": time})
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

        return (jobj["messages"], "")
    
    
    def create_message(token, content="", channel="", time=0):
        
        """
        This method will create a new message.
        This method requires Edit Messages permission.
        
        More docs: https://app.cryptolens.io/docs/api/v3/CreateMessage
        """
        
        try:
            response = HelperMethods.send_request("/message/CreateMessage/", {"token":token, "Channel": channel,"Content":content, "Time": time})
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

        return (jobj["messageId"], "")
    
    def remove_message(token, messageId):
        
        """
        This method will remove a message that was previously broadcasted.
        This method requires Edit Messages permission.
        
        More docs: https://app.cryptolens.io/docs/api/v3/RemoveMessage
        """
        
        try:
            response = HelperMethods.send_request("/message/RemoveMessage/", {"token":token, "Id": messageId})
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

        return (True, "")
    
    
class Product:
    
    @staticmethod
    def get_products(token):
        
        """
        This method will return the list of products. Each product contains fields such as
        the name and description, as well feature definitions and data objects. All the fields
        of a product are available here: https://app.cryptolens.io/docs/api/v3/model/Product
        
        More docs: https://app.cryptolens.io/docs/api/v3/GetProducts
        """
        
        try:
            response = HelperMethods.send_request("/product/getproducts/", {"token":token})
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

        return (jobj["products"], "")
    
    @staticmethod
    def get_keys(token, product_id, page = 1, order_by="ID ascending", search_query=""):
        
        """
        This method will return a list of keys for a given product.
        Please keep in mind that although each license key will be
        of the License Key type, the fields related to signing operations
        will be left empty. Instead, if you want to get a signed license key
        (for example, to achieve offline key activation), please use the
        Activation method instead.
        
        More docs: https://app.cryptolens.io/docs/api/v3/GetKeys
        """
        
        try:
            response = HelperMethods.send_request("/product/getkeys/",\
                                                  {"token":token,\
                                                   "ProductId" : product_id,\
                                                   "Page" : page,\
                                                   "OrderBy" : order_by,\
                                                   "SearchQuery" : search_query\
                                                   })
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

        return (jobj["licenseKeys"], "", {"returned":jobj["returned"], "total":jobj["total"], "pageCount":jobj["pageCount"]})
    
    
class Customer:
    
    @staticmethod
    def add_customer(token, name = "", email = "", company_name="",\
                     enable_customer_association = False,\
                     allow_activation_management = False ):
        
        """
        This method will add new customer.
        
        More docs: https://app.cryptolens.io/docs/api/v3/AddCustomer
        """
        
        try:
            response = HelperMethods.send_request("/customer/addcustomer/",\
                                                  {"token":token,\
                                                   "Name": name,\
                                                   "Email": email,\
                                                   "CompanyName": company_name,\
                                                   "EnableCustomerAssociation": enable_customer_association,\
                                                   "AllowActivationManagement": allow_activation_management
                                                   })
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

        return (jobj, "")
    
    @staticmethod
    def get_customer_licenses(token, customer_id, detailed=False, metadata=False):
        
        """
        This method will return a list of license keys that belong to a certain customer.
        
        More docs: https://app.cryptolens.io/docs/api/v3/GetCustomerLicenses
        """
        
        try:
            response = HelperMethods.send_request("/customer/GetCustomerLicenses/",\
                                                  {"token":token,\
                                                   "customerId" : customer_id,\
                                                   "detailed" : detailed,\
                                                   "metadata" : metadata
                                                   })
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

        return (jobj, "")
    
    @staticmethod
    def get_customer_licenses_by_secret(token, secret, detailed=False, metadata=False):
        
        """
        This method will return a list of license keys that belong to a certain customer.
        
        More docs: https://app.cryptolens.io/docs/api/v3/GetCustomerLicenses
        """
        
        try:
            response = HelperMethods.send_request("/customer/GetCustomerLicensesBySecret/",\
                                                  {"token":token,\
                                                   "secret" : secret,\
                                                   "detailed" : detailed,\
                                                   "metadata" : metadata
                                                   })
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

        return (jobj, "")
            
            
class Data:
    
    """
    Data object related methods
    """
    
    @staticmethod
    def increment_int_value_to_key(token, product_id, key, object_id=0, name = "",\
                                   int_value=0, enable_bound=False, bound=0):
        
        """
        This method will increment the int value of a data object associated with a license key.
        
        When creating an access token to this method, remember to include "IncrementIntValue" permission and 
        set the "Lock to key" value to -1.

        Note: either an object_id or name (provided there are no duplicates) is required.
        
        More docs: https://app.cryptolens.io/docs/api/v3/IncrementIntValue (see parameters under Method 2)
        """
        
        try:
            response = HelperMethods.send_request("/data/IncrementIntValueToKey/",\
                                                  {"token":token,\
                                                   "ProductId" : product_id,\
                                                   "Key" : key,\
                                                   "Id" : object_id,\
                                                   "Name" : name,\
                                                   "IntValue": int_value ,\
                                                   "EnableBound": str(enable_bound),\
                                                   "Bound" : bound
                                                   })
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

        return (jobj, "")

    @staticmethod
    def decrement_int_value_to_key(token, product_id, key, object_id=0, name="",\
                                   int_value=0, enable_bound=False, bound=0):
        
        """
        This method will decrement the int value of a data object associated with a license key.
        
        When creating an access token to this method, remember to include "DecrementIntValue" permission and 
        set the "Lock to key" value to -1.

        Note: either an object_id or name (provided there are no duplicates) is required.
        
        More docs: https://app.cryptolens.io/docs/api/v3/DecrementIntValue (see parameters under Method 2)
        """
        
        try:
            response = HelperMethods.send_request("/data/DecrementIntValueToKey/",\
                                                  {"token":token,\
                                                   "ProductId" : product_id,\
                                                   "Key" : key,\
                                                   "Id" : object_id,\
                                                   "Name" : name,\
                                                   "IntValue": int_value ,\
                                                   "EnableBound": str(enable_bound),\
                                                   "Bound" : bound
                                                   })
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

        return (jobj, "")

    @staticmethod
    def add_data_object_to_key(token, product_id, key, name = "", string_value="",\
                                   int_value=0, check_for_duplicates=False):
        
        """
        This method will add a new Data Object to a license key.
        
        More docs: https://app.cryptolens.io/docs/api/v3/AddDataObject (see parameters under Method 2)
        """
        
        try:
            response = HelperMethods.send_request("/data/AddDataObjectToKey/",\
                                                  {"token":token,\
                                                   "ProductId" : product_id,\
                                                   "Key" : key,\
                                                   "Name" : name,\
                                                   "IntValue": int_value ,\
                                                   "StringValue": string_value ,\
                                                   "CheckForDuplicates" : str(check_for_duplicates)
                                                   })
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

        return (jobj, "")
    
    @staticmethod
    def remove_data_object_to_key(token, product_id, key, object_id=0, name = ""):
        
        """
        This method will add a new Data Object to a license key.
        
        Note: either an object_id or name (provided there are no duplicates) is required.
        
        More docs: https://app.cryptolens.io/docs/api/v3/RemoveDataObject (see parameters under Method 2)
        """
        
        try:
            response = HelperMethods.send_request("/data/RemoveDataObjectToKey/",\
                                                  {"token":token,\
                                                   "ProductId" : product_id,\
                                                   "Key" : key,\
                                                   "Name" : name,\
                                                   "Id": object_id })
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

        return (jobj, "")

    @staticmethod
    def add_data_object_to_machine(token, product_id, key, machine_code, name = "", string_value="",\
                                   int_value=0, check_for_duplicates=False):
        
        """
        This method will add a new Data Object to Machine.
        
        More docs: https://app.cryptolens.io/docs/api/v3/AddDataObject (see parameters under Method 3)
        """
        
        try:
            response = HelperMethods.send_request("/data/AddDataObjectToMachineCode/",\
                                                  {"token":token,\
                                                   "ProductId" : product_id,\
                                                   "Key" : key,\
                                                   "Name" : name,\
                                                   "IntValue": int_value ,\
                                                   "StringValue": string_value ,\
                                                   "CheckForDuplicates" : str(check_for_duplicates), \
                                                   "MachineCode": machine_code
                                                   })
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

        return (jobj, "")

    @staticmethod
    def remove_data_object_to_machine(token, product_id, key, machine_code, object_id=0, name = ""):
        
        """
        This method will remove existing Data Object from Machine Code.
        
        More docs: https://app.cryptolens.io/docs/api/v3/RemoveDataObject (see parameters under Method 3)
        """
        
        try:
            response = HelperMethods.send_request("/data/RemoveDataObjectToMachineCode/",\
                                                  {"token":token,\
                                                   "ProductId" : product_id,\
                                                   "Key" : key,\
                                                   "MachineCode": machine_code,\
                                                   "Name" : name,\
                                                   "Id": object_id })
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

        return (jobj, "")

    @staticmethod
    def list_machine_data_objects(token, product_id, key, machine_code, \
                                  name_contains=""):
        
        """
        This method will list Data Objects for Machine.
        
        More docs: https://app.cryptolens.io/docs/api/v3/ListDataObjects (see parameters under Method 3)
        """
        
        try:
            response = HelperMethods.send_request("/data/ListDataObjectsToMachineCode/",\
                                                  {"token":token,\
                                                   "ProductId" : product_id,\
                                                   "Key" : key,\
                                                   "MachineCode": machine_code,\
                                                   "Contains": name_contains
                                                   })
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

        return (jobj, "")

    @staticmethod
    def list_key_data_objects(token, product_id, key, \
                                  name_contains=""):
        
        """
        This method will list Data Objects for License Key.
        
        More docs: https://app.cryptolens.io/docs/api/v3/ListDataObjects (see parameters under Method 2)
        """
        
        try:
            response = HelperMethods.send_request("/data/ListDataObjectsToKey/",\
                                                  {"token":token,\
                                                   "ProductId" : product_id,\
                                                   "Key" : key,\
                                                   "Contains": name_contains
                                                   })
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

        return (jobj, "")
    
    
class PaymentForm:
    
    @staticmethod
    def create_session(token, payment_form_id, currency, expires, price=None,\
                       heading = None, product_name = None, custom_field='',\
                       metadata = None):
        
        
        """
        This method will create a new session for a Payment Form.
        It allows you to customize appearance of the form (such as price, heading, etc).
        You should only create new sessions from a server side (i.e. never directly from your application).
        Note, session will only work once and it will eventually expire depending on Expires parameter.
        
        More docs: https://app.cryptolens.io/docs/api/v3/PFCreateSession
        """
        
        try:
            response = HelperMethods.send_request("/paymentform/CreateSession/",\
                                                  {"token":token,\
                                                   "PaymentFormId" : payment_form_id,\
                                                   "Price" : price,\
                                                   "Currency" : currency,\
                                                   "Heading": heading ,\
                                                   "ProductName": product_name,\
                                                   "CustomField" : custom_field,\
                                                   "Metadata" : metadata,\
                                                   "Expires" : expires,\
                                                   })
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

        return (jobj, "")

class Helpers:


    def __read_registry_value(key, subkey, value_name):

        import winreg

        """
        Reads a value from the Windows Registry.

        Parameters:
        key (int): The registry root key (e.g., winreg.HKEY_LOCAL_MACHINE).
        subkey (str): The path to the subkey.
        value_name (str): The name of the value to read.

        Returns:
        str: The value read from the registry, or an error message if not found.
        """
        try:
            # Open the registry key
            registry_key = winreg.OpenKey(key, subkey, 0, winreg.KEY_READ)
            
            # Query the value
            value, reg_type = winreg.QueryValueEx(registry_key, value_name)
            
            # Close the registry key
            winreg.CloseKey(registry_key)
            
            return value
        
        except FileNotFoundError:
            return None
        except Exception as e:
            return None #str(e)
        
    
    @staticmethod
    def GetMachineCode(v=1):
        
        """
        Get a unique identifier for this device. If you want the machine code to be the same in .NET on Windows, you
        can set v=2. More information is available here: https://help.cryptolens.io/faq/index#machine-code-generation
        
        Note: if we are unable to compute the machine code, None will be returned. Please make sure
        to check this in production code.
        """
        
        if "windows" in platform.platform().lower():

            import winreg

            seed = ""
            
            if v==2:
                seed = HelperMethods.start_process_ps_v2()
            else:
                seed = HelperMethods.start_process(["cmd.exe", "/C", "wmic","csproduct", "get", "uuid"],v)
            
            if seed == "" or seed == None:
                machineGUID = Helpers.__read_registry_value(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Cryptography", "MachineGuid")
                
                if machineGUID != None and machineGUID != "":
                    return HelperMethods.get_SHA256(machineGUID)
                return None
            else:
                return HelperMethods.get_SHA256(seed)
            
            
        elif "mac" in platform.platform().lower() or "darwin" in platform.platform().lower():               
            res = HelperMethods.start_process(["system_profiler","SPHardwareDataType"])
            seed = res[res.index("UUID"):].strip()
            
            if seed == "":
                return None
            else:
                return HelperMethods.get_SHA256(seed)
            
        elif "linux" in platform.platform().lower() :
            seed = HelperMethods.compute_machine_code()
            if seed == "":
                return None
            else:
                return HelperMethods.get_SHA256(seed)
        else:
            seed = HelperMethods.compute_machine_code()
            if seed == "":
                return None
            else:
                return HelperMethods.get_SHA256(seed)
    
    @staticmethod
    def IsOnRightMachine(license_key, is_floating_license = False, allow_overdraft=False, v = 1, custom_machine_code = None):
        
        """
        Check if the device is registered with the license key.
        The version parameter is related to the one in GetMachineCode method.
        """
        
        current_mid = ""
        
        if custom_machine_code == None:
            current_mid = Helpers.GetMachineCode(v)
        else:
            current_mid = custom_machine_code
        
        if license_key.activated_machines == None:
            return False
        
        if is_floating_license:
            for act_machine in license_key.activated_machines:
                if act_machine.Mid[9:] == current_mid or\
                   allow_overdraft and act_machine.Mid[19:] == current_mid:
                    return True
        else:
            for act_machine in license_key.activated_machines:
                if current_mid == act_machine.Mid:
                    return True
            
        return False
    
    
    @staticmethod
    def GetMACAddress():
        
        """
        An alternative way to compute the machine code (device identifier).
        This method is especially useful if you plan to target multiple platforms.
        """
        
        import uuid
        
        return ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0,8*6,8)][::-1])
    
    def HasNotExpired(license_key, allow_usage_on_expiry_date=True):

        """
        Checks that the license key has not expired. Cryptolens offers automatic blocking of licenses
        on the server side, and it is recommended to set it up instead of relying on the client side (unless 
        your application is running in offline mode). For more details, please review
        https://help.cryptolens.io/web-interface/keys-that-dont-expire

        Parameters:
            @license_key The license key object.
            @allow_usage_on_expiry_date If set to true, the license will be considered valid on the day it expires.
        """

        import datetime

        if license_key == None:
            return False
        
        diff = license_key.expires.replace(tzinfo=datetime.timezone.utc) - datetime.datetime.now(datetime.timezone.utc)

        if allow_usage_on_expiry_date and diff >= datetime.timedelta(0) or not(allow_usage_on_expiry_date) and diff > 0:
            return True

        return False

    def HasFeature(license_key, feature_name):
        
        """
        Uses a special data object associated with the license key to determine if a certain feature exists (instead of the 8 feature flags).
        <strong>Formatting: </strong> The name of the data object should be 'cryptolens_features' and it should be structured as a JSON array.
        
        For example, <pre>["f1", "f2"]</pre><p>means f1 and f2 are true. You can also have feature bundling, eg. <pre>["f1", ["f2",["voice","image"]]]</pre>
        which means that f1 and f2 are true, as well as f2.voice and f2.image. You can set any depth, eg. you can have
        <pre>["f1", ["f2",[["voice",["all"]], "image"]]]</pre> means f2.voice.all is true as well as f2.voice and f2.
        The dots symbol is used to specify the "sub-features". 
        
        Read more here: https://help.cryptolens.io/web-interface/feature-templates
        
        Parameters:
            @license_key The license key object.
            @feature_name For example, "f2.voice.all".
        
        """
        
        if license_key.data_objects == None:
            return False
        
        features = None
        
        for dobj in license_key.data_objects:
            
            if dobj["Name"] == 'cryptolens_features':
                features = dobj["StringValue"]
                break
            
        if features == None or features.strip() == "":
            return False
    
        array = json.loads(features)
            
        feature_path = feature_name.split(".")
        
        found = False
        
        for i in range(len(feature_path)):
            
            found = False
            index = -1
            
            for j in range(len(array)):
                
                if not(isinstance(array[j], list)) and array[j] == feature_path[i]:
                    found = True
                    break
                elif isinstance(array[j], list) and array[j][0] == feature_path[i]:
                    found = True
                    index = j
                    
            if not(found):
                return False
            
            if i+1 < len(feature_path) and index != -1:
                array = array[index][1]
            
        if not(found):
            return False
        
        return True

class Subscription:
    """
    Subscription related methods
    """
    
    @staticmethod
    def record_usage_to_stripe(token, product_id, key, amount=""):
        
        """
        This method records uses Stripe's metered billing to record usage for a certain subscription. In order to use this method, 
        you need to have set up recurring billing. A record will be created using Stripe's API with action set to 'increment'      
        
        More docs: https://app.cryptolens.io/docs/api/v3/RecordUsage
        """
        
        try:
            response = HelperMethods.send_request("/subscription/RecordUsage/",\
                                                  {"token":token,\
                                                   "ProductId" : product_id,\
                                                   "Key" : key,\
                                                   "Amount" : amount,
                                                   })
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

        return (jobj, "")

class User:
    
    """
    The idea behind user authentication is to allow you to authenticate 
    users using their crendntials (i.e. username and password) to verify their
    license. You can use their username and password to retrieve their 
    licenses instead of asking for a license key.

    This is similar to obtaining all licenses assigned to a customer 
    using customer secret, with the difference that the user can pick both
    the username and password, as well as restore a forgotten password.
    
    For more information, please see 
        https://help.cryptolens.io/examples/user-verification and
        https://app.cryptolens.io/docs/api/v3/UserAuth
    """
    
    @staticmethod
    def login(token, username, password):
        
        """
        This method will return all licenses that belong to the user.
        This method can be called with an access token that has UserAuthNormal 
        and UserAuthAdmin permission.
        
        More docs: https://app.cryptolens.io/docs/api/v3/Login
        """
        
        try:
            response = HelperMethods.send_request("/userauth/login/", {"token":token, "username":username, "password":password})
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

        return (jobj["licenseKeys"], "")
    
    """
    The idea behind user authentication is to allow you to authenticate 
    users using their crendntials (i.e. username and password) to verify their
    license. You can use their username and password to retrieve their 
    licenses instead of asking for a license key.

    This is similar to obtaining all licenses assigned to a customer 
    using customer secret, with the difference that the user can pick both
    the username and password, as well as restore a forgotten password.
    
    For more information, please see 
        https://help.cryptolens.io/examples/user-verification and
        https://app.cryptolens.io/docs/api/v3/UserAuth
    """
    
    @staticmethod
    def register(token, username, password, email = "", customerId = 0):
        
        """
        This method will register a new user. Please note that calling this
        method requires a UserAuthAdmin token.
        
        More docs: https://app.cryptolens.io/docs/api/v3/Register
        """
        
        try:
            response = HelperMethods.send_request("/userauth/Register/",\
                                                  {"token":token,\
                                                   "username":username,\
                                                   "password":password,\
                                                   "email":email,\
                                                   "customerid":customerId})
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

        return (jobj, "")
    
    @staticmethod
    def associate(token, username, customer_id=0):
        
        """
        Associates a user with a customer object. Please note that calling
        this method requires a UserAuthAdmin token.
        
        More docs: https://app.cryptolens.io/docs/api/v3/Associate
        """
        
        try:
            response = HelperMethods.send_request("/userauth/Associate/",\
                                                  {"token":token,\
                                                   "username":username,\
                                                   "customerid":customer_id})
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

        return (jobj, "")
    
    @staticmethod
    def dissociate(token, username):
        
        """
        Dissociates a user from a customer customer object. Please note that
        calling this method requires a UserAuthAdmin token.
        
        More docs: https://app.cryptolens.io/docs/api/v3/Dissociate
        """
        
        try:
            response = HelperMethods.send_request("/userauth/Dissociate/",\
                                                  {"token":token,\
                                                   "username":username})
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

        return (jobj, "")
    
    @staticmethod
    def get_users(token, customer_id = 0):
        
        """
        List all registered users. Please note that calling this method
        requires a UserAuthAdmin token.
        
        More docs: https://app.cryptolens.io/docs/api/v3/GetUsers
        """
        
        try:
            response = HelperMethods.send_request("/userauth/GetUsers/",\
                                                  {"token":token,\
                                                   "customerid":customer_id})
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

        return (jobj["users"], "")
    
    @staticmethod
    def change_password(token, username, new_password, old_password="", password_reset_token="", admin_mode=False):
        
        """
        This method will change the password of a user. It supports 3 modes of
        operation. With an access token that has UserAuthNormal permission
        (i.e. without admin permission), the password can either be changed by
        providing the old password or a password reset token, which can be
        generated using Reset Password Token method. Finally, if you call this
        method with an access token that has UserAuthAdmin permission, it will
        allow you to set AdminMode to True and only provide the NewPassword.
        
        More docs: https://app.cryptolens.io/docs/api/v3/ChangePassword
        """
        
        try:
            response = HelperMethods.send_request("/userauth/ChangePassword/",\
                                                  {"token":token,\
                                                   "username":username,\
                                                   "OldPassword": old_password,\
                                                   "NewPassword":new_password,\
                                                   "PasswordResetToken": password_reset_token,\
                                                   "AdminMode":admin_mode})
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

        return (jobj, "")
    
    
    @staticmethod
    def reset_password_token(token, username):
        
        """
        This method allows you to retrive the password reset token that you
        can use when calling Change Password method. Please note that calling
        this method requires a UserAuthAdmin token.
        
        More docs: https://app.cryptolens.io/docs/api/v3/ResetPasswordToken
        """
        
        try:
            response = HelperMethods.send_request("/userauth/ResetPasswordToken/",\
                                                  {"token":token,\
                                                   "username":username})
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

        return (jobj["passwordResetToken"], "")
    
    
    @staticmethod
    def remove_user(token, username):
        
        """
        This method removes a user. Please note that calling this method
        requires a UserAuthAdmin token.
        
        More docs: https://app.cryptolens.io/docs/api/v3/RemoveUser
        """
        
        try:
            response = HelperMethods.send_request("/userauth/RemoveUser/",\
                                                  {"token":token,\
                                                   "username":username})
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

        return (jobj, "")