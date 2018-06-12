#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 11:13:06 2018

@author: pool
aim: try to use multi signature to secure our accounts
"""
from bitcoin.rpc import RawProxy

# basic variables
p=RawProxy()
add = dict()
privkey = dict()
pubkey = dict()
mid = "\",\""

for i in range(0, 3):
    print('\n')
    print("Brand new address pair: Number", i+1)

    add[i] = p.getnewaddress()
    print("Compressed public address -", len(add[i]), "chars -", add[i])

    privkey[i] = p.dumpprivkey(add[i])
    print("Private key -", len(privkey[i]), "chars -", privkey[i])

    validDate = p.validateaddress(add[i])
    pubkey[i]=validDate["pubkey"]
    print("Less compressed public key/address -", len(pubkey[i]), "chars -", pubkey[i])


# command used in the bitcoind, you can test it by the command line
print('\n')
print("-----------command used in the bitcoind-------------------")
print ("%s%s%s%s%s%s%s" % ('bitcoin-cli createmultisig 2 \'["',pubkey[0],mid,pubkey[1],mid,pubkey[2],'"]\''))

print('\n')
threeaddy = [pubkey[0],pubkey[1],pubkey[2]]
print ("The multisig address is")
multisigaddy = p.addmultisigaddress(2,threeaddy)
multiaddyandredeem = (p.createmultisig(2,threeaddy))
print (len(multisigaddy),"chars - ", multisigaddy)
print('\n')
print ("The redeemScript -", len(multiaddyandredeem["redeemScript"]), "chars -",multiaddyandredeem["redeemScript"])
print('\n')
