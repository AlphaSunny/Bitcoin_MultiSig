# This simple wallet works with bitcoind and will only work with 2-of-3 multisigs
# Using the python-bitcoinlib library

# 如何分布三个私钥的存储
# 一个自己使用，一个存放在wallet provider， 一个放在最安全的地方，一般不用

# 如何来花这个multisig addr中的比特币？
# 比如你想到taobao.com上去花比特币买东西，你这时用自己的私钥来 createrawTransaction,但是这时交易显示的花费是失败的，
# 这时你将signed之后的原始交易发给第三方平台，这时你就让它用私钥来sign你sign过的transaction，这时会显示花费成功
import bitcoin
from bitcoin.rpc import RawProxy

bitcoin.SelectParams('testnet')
p = RawProxy() #creates an object called p that allows for bitcoind calls

money = p.getbalance()
print(money)
# YOU NEED AT LEAST TWO OF THE PRIVATE KEYS FROM PART ONE linked to your MULTI-SIG ADDRESS
multisigprivkeyone = "cPw3fUfVnhZNNpg8mEnoNcbrk4VhhobDohZBcZdrS3pfP53ymhB2" 
multisigprivkeytwo = "cPpjLNPGgvwfCSUuXk1qExmBQB71piHxMUxmukzLr43m38VqsCHo"
multisigprivkeythree = "cT2YurYhGWiShznfwzcsysf1a4koDhP369dtWiKBTyZV1HMTGLEk"
ChangeAddress = "2NBwWtf4mQcmx1mR2tNSsuh21LsoPtbxA79" # Makes Sure to set your own personal Change Address

SetTxFee = int(0.00005461*100000000) 


# ask your account, how much money you have
unspent = p.listunspent() # Query wallet.dat file for unspent funds to see if we have multisigs to spend from

print( "Your Bitcoin-QT/d has",len(unspent),"unspent outputs")
for i in range(0, len(unspent)):
    print('\n')
    print( "Output",i+1,"has",unspent[i]["amount"],"bitcoins, or",int(unspent[i]["amount"]*100000000),"satoshis")
    print( "The transaction id for output",i+1,"is")
    print( unspent[i]["txid"])
    print( "The ScriptPubKey is", unspent[i]["scriptPubKey"])
    print( "on Public Address =====>>",unspent[i]["address"])

print('\n')
totalcoin = int(p.getbalance()*100000000)
print( "The total value of unspent satoshis is", totalcoin)
print('\n')


# 让用户选择来花费哪个utxo，因为是测试网络生成的multisig的开头也为2   ???????
WhichTrans = int(input('Spend from which output? '))-1
if WhichTrans > len(unspent): #Basic idiot check. Clearly a real wallet would do more checks.
    print( "Sorry that's not a valid output" )
else:
    tempaddy = str(unspent[WhichTrans]["address"])
    print('\n')
    if int(tempaddy[0:1]) == 1:
        print( "The public address on that account starts with a '1' - its not multisig.")
    elif int(tempaddy[0:1]) == 2:
        print( "The public address on that account is",tempaddy)
        print( "The address starts with the number '3' which makes it a multisig.")
        print('\n')
        print( "All multisig transactions need: txid, scriptPubKey and redeemScript")
        print( "Fortunately all of this is right there in the bitcoind 'listunspent' json from before")
        print('\n')
        print( "The txid is:",unspent[WhichTrans]["txid"])
        print( "The ScriptPubKey is:", unspent[WhichTrans]["scriptPubKey"])
        print('\n')
        # 注意只有multisig含有redeemscripts
        print( "And only multisigs have redeemScripts.")
        print( "The redeemScript is:",unspent[WhichTrans]["redeemScript"])
        print('\n')

        print( "You have",int(unspent[WhichTrans]["amount"]*100000000),"satoshis in this output.")

        HowMuch = int(input('How much do you want to spend? '))
        if HowMuch > int(unspent[WhichTrans]["amount"]*100000000):
            print( "Sorry not enough funds in that account") # check to see if there are enough funds.)
        else:
            print('\n')
            # 输入你想需要将比特币 汇入的地址
            SendAddress = str(input('Send funds to which bitcoin address? ')) 
            print('\n')
            Leftover = int(unspent[WhichTrans]["amount"]*100000000)-HowMuch-SetTxFee
            print( "This send to",SendAddress,"will leave", Leftover,"Satoshis in your accounts.")
            print( "A tx fee of",SetTxFee,"will be sent to the miners")
            print('\n')
            print( "Creating the raw transaction for User One - Private Key One")
            print('\n')

            rawtransact = p.createrawtransaction ([{"txid":unspent[WhichTrans]["txid"],
                    "vout":unspent[WhichTrans]["vout"],
                    "scriptPubKey":unspent[WhichTrans]["scriptPubKey"],
                    "redeemScript":unspent[WhichTrans]["redeemScript"]}],{SendAddress:HowMuch/100000000.00,ChangeAddress:Leftover/100000000.00})
            print("bitcoind decoderawtransaction", rawtransact)
            print('\n')
            print('\n')
            print("And now we'll sign the raw transaction -> The first user gets a 'False'")
            print("This makes sense because in multisig, no single entity can sign alone")
            print('\n')
            print("For fun you can paste this FIRST signrawtransaction into bitcoind to verify multisig address")
            print("%s%s%s%s%s%s%s%s%s%s%s%s%s" % ('bitcoind signrawtransaction \'',rawtransact,'\' \'[{"txid":"',unspent[WhichTrans]["txid"],'","vout":',
                                      unspent[WhichTrans]["vout"],',"scriptPubKey":"',unspent[WhichTrans]["scriptPubKey"],'","redeemScript":"',
                                      unspent[WhichTrans]["redeemScript"],'"}]\' \'["',multisigprivkeyone,'"]\''))
            print('\n')

            # 通过一个私钥，调用signrawtransaction功能，返回了一串 hex码
            signedone = p.signrawtransaction (rawtransact,
                    [{"txid":unspent[WhichTrans]["txid"],
                    "vout":unspent[WhichTrans]["vout"],"scriptPubKey":unspent[WhichTrans]["scriptPubKey"],
                    "redeemScript":unspent[WhichTrans]["redeemScript"]}],
                    [multisigprivkeyone])
            # 通过hex码来提交
            print(signedone)
            print('\n')
            # 意味着在实际的软件开发中，只需要将一个私钥sign后的hex码发给另一个私钥的拥有者，就可以花费这笔钱了
            print("In a real world situation, the 'hex' part of this thing above would be sent to the second")
            print("user or the wallet provider. Notice, the private key is not there. It has been signed digitally")
            print('\n')
            print('\n')
            print("you can paste this SECOND signrawtransaction into bitcoind to verify multisig address")
            print("%s%s%s%s%s%s%s%s%s%s%s%s%s" % ('bitcoind signrawtransaction \'',signedone["hex"],'\' \'[{"txid":"',unspent[WhichTrans]["txid"],'","vout":',
                                      unspent[WhichTrans]["vout"],',"scriptPubKey":"',unspent[WhichTrans]["scriptPubKey"],'","redeemScript":"',
                                      unspent[WhichTrans]["redeemScript"],'"}]\' \'["',multisigprivkeytwo,'"]\''))
            doublesignedrawtransaction = p.signrawtransaction (signedone["hex"],
                    [{"txid":unspent[WhichTrans]["txid"],
                    "vout":unspent[WhichTrans]["vout"],"scriptPubKey":unspent[WhichTrans]["scriptPubKey"],
                    "redeemScript":unspent[WhichTrans]["redeemScript"]}],
                    [multisigprivkeytwo])

            # 经过两个私钥签名后就得到了这串hex码，只要将其提交给node，这笔交易就会被花费
            print( doublesignedrawtransaction)
            print('\n')
            print( "You are now ready to send",HowMuch,"Satoshis to",SendAddress)
            print( "And",Leftover,"Satoshis will be sent to the change account",ChangeAddress)
            print( "Finally, a miner's fee of ",SetTxFee,"Satoshis will be sent to the miners")
            print('\n')

            # 在这里就不实际花费了，如果你想实际花费，直接调用 bitcoind sendrawtransaction这个接口

