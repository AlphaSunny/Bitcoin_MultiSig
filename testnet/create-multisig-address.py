#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 11:13:06 2018

@author: pool
aim: try to use multi signature to secure our accounts
"""
import bitcoin
from bitcoin.rpc import RawProxy
bitcoin.SelectParams('testnet')

# basic variables
p=RawProxy()
add = dict()
privkey = dict()
pubkey = dict()
mid = "\",\""

for i in range(0, 3):
    print('\n')
    print("Brand new address pair: Number", i+1)
    
    #地址
    add[i] = p.getnewaddress()
    print("Compressed public address -", len(add[i]), "chars -", add[i])
    
    # 通过dumpprivkey 来得到私钥
    privkey[i] = p.dumpprivkey(add[i])
    print("Private key -", len(privkey[i]), "chars -", privkey[i])

    # 得到公钥
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
# 生成multisig需要使用没压缩过得public key

# 给账户添加一个multisig地址， 返回multisig的地址
multisigaddy = p.addmultisigaddress(2,threeaddy)

# 返回一个json值
multiaddyandredeem = (p.createmultisig(2,threeaddy))
print (len(multisigaddy),"chars - ", multisigaddy)
print('\n')
print ("The redeemScript -", len(multiaddyandredeem["redeemScript"]), "chars -",multiaddyandredeem["redeemScript"])
print('\n')
