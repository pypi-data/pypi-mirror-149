from algosdk import encoding
from pyteal import compileTeal, Mode
from algosdk.future.transaction import LogicSig
from algosdk import logic
import base64
import time
from pyteal import *
from anssdk import constants, dot_algo_name_record
from anssdk.helper import validation

class ans_resolver:
    
    def __init__(self, client, indexer=None):
        self.algod_client = client
        if(indexer is not None):
            self.algod_indexer = indexer

    def compile_program(self, algod_client, source_code) :
        compile_response = algod_client.compile(source_code.decode('utf-8'))
        return base64.b64decode(compile_response['result'])            

    def prep_name_record_logic_sig(self, name, reg_app_id):
        reg_escrow_acct = logic.get_application_address(reg_app_id)
        logic_sig_teal = compileTeal(dot_algo_name_record.ValidateRecord(name,reg_app_id,reg_escrow_acct), Mode.Signature, version=4)
        validate_name_record_program = self.compile_program(self.algod_client, str.encode(logic_sig_teal))
        lsig = LogicSig(validate_name_record_program)
        return lsig

    def resolve_name(self, name):
        
        name = name.split('.algo')[0]
        name = name.lower()
        validation.is_valid_name(name)
        reg_app_id = constants.APP_ID
        account_info = self.algod_client.account_info(address=self.prep_name_record_logic_sig(name, reg_app_id).address())
        if(len(account_info["apps-local-state"]) == 0):
            return({
                'found': False
            })
        try:
            socials = []
            metadata = []
            allowed_socials = ['twitter', 'github', 'youtube', 'telegram', 'reddit', 'discord']
            for apps_local_data in account_info['apps-local-state']:
                owner = None
                expiry = None
                if(apps_local_data['id']==reg_app_id):
                    for key_value in apps_local_data['key-value']:
                        
                        if(validation.decode_value(key_value['key'])=="expiry"):
                            expiry = key_value['value']['uint']
                        elif(validation.decode_value(key_value['key'])=="owner"):
                            owner = validation.decode_address((key_value['value']['bytes']))
                        
                        elif(validation.decode_value(key_value['key']) in allowed_socials):
                            key = validation.decode_value(key_value['key'])
                            kv = {}
                            kv[key] = validation.decode_value(key_value['value']['bytes'])
                            socials.append(kv)
                        else:
                            key = validation.decode_value(key_value['key'])
                            if(key == 'name'):
                                continue
                            if(key == 'transfer_to'):
                                if(validation.decode_address((key_value['value']['bytes'])) != ''):
                                    value = validation.decode_address((key_value['value']['bytes']))
                                    if(value == b''):
                                        continue
                                    kv = {}
                                    kv[key] = value
                                    metadata.append(kv)
                                    continue
                            if(key == 'transfer_price'):
                                if(key_value['value']['uint'] != ''):
                                    value = key_value['value']['uint']
                                    kv = {}
                                    kv[key] = value
                                    metadata.append(kv)
                                    continue
                            if(validation.decode_value(key_value['value']['bytes']) != ''):
                                kv = {}
                                kv[key] = validation.decode_value(key_value['value']['bytes'])
                                metadata.append(kv)
                        
                                            
                if(owner!=None and expiry!=None and expiry>int(time.time())):
                    return ({
                        'found': True,
                        'owner': owner,
                        'expiry': expiry,
                        'socials': socials,
                        'metadata': metadata
                    })
                else:
                    
                    return ({
                        'found': False
                    })

        except Exception as e:
            print(e)
            return ({
                'found': False
            })         

    def get_names_owned_by_address(self,address, socials=False, metadata=False, limit=0):
        is_valid_address = encoding.is_valid_address(address)
        indexer = None
        try:
            if(self.algod_indexer is not None):
                indexer = self.algod_indexer
        except Exception as err:
            return({
                'err': 'Indexer is not instantiated'
            })
            return

        if(is_valid_address is False):
            return(
                {
                    'err':'Invalid Algorand address'
                }
            )
        else:
            
            next_token = ''
            txn_length = 1
            txns = []
            
            while(txn_length > 0):
                
                account_info = indexer.search_transactions_by_address(address=address, limit=10000, next_page=next_token, start_time="2022-02-25")
                
                if(len(account_info["transactions"]) > 0):
                    txn_length = len(account_info["transactions"])
                    txns+=account_info["transactions"]
                    if(account_info["next-token"] is not None):
                        next_token = account_info["next-token"]
                    else:
                        break
                else:
                    break
                
            names = []
            owned_names = []
            try:
                for txn in txns:
                    
                    if(txn["tx-type"] == "appl"):
                        
                        if(txn["application-transaction"]["application-id"] == constants.APP_ID):
                            args = txn["application-transaction"]["application-args"]
                            method = base64.b64decode(args[0]).decode('utf-8')
                            if(len(args) >= 2 or method == 'accept_transfer'):
                                
                                if(method == 'register_name'):
                                    arg_1 = base64.b64decode(args[1]).decode('utf-8')
                                    if(arg_1 not in names):
                                        names.append(arg_1+'.algo')
                                elif(method == 'accept_transfer'):
                                    lsig_account = txn["application-transaction"]["accounts"][0]
                                    lsig_account_info = indexer.account_info(lsig_account)
                                    lsig_account_info = lsig_account_info["account"]["apps-local-state"]
                                    
                                    for app in lsig_account_info:
                                        if(app["id"] == constants.APP_ID):
                                            kv_pairs = app["key-value"]
                                            
                                            for kv_pair in kv_pairs:
                                                
                                                key = base64.b64decode(kv_pair["key"]).decode('utf-8')
                                                value = base64.b64decode(kv_pair["value"]["bytes"])
                                                #print(key)
                                                if(key == 'name'):
                                                    
                                                    if(value not in names):
                                                        names.append(value.decode('utf-8')+'.algo')
                                                        break
                owned_names = []
                for name in names:
                    if(len(owned_names) >= limit and limit > 0):
                        return owned_names

                    domain_info = self.resolve_name(name)
                    if(domain_info["owner"] == address):
                        kv = {}
                        kv['name'] = name
                        if(socials is True):
                            kv['socials'] = domain_info['socials']
                        if(metadata is True):
                            kv['metadata'] = domain_info['metadata']
                        owned_names.append(kv)

            except Exception as err:
                print('Error: ',err)
                return []

            return owned_names            
        
    





