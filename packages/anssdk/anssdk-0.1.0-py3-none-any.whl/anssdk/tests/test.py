'''
Copyright (c) 2022 Algorand Name Service

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
'''


import unittest
import ans_helper as anshelper


import sys
sys.path.append('../')
from anssdk import constants, transactions

from anssdk.resolver import ans_resolver

unittest.TestLoader.sortTestMethodsUsing = None

class TestDotAlgoNameRegistry(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.algod_client = anshelper.SetupClient()
        cls.algod_indexer = anshelper.SetupIndexer()
        cls.app_index = constants.APP_ID
        cls.resolver_obj = ans_resolver(cls.algod_client, cls.algod_indexer)
        cls.transactions_obj = transactions.Transactions(cls.algod_client)


    def test_name_resolution(self):
        
        account_info = self.resolver_obj.resolve_name('lalith')
        self.assertEqual(account_info["owner"], 'PD2CGHFAZZQNYBRPZH7HNTA275K3FKZPENRSUXWZHBIVNPHVDFHLNIUSXU')

    def test_prep_name_reg_txns(self):
        
        name_reg_txns = self.transactions_obj.prepare_name_registration_transactions(
            'xyz1234',
            'RANDGVRRYGVKI3WSDG6OGTZQ7MHDLIN5RYKJBABL46K5RQVHUFV3NY5DUE',
            5
        )
        self.assertGreaterEqual(len(name_reg_txns), 2)       

    def test_prep_link_socials_txn(self):

        edited_handles = {
            'discord': 'lmedury',
            'twitter': 'lmedury'
        }

        update_name_property_txns = self.transactions_obj.prepare_update_name_property_transactions('ans.algo', 'PD2CGHFAZZQNYBRPZH7HNTA275K3FKZPENRSUXWZHBIVNPHVDFHLNIUSXU', edited_handles)  
        self.assertGreaterEqual(len(update_name_property_txns), 2)

    def test_prep_name_renew_txns(self):

        name_renew_txns = self.transactions_obj.prepare_name_renewal_transactions('ans.algo', 'PD2CGHFAZZQNYBRPZH7HNTA275K3FKZPENRSUXWZHBIVNPHVDFHLNIUSXU', 2)
        self.assertEqual(len(name_renew_txns), 2)

    def test_prep_initiate_name_transfer_txn(self):

        initiate_transfer_txn = self.transactions_obj.prepare_initiate_name_transfer_transaction('ans.algo', 'PD2CGHFAZZQNYBRPZH7HNTA275K3FKZPENRSUXWZHBIVNPHVDFHLNIUSXU', 'RANDGVRRYGVKI3WSDG6OGTZQ7MHDLIN5RYKJBABL46K5RQVHUFV3NY5DUE', 0)

    def test_prep_accept_name_transfer_txns(self):

        accept_transfer_txns = self.transactions_obj.prepare_accept_name_transfer_transactions('ans.algo', 'RANDGVRRYGVKI3WSDG6OGTZQ7MHDLIN5RYKJBABL46K5RQVHUFV3NY5DUE', 'PD2CGHFAZZQNYBRPZH7HNTA275K3FKZPENRSUXWZHBIVNPHVDFHLNIUSXU', 0)
        self.assertEqual(len(accept_transfer_txns), 3)

    def test_names_owned_by_address(self):
        
        account_info = self.resolver_obj.get_names_owned_by_address('PD2CGHFAZZQNYBRPZH7HNTA275K3FKZPENRSUXWZHBIVNPHVDFHLNIUSXU', True, True, 3)
        self.assertGreaterEqual(len(account_info), 2)
      

if __name__ == '__main__':
    unittest.main()
